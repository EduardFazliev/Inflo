import json
import logging
import pprint
import sys
import time
from encodings.utf_8 import encode

import fish
import requests


logger = logging.getLogger(__name__)


class FlopsJsonException(Exception):
    """
    Custom exception class for Flops json parsing.
    """
    def __init__(self):
        self.message = 'Invalid JSON received.'


class FlopsJsonNoSuchKeyException(FlopsJsonException):
    """
    Custom exception class for no such key in json.

    Args:
        key: Json key, that could not be found in received json.
    """
    def __init__(self, key):
        super(FlopsJsonException, self).__init__()
        self.message += 'No key {0} in received json was found.'.format(key)


class FlopsApi(object):
    """
    This class is Flops API python realization.
    """
    inflo_key = 'inflo_created_'
    api_link = 'https://api.flops.ru/api/v1/'
    created_vm_info_file = 'created_vm'

    def __init__(self, api_key, customer_id):
        """
        Args:
            api_key: API key for Flops account.
            customer_id: ID of Flops customer.
        """
        self.api_key = api_key
        self.customer_id = customer_id

    @staticmethod
    def send_get_request(url, payload):
        """Sends get request with spec header.
        Args:
            url (str): API URL to send comment.
            payload (dict): json to send.
        Returns:
            result.content (dict): Response content in json format.
        """
        logger.debug('GET request: url: {0}, payload: {1}'.format(url, payload))
        try:
            response = requests.get(url, params=payload)
        except Exception as e:
            logger.debug('GET request returned error: {0}'.format(e))
            logger.info('Request error. Use "-v" flag for debug output.')
            sys.exit(1)
        else:
            logger.debug('GET respond: status: {0}, content: {1}'.format(response.status_code, response.content))
            return 0, response.content

    @staticmethod
    def deserialize_json(json_string):
        """
        Loads json in a dict, throws FlopsJsonException if failed.

        Args:
            json_string: Json string to load in dict.

        Returns:
            dsr_dict(dict): Dictionary loaded from json.
        """
        try:
            dsr_dict = json.loads(json_string)
        except Exception as e:
            logger.debug(e)
            raise FlopsJsonException()
        else:
            return dsr_dict

    @staticmethod
    def get_dict_key(input_dict, key):
        """
        Get value of specific key, throws FlopsJsonException if failed.

        Args:
            input_dict(dict): Original dictionary.
            key: Required dictionary key.

        Returns:
            result: Value of key "key" in dictionary "input_dict".
        """
        try:
            result = input_dict[key]
        except KeyError as e:
            logger.debug('Error while trying get key value: {0}'.format(e))
            raise FlopsJsonNoSuchKeyException(key)
        except TypeError as e:
            logger.debug('Unexpected exception: {0}'.format(e))
            raise FlopsJsonException()
        except KeyboardInterrupt:
            logger.info('Interrupted by user.')
            logger.debug('Interrupted by user while executing "get_dict_key" with parameters:\n'
                         'input dict: {0}\n'
                         'key: {1}'.format(input_dict, key))
        else:
            return result

    def check_inflo_key(self, vm_id):
        """
        Function checks if special key 'inflo_key' is in VM name.

        Args:
            vm_id: Virtual machine ID.

        Returns:
            True if 'inflo_key' is in VM name, False otherwise.

        """
        url = '{0}vm/{1}/'.format(FlopsApi.api_link, vm_id)

        vm_info = self.info(url)
        status = self.get_dict_key(vm_info, 'status')

        if status != 'OK':
            logger.info('Can not get virtual server name to check.')
            return False
        else:
            result = self.get_dict_key(vm_info, 'result')
            vm_name = self.get_dict_key(result, 'name')
            if FlopsApi.inflo_key in vm_name:
                return True
            else:
                return False

    def vm_info_by_name(self, name):
        """
        Get virtual machine info by name.

        Args:
            name(str): Name of virtual machine.

        Returns:
            Tuple (0, dict) if VM with name 'name' found, 1 otherwise.

        """
        # Get servers list
        url = '{0}vm/'.format(FlopsApi.api_link)
        response = self.info(url)

        server_list = self.get_dict_key(response, 'result')

        for server in server_list:
            checked_name = self.get_dict_key(server, 'name')
            if checked_name == name:
                server_ip = self.get_dict_key(server, 'ipAddresses')
                server_id = self.get_dict_key(server, 'id')
                logger.debug('Server with name {0} found. IP: {1}, ID: {2}'.format(name, server_ip, server_id))
                return 0, {
                    'ip': server_ip[0],
                    'id': server_id
                }

        logger.info('No VM with name {0} was found.'.format(name))
        return 1

    def wait_for_async_answer(self, operation_id, timeout=180):
        """
        Function waits for answer when async operation is in progress and prints current progress.

        Args:
            operation_id: ID of executing async operation.
            timeout: Timeout for operation.

        Returns:
            Tuple (1, err) if errorMessage is in received json,
            tuple (0, result) if 'status' files in received json is 'DONE' and
            tuple (2, timeout_str) if timeout is reached.

        """
        # Generating API URL to get information about ansync operation status.
        url = '{0}operation/{1}/'.format(FlopsApi.api_link, operation_id)
        logger.debug('URL for operation request is {0}.'.format(url))

        # Initialize progress bar, timeout_counter.
        pb = fish.ProgressFish(total=100)
        logger.debug('Progress bar initialized with total amount of 100.')
        timeout_counter = 0
        logger.debug('Timeout counter is initialized. Total timeout set to: {0}'.format(timeout))

        while True:
            # Get json with status of operation.
            info_common = self.info(url)
            result = self.get_dict_key(info_common, 'result')

            # If error message is appears, then return error.
            try:
                err = result['errorMessage']
            except KeyError:
                logger.debug('No error message in response.')
            else:
                return 1, err
            finally:
                logger.debug('Checking error message finished.')

            # If percentage is equal 100 and status is "DONE" - return
            # success code and result dict.
            percentage = self.get_dict_key(result, 'percentage')
            status = self.get_dict_key(result, 'status')
            if percentage in ('100', 100) and status == 'DONE':
                pb.animate(amount=100)
                logger.debug('Operation with ID {0} is finished.'.format(operation_id))
                return 0, result

            # Show current progress with "fish" progress bar.
            pb.animate(amount=percentage)

            if timeout_counter > timeout:
                logger.debug('Timeout is reached. Returning error.')
                return 2, 'Timeout of {0} is reached.'.format(timeout)
            else:
                timeout_counter += 5
                logger.debug('Timeout counter is increased. Current value: {0}.'.format(timeout_counter))

            time.sleep(5)

    def info(self, url):
        """
        Function is executing API call with specific url 'url' and print and returns response.

        Args:
            url: URL for API call.

        Returns:
            response(dict): Dictionary loaded from received json.
        """
        # For info we need only send api key and id in payload.
        payload = {
            'clientId': self.customer_id,
            'apiKey': self.api_key
        }
        code, message = self.send_get_request(url, payload)
        # Using staticmethod to ensure, that response is a correct json.
        response = self.deserialize_json(message)
        # Pretty print dict

        pprint.pprint(response)
        return response

    def create_vm(self, name, tenant_id, distr_id, tariff_id, memory, disk, cpu, ip_count, password, send_password,
                  open_support_access, public_key_id, software_id):
        """
        Function create virtual machine with received parameters.
        Args:
            name: VM name.
            tenant_id: Tenant ID.
            distr_id: ID of required OS distro.
            tariff_id: ID of tariff.
            memory: Amount of memory.
            disk: Disk size.
            cpu: Cpu core count.
            ip_count: External IP addresses count.
            password: Desired password.
            send_password: Send password to email or not.
            open_support_access: Open access for Flops support team or not.
            public_key_id: ID of public keys to add to new VM.
            software_id: ID of software should be installed on new VM.

        Returns:
            0 is VM successfully created, 1 if VM not created and
            -1 if there is no errors, but no info about VM is received.

        """
        # Generate Flops API URL for creating virtual server.
        url = '{0}vm/install/'.format(FlopsApi.api_link)
        logger.debug('URL for create-vm: {0}'.format(url))
        # Change server name to show, that it was created by Inflo.
        name = FlopsApi.inflo_key + name
        logger.debug('Generated name for virtual server is {0}'.format(name))

        payload = {
            'clientId': self.customer_id,
            'apiKey': self.api_key,
            'name': name,
            'tenantId': tenant_id,
            'distributionId': distr_id,
            'tariffId': tariff_id,
            'memory': memory,
            'disk': disk,
            'cpu': cpu,
            'ipCount': ip_count,
            'password': password,
            'sendPassword': send_password,
            'openSupportAccess': open_support_access,
            'publicKeyIds': public_key_id,
            'softwareIds': software_id
        }
        logger.debug('Payload for sending get request to create virtual server is formed: {0}'.format(payload))
        code, message = self.send_get_request(url, payload)
        response = self.deserialize_json(message)

        vm_id = self.get_dict_key(response, 'result')
        operation_id = self.get_dict_key(response, 'operationId')

        logger.debug('Response is received:{0}'.format(response))

        pprint.pprint(response)

        code, message = self.wait_for_async_answer(operation_id)

        if code == 0:
            logger.info('Operation with ID {0} is finished. Virtual machine {1} is created.'.format(operation_id, name))
            # Get server-list for determine vm ID.
            code, message = self.vm_info_by_name(name)

            # If virtual server is appeared in server list, store it's ip, id and name in file.
            if code == 0:
                with open(FlopsApi.created_vm_info_file, 'w') as f:
                    f.write('vm_name {0}\n'.format(name))
                    f.write('ip {0}\n'.format(message['ip']))
                    f.write('id {0}\n'.format(message['id']))
                return 0
            else:
                logger.info('Virtual machine is created, but no info retrieved. Check Flops web-console for details.')
                return -1
        else:
            # If virtual server with specific name not appeared in server list, then something went wrong.
            logger.info(
                    'Operation with ID {0} is NOT finished. Virtual machine {1} is NOT created. '
                    'Reason: {2}'.format(operation_id, name, message)
            )
            return 1

    def delete_vm(self, vm_id, tenant_id):
        """
        Function deletes VM by VM ID and Tenant ID.

        Args:
            vm_id: Virtual machine ID.
            tenant_id: Tenant ID.

        Returns:
            0.

        """
        url = '{0}vm/{1}/delete'.format(FlopsApi.api_link, vm_id)
        # Getting info in raw(json) format.

        key_exist = self.check_inflo_key(vm_id)

        if key_exist:
            logger.debug('Inflo key is in virtual server name, deleting...')
            payload = {'clientId': self.customer_id, 'apiKey': self.api_key, 'tenantId': tenant_id}
            logger.debug('Payload for deleting server formed: {0}.'.format(payload))

            code, message = self.send_get_request(url, payload)
            answer = self.deserialize_json(message)

            pprint.pprint(answer)

            logger.info('VM is successfully deleted.')
        else:
            logger.inflo('VM is NOT deleted.')
        return 0

    def shutdown(self, vm_id, tenant_id):
        """
        Function shutdown VM by VM ID and Tenant ID.

        Args:
            vm_id: VM ID.
            tenant_id: Tenant ID.

        Returns:
            0 if VM is stopped, 1 otherwise.
        """
        url = '{0}vm/{1}/poweroff'.format(FlopsApi.api_link, vm_id)

        key_exist = self.check_inflo_key(vm_id)

        if key_exist:
            logger.debug('Inflo key is in virtual server name, shutdown in progress...')
            payload = {'clientId': self.customer_id, 'apiKey': self.api_key, 'tenantId': tenant_id}
            logger.debug('Payload for stopping server formed: {0}'.format(payload))

            code, message = self.send_get_request(url, payload)
            answer = self.deserialize_json(message)
            pprint.pprint(answer)
            operation_id = self.get_dict_key(answer, 'operationId')

            code, message = self.wait_for_async_answer(operation_id)

            if code == 0:
                logger.info(
                    'Operation with ID {0} is finished. Virtual machine with ID {1} is stopped.'.format(operation_id,
                                                                                                        vm_id))
                return 0
            else:
                logger.info(
                        'Operation with ID {0} is NOT finished. Virtual machine {1} may be NOT stopped. '
                        'Reason: {2}'.format(operation_id, vm_id, message)
                )
                return 1
        else:
            logger.info('No inflo key is in virtual server name, will not stop VM.')
            logger.debug('key_exist value is {0}, not stopping VM.'.format(key_exist))
            return 1
