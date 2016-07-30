import getpass
import logging

import simplecrypt
import sys

logger = logging.getLogger(__name__)
filename = 'inflo.secret'


def str_check(str_assume, str_mean):
    """Functions performes check if variable is string or can be converted to string.

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


def set_conf(ext_api, ext_id):
    api = str_check(ext_api, 'API key')
    cust_id = str_check(ext_id, 'Customer ID')

    # Safely get password and encrypt API key and customer ID to save in temp file.
    password = getpass.getpass('Please type password to protect your API key and customer ID.')

    encr_api = simplecrypt.encrypt(password, api)
    encr_id = simplecrypt.encrypt(password, cust_id)
    with open(filename, 'w') as f:
        f.write(encr_api)
        f.write(encr_id)
    logger.debug('API and ID successfully encrypted and stored to file.')


def get_conf():
    password = getpass.getpass('Enter password:')

    with open(filename, 'r') as f:
        try:
            api = simplecrypt.decrypt(password, f.readline())
            cust_id = simplecrypt.decrypt(password, f.readline())
        except Exception as e:
            logger.debug('Error occured while decrypting API and ID: {0}'.format(e))
            print 'Wrong password, sorry dude... bye!'
            sys.exit(0)
        else:
            return api, cust_id


if __name__ == '__main__':
    pass
