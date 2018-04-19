import logging

log = logging.getLogger(__name__)


def get_auth_headers():
    # Normally we don't hard-code tokens, but I'm in a hurry
    api_token = '9b64727ad991138525752c3ec17da5073e508fa3'
    return {'Authorization': 'Token %s' % api_token}