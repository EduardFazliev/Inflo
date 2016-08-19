import json
import logging
import sys
import time

import fish
import prettytable

import helpers
import requests_lib


logger = logging.getLogger(__name__)
inflo_delete_key = 'inflo_created_'


def get_created_vm_info(name, api_key, customer_id):
    # Get servers list
    url = '{0}vm/'.format(helpers.api_link)
    response = get_info(api_key=api_key, customer_id=customer_id, raw=True, url=url)
    try:
        server_list = response['result']
    except KeyError:
        err_message = 'No key "result" in response json.'
        logger.exception(err_message)
        return 2, err_message

    for server in server_list:
        if server['name'] == name:
            return 0, {
                'ip': server['ipAddresses'][0],
                'id': server['id']
            }

    return 1, 'No VM with name {0} was found.'.format(name)


# Print functions #
def print_info(answer, headers):
    try:
        status = answer['status']
    except KeyError:
        err_message = 'Error: No "Status" received!'
        print err_message
        return -1, err_message
    try:
        result = answer['result']
    except KeyError:
        err_message = 'Error: No "Result" received!'
        print err_message
        return -1, err_message

    print '''
    #-#-#-#-#
    -> Status: {0}
    -> Result:
    '''.format(status)

    pt = prettytable.PrettyTable()
    for header in headers:
        if type(header) == tuple:
            if header[0] == 2:
                try:
                    pt.add_column(header[2], [subject[header[1]][header[2]] for subject in result])
                except TypeError:
                    pt.add_column(header[2], [result[header[1]][header[2]]])
                except Exception:
                    print 'Error while generating table of results. Will print raw json result instead.'
                    print result
                    logger.exception('Error while adding value to pretty table object.')
                    sys.exit(0)
        else:
            try:
                pt.add_column(header, [subject[header] for subject in result])
            except TypeError:
                pt.add_column(header, [result[header]])
            except Exception:
                print 'Error while generating table of results. Will print raw json result instead.'
                print result
                logger.exception('Error while adding value to pretty table object.')
                sys.exit(0)

    print pt


def print_result(answer, headers):
    status = answer['status']

    print '''
    #-#-#-#-#
    -> Status: {0}
    -> Result:
    '''.format(status)

    pt = prettytable.PrettyTable()
    for header in headers:
        try:
            pt.add_column(header, answer[header])
        except Exception as e:
            print 'Can not add key {0}'.format(header)
            print answer
            logger.debug(e)

    print pt
###################


# Information functions #


def get_info(api_key=None, customer_id=None, raw=False, url=None, table_format=None):
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key, }
    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)
    if raw:
        print message
    else:
        print_info(answer, table_format)

    return answer


def wait_for_async_answer(api_key=None, customer_id=None, raw=True, url=None, operation_id=None, retry=3, timeout=180):
    url = '{0}operation/{1}/'.format(helpers.api_link, operation_id)
    logger.debug('URL for operation request is {0}.'.format(url))

    # Initialize progress bar, retry_counter, timeout_counter.
    pb = fish.ProgressFish(total=100)
    logger.debug('Progress bar initialized with total amount of 100.')
    retry_counter = 0
    logger.debug('Retry counter is initialized. Total retries available: {0}'.format(retry))
    timeout_counter = 0
    logger.debug('Timeout counter is initialized. Total timeout set to: {0}'.format(timeout))

    while True:
        info_common = get_info(api_key=api_key, customer_id=customer_id, raw=raw, url=url)

        logger.debug('Loaded successfully.\nTrying to get value of "result" key.')
        try:
            info = info_common['result']
        except KeyError:
            err_message = 'No "result" key in response json.'
            logger.exception(err_message)
            return 1, err_message

        # If error occurred - return error code and error message.
        try:
            if info['errorMessage'] is not None:
                logger.debug('Response reported error: {0}'.format(info['errorMessage']))
                return 3, info['errorMessage']
        except KeyError:
            logger.exception('No "errorMessage" key in response json.')

        # If percentage is equal 100 and status is "DONE" - return
        # success code and 'info' dictionary.
        try:
            if info['percentage'] in ('100', 100) and info['status'] == 'DONE':
                pb.animate(amount=100)
                logger.debug('Operation with ID {0} is finished.'.format(operation_id))
                return 0, info
        except KeyError:
            logger.exception('No "percentage" or "status" key in response json.')

        # Show current progress with "fish" progress bar.
        pb.animate(amount=info['percentage'])

        if timeout_counter > timeout:
            logger.debug('Timeout is reached. Returning error.')
            return 2, 'Timeout of {0} is reached.'.format(timeout)
        else:
            timeout_counter += 1
            logger.debug('Timeout counter is increased. Current value: {0}.'.format(timeout_counter))

        time.sleep(1)


