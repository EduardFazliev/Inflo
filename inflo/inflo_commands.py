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

    return message


def wait_for_async_answer(api_key=None, customer_id=None, raw=True, url=None, operation_id=None):
    logger.debug('URL for operation request is {0}.'.format(url))

    pb = fish.ProgressFish(total=100)

    while True:
        response = get_info(api_key=api_key, customer_id=customer_id, raw=raw, url=url)

        # Get result and load it in 'info' dictionary.
        try:
            info_common = json.loads(response)
            info = info_common['result']
        except KeyError:
            logger.exception('No "result" key in response json.')

        # If error occurred - return error code and error message.
        try:
            if info['errorMessage'] is not None:
                return -1, info['errorMessage']
        except KeyError:
            logger.exception('No "errorMessage" key in response json.')

        # If percentage is equal 100 and status is "DONE" - return
        # success code and 'info' dictionary.
        try:
            if info['percentage'] in ('100', 100) and info['status'] == 'DONE':
                logger.debug('Operation with ID {0} is finished.'.format(operation_id))
                return 0, info
        except KeyError:
            logger.exception('No "percentage" or "status" key in response json.')

        # Show current progress with "fish" progress bar.
        print type(info['percentage'])
        pb.animate(amount=info['percentage'])
        time.sleep(1)


# Action functions #
def create_vm(name, tenant_id, distr_id, tariff_id, memory, disk, cpu, ip_count, password, send_password,
              open_support_access, public_key_id, software_id, api_key=None, customer_id=None, raw=False, id_only=False):
    url = '{0}vm/install/'.format(helpers.api_link)
    logger.debug('URL for create-vm: {0}'.format(url))
    if api_key in [None, ''] or customer_id in [None, '']:
        logger.debug('API key and customer ID is not provided, so trying to get them from file...')
        api_key, customer_id = helpers.get_conf()
    else:
        logger.debug('API key and customer ID provided.')

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
    answer = json.loads(message)
    try:
        vm_id = answer['result']
        operation_id = answer['operationId']
    except KeyError:
        print 'Received invalid response, exiting...'
        logger.exception('Can not get vm_id or operation_id from responses json.')
        sys.exit(1)
    except Exception:
        print 'Unknown Error, exiting...'
        logger.exception('Error occurred while parsing response json.')
        sys.exit(1)

    if type(vm_id) != int:
        logger.error('Invalid vm_id.')
        sys.exit(1)
    elif type(operation_id) != int:
        logger.error('Invalid operation_id.')
        sys.exit(1)

    logger.debug('Response is received:\nCode: {0}\nMessage: {1}'.format(code, message))

    if id_only:
        print vm_id
    elif raw:
        print message
    else:
        print_result(answer, ['result', 'operationId'])

    url = 'operation/{0}/'.format(operation_id)
    code, message = wait_for_async_answer(api_key=api_key, customer_id=customer_id, raw=True, operation_id=operation_id,
                                          url=url)

    if code == 0:
        logger.info('Operation with ID {0} is finished. Virtual machine {1} is created.'.format(operation_id, name))
        return 0
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

    if raw:
        print message
    else:
        print_result(answer, ['operationId'])


def add_pub_key(vm_id, tenant_id, key_ids=[], api_key=None, customer_id=None, raw=False):
    url = '{0}vm/[vmId]/pubkey_change/'.format(helpers.api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key, 'tenantId': tenant_id, 'keyIds': key_ids}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_result(answer, ['operationId'])


def delete_vm(vm_id, tenant_id, api_key=None, customer_id=None, raw=False):
    url = '{0}vm/{1}/delete'.format(helpers.api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    # Getting info in raw(json) format.
    info_url = '{0}vm/{1}/'.format(helpers.api_link, vm_id)
    info_raw = get_info(api_key=api_key, customer_id=customer_id, raw=True, url=info_url)
    info = json.loads(info_raw)
    status = info['result']['name']
    if status != 'OK':
        print 'Can not get virtual server name to check. Not deleting VM.'
        sys.exit(0)
    else:
        vm_name = info['result']['name']

    if inflo_delete_key in vm_name:
        print 'Inflo delete key is found. Deleting vm...'
    else:
        print 'Inflo delete key is not found. Not deleting vm...'
        sys.exit(0)

    payload = {'clientId': customer_id, 'apiKey': api_key, 'tenantId': tenant_id}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    if raw:
        print message
    else:
        print_result(answer, ['operationId'])


####################


if __name__ == '__main__':
    pass
