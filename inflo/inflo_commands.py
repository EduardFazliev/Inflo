import json
import prettytable

import helpers
import requests_lib

api_link = 'https://api.flops.ru/api/v1/'


def get_tenant_info(api_key=None, customer_id=None):
    url = '{0}/tenant/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    print '''
    Status: {0}
    ++++++++++++++++++++
    '''.format(answer['status'])

    pt = prettytable.PrettyTable()

    result = answer['result']
    pt.add_column('id', [tenant['id'] for tenant in result])
    pt.add_column('description', [tenant['description'] for tenant in result])

    print pt


def server_list(api_key=None, customer_id=None, raw=False):
    url = '{0}/vm/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    print '''
    Status: {0}
    ++++++++++++++++++++
    '''.format(answer['status'])

    if not raw:
        pt = prettytable.PrettyTable()
        result = answer['result']

        pt.add_column('id', [server['id'] for server in result])
        pt.add_column('name', [server['name'] for server in result])
        pt.add_column('memory', [server['memory'] for server in result])
        pt.add_column('disk', [server['disk'] for server in result])
        pt.add_column('cpu', [server['cpu'] for server in result])
        pt.add_column('ip', [server['ipAddresses'] for server in result])
        pt.add_column('os', [server['distribution']['name'] for server in result])

        print pt
    else:
        print message


def os_list(api_key=None, customer_id=None):
    url = '{0}/distribution/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    answer = json.loads(message)

    print '''
    -> Status: {0}
    -> Printing result...
    '''.format(answer['status'])

    pt = prettytable.PrettyTable()
    result = answer['result']

    pt.add_column('id', [server['id'] for server in result])
    pt.add_column('name', [server['name'] for server in result])
    pt.add_column('description', [server['description'] for server in result])
    pt.add_column('bitness', [server['bitness'] for server in result])

    print pt


def get_vm_info(api_key=None, customer_id=None, vm_id=str, raw=False):
    url = '{0}/vm/{1}/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print '''
    -> Status: {0}
    -> Printing result...
    '''.format(answer['status'])

    if not raw:

        pt = prettytable.PrettyTable()
        result = answer['result']

        pt.add_column('id', [server['id'] for server in result])
        pt.add_column('name', [server['name'] for server in result])
        pt.add_column('cpu', [server['cpu'] for server in result])
        pt.add_column('memory', [server['memory'] for server in result])
        pt.add_column('disk', [server['disk'] for server in result])
        pt.add_column('bandwidth', [server['bandwidth'] for server in result])
        pt.add_column('ipAddresses', [server['ipAddresses'] for server in result])
        pt.add_column('privateIpAddress', [server['privateIpAddress'] for server in result])
        pt.add_column('state', [server['state'] for server in result])
        # TODO: Convert Unix time to standard one.
        pt.add_column('timeAdded', [server['timeAdded'] for server in result])
        pt.add_column('distribution', [server['distribution'] for server in result])

    else:
        print message


def get_vm_snapshots(api_key=None, customer_id=None, vm_id=str):
    url = '{0}/vm/{1}/snapshots/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print '''
    -> Status: {0}
    -> Printing result...
    '''.format(answer['status'])

    pt = prettytable.PrettyTable()
    result = answer['result']

    pt.add_column('id', [server['id'] for server in result])
    pt.add_column('name', [server['name'] for server in result])
    pt.add_column('description', [server['description'] for server in result])
    pt.add_column('parentSnapshotId', [server['parentSnapshotId'] for server in result])
    # TODO: Convert Unix time to standard one.
    pt.add_column('timeAdded', [server['timeAdded'] for server in result])


def get_vm_backups(api_key=None, customer_id=None, vm_id=str):
    url = '{0}/vm/{1}/backups/'.format(api_link, vm_id)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print '''
    -> Status: {0}
    -> Printing result...
    '''.format(answer['status'])

    pt = prettytable.PrettyTable()
    result = answer['result']

    pt.add_column('id', [server['id'] for server in result])
    pt.add_column('size', [server['size'] for server in result])
    # TODO: Convert Unix time to standard one.
    pt.add_column('timeAdded', [server['timeAdded'] for server in result])


def get_pubkeys(api_key=None, customer_id=None):
    url = api_link + 'pubkeys'
    url = '{0}/pubkeys/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print '''
    -> Status: {0}
    -> Printing result...
    '''.format(answer['status'])

    pt = prettytable.PrettyTable()
    result = answer['result']

    pt.add_column('id', [server['id'] for server in result])
    pt.add_column('name', [server['name'] for server in result])
    pt.add_column('type', [server['type'] for server in result])
    pt.add_column('publicKey', [server['publicKey'] for server in result])
    # TODO: Convert Unix time to standard one.
    pt.add_column('timeAdded', [server['timeAdded'] for server in result])


def get_software(api_key=None, customer_id=None):
    url = '{0}/software/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print '''
    -> Status: {0}
    -> Printing result...
    '''.format(answer['status'])

    pt = prettytable.PrettyTable()
    result = answer['result']

    pt.add_column('id', [server['id'] for server in result])
    pt.add_column('name', [server['name'] for server in result])


def get_tariffs(api_key=None, customer_id=None):
    url = '{0}/tariffs/'.format(api_link)
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientID': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)
    answer = json.loads(message)

    print '''
    -> Status: {0}
    -> Printing result...
    '''.format(answer['status'])

    pt = prettytable.PrettyTable()
    result = answer['result']

    pt.add_column('id', [server['id'] for server in result])
    pt.add_column('name', [server['name'] for server in result])
    pt.add_column('memory', [server['memory'] for server in result])
    pt.add_column('disk', [server['disk'] for server in result])
    pt.add_column('cpu', [server['cpu'] for server in result])
    pt.add_column('ipCount', [server['ipCount'] for server in result])
    pt.add_column('onDemand', [server['onDemand'] for server in result])
    pt.add_column('forWindows', [server['forWindows'] for server in result])


if __name__ == '__main__':
    pass
