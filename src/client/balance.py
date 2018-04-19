import json

import requests

from client.auth import get_auth_headers
from client.query import validate_response


class Balances:

    def __init__(self, json):
        self.json = json

def get_balances():
    response = validate_response(requests.get('https://sandboxapi.b2c2.net/balance/', headers=get_auth_headers()), expected_status=200)
    return Balances(json.loads(response.text))