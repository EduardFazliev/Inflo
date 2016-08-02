import json
import prettytable

import helpers
import requests_lib

api_link = 'https://api.flops.ru/api/v1/'


def print_out(answer, headers):
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


def get_tenant_info(api_key=None, customer_id=None):
    url = '{0}/tenant/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    print_out(answer, ['id', 'description'])


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
        print_out(answer, ['id', 'name', 'memory', 'disk', 'cpu', 'ipAddresses', (2, 'distribution', 'name')])


def os_list(api_key=None, customer_id=None):
    url = '{0}/distribution/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_out(answer, ['id', 'name', 'description', 'bitness'])


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
        print_out(answer, ['id', 'name', 'cpu', 'memory', 'disk', 'bandwidth', 'ipAddresses', 'privateIpAddresses',
                           'state', 'timeAdded', (2, 'distribution', 'name')])


def get_vm_snapshots(api_key=None, customer_id=None, vm_id=str):
    url = '{0}/vm/{1}/snapshots/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_out(answer, ['id', 'name', 'description', 'bitness', 'parentSnapshotId', 'timeAdded'])


def get_vm_backups(api_key=None, customer_id=None, vm_id=str):
    url = '{0}/vm/{1}/backups/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_out(answer, ['id', 'size', 'timeAdded'])


def get_pubkeys(api_key=None, customer_id=None):
    url = '{0}/pubkeys/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_out(answer, ['id', 'name', 'type', 'publicKey', 'timeAdded'])


def get_software(api_key=None, customer_id=None):
    url = '{0}/software/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_out(answer, ['id', 'name'])


def get_tariffs(api_key=None, customer_id=None):
    url = '{0}/tariffs/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print_out(answer, ['id', 'name', 'memory', 'disk', 'cpu', 'ipCount', 'onDemand', 'forWindows'])


if __name__ == '__main__':
    pass
