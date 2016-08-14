import getpass
import json
import logging

import simplecrypt
import sys

logger = logging.getLogger(__name__)
filename = 'inflo.secret'
api_link = 'https://api.flops.ru/api/v1/'


def str_check(str_assume, str_mean):
    """Function performes check if variable is string or can be converted to string.

    Args:
        str_assume: Variable, that assumed to be a string.
        str_mean(string): What is str_assume mean.

    Returns:
        Same string, if str_assume is string.
        str_for_sure if str_assume could be safely converted to string, raises ValueError if not.
    """
    if type(str_assume) is not str:
        try:
            str_for_sure = str(str_assume)
        except Exception as e:
            raise ValueError('{0} must be string.'.format(str_mean))
        else:
            logger.debug('{0} converted to string successfully.'.format(str_assume))
            return str_for_sure
    else:
        return str_assume


def set_conf(ext_api=None, ext_id=None):
    if ext_api is None and ext_id is None:
        logger.debug('API and ID is none, nothing to do...')
        print 'No API or ID specified, exiting...'
        sys.exit(0)

    api = str_check(ext_api, 'API key')
    cust_id = str_check(ext_id, 'Customer ID')

    # Safely get password and encrypt API key and customer ID to save in temp file.
    password = getpass.getpass('Please type password to protect your API key and customer ID: ')

    js = '{{"api": "{0}", "id": "{1}"}}'.format(api, cust_id)
    encr_js = simplecrypt.encrypt(password, js)

    with open(filename, 'wb') as f:
        f.write(encr_js)

    logger.debug('API and ID successfully encrypted and stored to file.')


def get_conf():
    password = getpass.getpass('Enter password:')

    with open(filename, 'rb') as f:
        try:
            encr_js = f.read()
            decr_js = simplecrypt.decrypt(password, encr_js)
            logger.debug('Fresh decrypted string: {0}'.format(decr_js))

            js = decr_js.decode('utf8')
            logger.debug('Decoded JSON is {0}'.format(js))

            js_dict = json.loads(js)
            api = js_dict['api']
            cust_id = js_dict['id']
        except Exception as e:
            logger.debug('Error occurred while decrypting API and ID: {0}'.format(e))
            print 'Wrong password, sorry dude... bye!'
            sys.exit(0)
        else:
            return api, cust_id


if __name__ == '__main__':
    pass
