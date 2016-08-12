import json
import logging

import prettytable
import sys

import helpers
import requests_lib

api_link = 'https://api.flops.ru/api/v1/'
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
def get_tenant_info(api_key=None, customer_id=None):
    url = '{0}tenant/'.format(api_link)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    print_info(answer, ['id', 'description'])


def server_list(api_key=None, customer_id=None, raw=False):
    url = '{0}vm/'.format(api_link)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    if raw:
        print message
    else:
        print_info(answer, ['id', 'name', 'memory', 'disk', 'cpu', 'ipAddresses', ('2', 'distribution', 'name')])


def os_list(api_key=None, customer_id=None):
    url = '{0}distribution/'.format(api_link)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name', 'description', 'bitness'])


def get_vm_info(vm_id, api_key=None, customer_id=None, raw=False):
    url = '{0}vm/{1}/'.format(api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    if raw:
        print message
        return message
    else:
        print_info(answer, ['id', 'name', 'cpu', 'memory', 'disk', 'bandwidth', 'ipAddresses', 'privateIpAddress',
                            'state', 'timeAdded', (2, 'distribution', 'name')])


def get_vm_snapshots(api_key=None, customer_id=None, vm_id=str):
    url = '{0}vm/{1}/snapshots/'.format(api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name', 'description', 'bitness', 'parentSnapshotId', 'timeAdded'])


def get_vm_backups(api_key=None, customer_id=None, vm_id=str):
    url = '{0}vm/{1}/backups/'.format(api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'size', 'timeAdded'])


def get_pubkeys(api_key=None, customer_id=None, raw=False):
    url = '{0}pubkeys/'.format(api_link)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    if raw:
        print message
    else:
        print_info(answer, ['id', 'name', 'type', 'publicKey', 'timeAdded'])


def get_software(api_key=None, customer_id=None):
    url = '{0}software/'.format(api_link)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name'])


def get_tariffs(api_key=None, customer_id=None):
    url = '{0}tariffs/'.format(api_link)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name', 'memory', 'disk', 'cpu', 'ipCount', 'onDemand', 'forWindows'])
#########################


# Action functions #
def create_vm(name, tenant_id, distr_id, tariff_id, memory, disk, cpu, ip_count, password, send_password,
              open_support_access, public_key_id, software_id, api_key=None, customer_id=None):
    url = '{0}vm/install/'.format(api_link)
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
    logger.debug('Response is received:\nCode: {0}\nMessage: {1}'.format(code, message))

    print_result(answer, ['result', 'operationId'])


def start_server(vm_id, tenant_id, api_key=None, customer_id=None):
    url = '{0}vm/[vmId]/start/'.format(api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key, 'tenantId': tenant_id}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_result(answer, ['operationId'])


def add_pub_key(vm_id, tenant_id, key_ids, api_key=None, customer_id=None):
    url = '{0}vm/[vmId]/pubkey_change/'.format(api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key, 'tenantId': tenant_id}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_result(answer, ['operationId'])


def delete_vm(vm_id, tenant_id, api_key=None, customer_id=None):
    url = '{0}vm/{1}/delete'.format(api_link, vm_id)
    if api_key in [None, ''] or customer_id in [None, '']:
        api_key, customer_id = helpers.get_conf()

    # Getting info in raw(json) format.
    info_raw = get_vm_info(vm_id, api_key=api_key, customer_id=customer_id, raw=True)
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

    print_result(answer, ['operationId'])
####################

if __name__ == '__main__':   
    pass
