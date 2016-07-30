import json
import prettytable

import helpers
import requests_lib


api_link = 'https://api.flops.ru/api/v1/'


def get_tenant_info(api_key=None, customer_id=None):
    url = api_link + 'tenant'
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
    url = api_link + 'vm'
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
    url = api_link + 'distribution'
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


if __name__ == '__main__':
    pass
