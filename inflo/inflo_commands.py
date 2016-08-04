import json
import prettytable

import helpers
import requests_lib

api_link = 'https://api.flops.ru/api/v1/'


def print_info(answer, headers):
    status = answer['status']
    result = answer['result']

    print '''
    #-#-#-#-#
    -> Status: {0}
    -> Result:
    '''.format(status)

    pt = prettytable.PrettyTable()
    for header in headers:
        if type(header) == tuple:
            if header[0] == 2:
                pt.add_column(header[2], [subject[header[1]][header[2]] for subject in result])
        else:
            pt.add_column(header, [subject[header] for subject in result])

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
        pt.add_column(answer[header])

    print pt


def get_tenant_info(api_key=None, customer_id=None):
    url = '{0}/tenant/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    print_info(answer, ['id', 'description'])


def server_list(api_key=None, customer_id=None, raw=False):
    url = '{0}/vm/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    if raw:
        print message
    else:
        print_info(answer, ['id', 'name', 'memory', 'disk', 'cpu', 'ipAddresses', (2, 'distribution', 'name')])


def os_list(api_key=None, customer_id=None):
    url = '{0}/distribution/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name', 'description', 'bitness'])


def get_vm_info(api_key=None, customer_id=None, vm_id=str, raw=False):
    url = '{0}/vm/{1}/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    if raw:
        print message
    else:
        print_info(answer, ['id', 'name', 'cpu', 'memory', 'disk', 'bandwidth', 'ipAddresses', 'privateIpAddresses',
                           'state', 'timeAdded', (2, 'distribution', 'name')])


def get_vm_snapshots(api_key=None, customer_id=None, vm_id=str):
    url = '{0}/vm/{1}/snapshots/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name', 'description', 'bitness', 'parentSnapshotId', 'timeAdded'])


def get_vm_backups(api_key=None, customer_id=None, vm_id=str):
    url = '{0}/vm/{1}/backups/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'size', 'timeAdded'])


def get_pubkeys(api_key=None, customer_id=None):
    url = '{0}/pubkeys/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name', 'type', 'publicKey', 'timeAdded'])


def get_software(api_key=None, customer_id=None):
    url = '{0}/software/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name'])


def get_tariffs(api_key=None, customer_id=None):
    url = '{0}/tariffs/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_info(answer, ['id', 'name', 'memory', 'disk', 'cpu', 'ipCount', 'onDemand', 'forWindows'])


def create_vm(name, tenant_id, distr_id, tariff_id, memory, disk, cpu, ip_count, password, send_password,
              open_support_access, public_key_id, software_id, api_key=None, customer_id=None):
    url = '{0}/vm/install/'.format(api_key)

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

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_result(answer, ['result', 'operationId'])


def delete_vm(vm_id, tenant_id, api_key=None, customer_id=None):
    url = '{0}/vm/{1}/delete'.format(api_link, vm_id)

    payload = {'tenantId': tenant_id}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_result(answer, ['operationId'])

if __name__ == '__main__':
    pass
