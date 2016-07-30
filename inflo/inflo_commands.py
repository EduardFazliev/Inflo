import helpers
import requests_lib

api_link = 'https://api.flops.ru/api/v1/'


def get_tenant_info(api_key=None, customer_id=None):
    url = api_link + 'tenant'
    if api_key or customer_id is None:
        api_key, customer_id = helpers.get_conf()

    payload = {'clientId': customer_id, 'apiKey': api_key}

    code, message = requests_lib.send_get_request(url, payload)

    if code != -1:
        print message


if __name__ == '__main__':
    pass