# Action functions #
def create_vm(name, tenant_id, distr_id, tariff_id, memory, disk, cpu, ip_count, password, send_password,
              open_support_access, public_key_id, software_id, api_key=None, customer_id=None, raw=False):
    url = '{0}vm/install/'.format(helpers.api_link)
    logger.debug('URL for create-vm: {0}'.format(url))

    if api_key in [None, ''] or customer_id in [None, '']:
        logger.debug('API key and customer ID is not provided, so trying to get them from file...')
        api_key, customer_id = helpers.get_conf()
    else:
        logger.debug('API key and customer ID provided.')

    name = inflo_delete_key + name

    payload = {
        'clientId': customer_id,
        'apiKey': api_key,
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

    code, message = requests_lib.send_get_request(url, payload)

    if code == -1:
        logger.error('Error occurred while sending GET request: {0}'.format(message))
        return -1

    try:
        answer = json.loads(message)
    except ValueError:
        err_message = 'Can not decode json.'
        logger.exception(err_message)
        return 1
    else:
        try:
            vm_id = answer['result']
            operation_id = answer['operationId']
        except KeyError:
            print 'Received invalid response, exiting...'
            logger.exception('Can not get vm_id or operation_id from responses json.')
            return 1
        except Exception:
            print 'Unknown Error, exiting...'
            logger.exception('Error occurred while parsing response json.')
            return -1

    if type(vm_id) != int:
        logger.error('Invalid vm_id.')
        sys.exit(1)
    elif type(operation_id) != int:
        logger.error('Invalid operation_id.')
        sys.exit(1)

    logger.debug('Response is received:\nCode: {0}\nMessage: {1}'.format(code, message))

    if raw:
        print message
    else:
        print_result(answer, ['result', 'operationId'])

    code, message = wait_for_async_answer(api_key=api_key, customer_id=customer_id, raw=True, operation_id=operation_id,
                                          url=url)

    if code == 0:
        logger.info('Operation with ID {0} is finished. Virtual machine {1} is created.'.format(operation_id, name))
        # Get server-list for determine vm ID.
        code, message = get_created_vm_info(name, api_key, customer_id)

        if code == 0:
            with open('created_vm', 'w') as f:
                f.write('vm_name {0}\n'.format(name))
                f.write('ip {0}\n'.format(message['ip']))
                f.write('id {0}\n'.format(message['id']))
            return 0
        else:
            logger.info(message)
            return -1, message
    else:
        logger.info(
                'Operation with ID {0} is NOT finished. Virtual machine {1} is NOT created. '
                'Reason: {2}'.format(operation_id, name, message)
        )
        return 1


def start_server(vm_id, tenant_id, api_key=None, customer_id=None, raw=False):
    url = '{0}vm/[vmId]/start/'.format(helpers.api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key, 'tenantId': tenant_id}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    try:
        status = answer['status']
    except KeyError:
        err_message = 'No key "status" in response json.'
        logger.exception(err_message)
        return 2, err_message

    if status != 'OK':
        logger.info('Returned status is not "OK". Operation failed.')
        logger.debug('Response code: {0}, response message: {1}'.format(code, message))
        return 1, message
    else:
        try:
            operation_id = answer['operationId']
        except KeyError:
            err_message = 'No key "status" in response json.'
            logger.exception(err_message)
            return 2, err_message

    if raw:
        print message
    else:
        print_result(answer, ['operationId'])

    code, message = wait_for_async_answer(api_key=api_key, customer_id=customer_id, raw=True, operation_id=operation_id,
                                          url=url)

    if code == 0:
        logger.info('Operation with ID {0} is finished. Virtual machine started.'.format(operation_id))
        return 0, 'Virtual machine is successfully started.'
    else:
        logger.info(
                'Operation with ID {0} is NOT finished. Virtual machine is NOT started. '
                'Reason: {1}'.format(operation_id, message)
        )
        return 1, 'Virtual machine is not started.'


def add_pub_key(vm_id, tenant_id, key_ids=[], api_key=None, customer_id=None, raw=False):
    url = '{0}vm/[vmId]/pubkey_change/'.format(helpers.api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key, 'tenantId': tenant_id, 'keyIds': key_ids}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_result(answer, ['operationId'])


def delete_vm(vm_id=None, tenant_id=None, api_key=None, customer_id=None, raw=False):
    url = '{0}vm/{1}/delete'.format(helpers.api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    # Getting info in raw(json) format.
    info_url = '{0}vm/{1}/'.format(helpers.api_link, vm_id)
    info = get_info(api_key=api_key, customer_id=customer_id, raw=True, url=info_url)

    try:
        status = info['status']
    except KeyError:
        error_message = 'No key "status" found.'
        logger.exception(error_message)
        return 1, error_message

    if status != 'OK':
        logger.info('Can not get virtual server name to check. Not deleting VM.')
        return 1, 'Can not get virtual server name to check. VM is NOT deleted.'
    else:
        vm_name = info['result']['name']

    if inflo_delete_key in vm_name:
        logger.info('Inflo delete key is found. Deleting vm...')
    else:
        logger.info('Inflo delete key is not found. Not deleting vm...')
        return 0, 'No delete key in VM name. VM is NOT deleted.'

    payload = {'clientId': customer_id, 'apiKey': api_key, 'tenantId': tenant_id}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    if raw:
        print message
    else:
        print_result(answer, ['operationId'])

    return 0, 'VM is successfully deleted.'


####################


if __name__ == '__main__':
    pass
