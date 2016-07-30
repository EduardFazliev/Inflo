import logging
import requests
from requests.auth import HTTPBasicAuth


logger = logging.getLogger(__name__)


def send_post_request(self, url, payload):
    """Sends post request with spec header.
    Args:
        url (str): API URL to send comment.
        payload (dict): json to send.
    Returns:
        result.content (dict): Response content in json format.
        result.status_code (str): Response code.
    """
    result = (-42, "Unknown.")
    logger.debug('POST request: url: {0}, payload: {1}'.format(url, payload))
    try:
        response = requests.post(url, json=payload, headers={"X-Atlassian-Token": "no-check"},
                                 auth=HTTPBasicAuth(self.username, self.passwd))
    except Exception as e:
        logger.exception("Error occurred while sending POST request.")
        result = (-1, e)
    else:
        logger.debug('POST respond: status: {0}, content: {1}'.format(response.status_code, response.content))
        result = response.status_code, response.content

    return result


def send_put_request(self, url, payload):
    """Sends put request with spec header.
    Args:
        url (str): API URL to send comment.
        payload (dict): json to send.
    Returns:
        result.content (dict): Response content in json format.
        result.status_code (str): Response code.
    """
    result = (-42, "Unknown.")
    logger.debug('PUT request: url: {0}, payload: {1}'.format(url, payload))
    try:
        response = requests.put(url, json=payload, headers={"X-Atlassian-Token": "no-check"},
                                auth=HTTPBasicAuth(self.username, self.passwd))
    except Exception as e:
        logger.exception("Error occurred while sending PUT request.")
        result = (-1, e)
    else:
        logger.debug('PUT respond: status: {0}, content: {1}'.format(response.status_code, response.content))
        result = (response.status_code, response.content)
    finally:
        return result


def send_get_request(url, payload):
    """Sends get request with spec header.
    Args:
        url (str): API URL to send comment.
        payload (dict): json to send.
    Returns:
        result.content (dict): Response content in json format.
        result.status_code (str): Response code.
    """
    logger.debug('GET request: url: {0}, payload: {1}'.format(url, payload))
    try:
        response = requests.get(url, params=payload)
    except Exception as e:
        logger.exception("Error occurred while sending GET request.")
        return -1, e
    else:
        logger.debug('GET respond: status: {0}, content: {1}'.format(response.status_code, response.content))
        return response.status_code, response.content
