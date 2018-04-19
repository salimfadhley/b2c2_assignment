import json
import logging
from uuid import uuid4

import requests
from iso8601 import iso8601

from client.errors import APIException
from client.auth import get_auth_headers
from client.query import validate_response
from client.trade import Trade


log = logging.getLogger(__name__)


class Rfq:
    def __init__(self, json):
        self.json = json

    def get_trade(self):
        return Trade(self)

    def get_valid_until(self):
        return iso8601.parse_date(self.json["valid_until"])

    def is_valid_for_time(self, dt):
        """Return true if the rfq is valid for the given datetime."""
        return dt < self.get_valid_until()

    @property
    def instrument(self):
        return self.get_value("instrument")

    @property
    def side(self):
        return self.get_value("side")

    @property
    def quantity(self):
        return self.get_value("quantity")

    @property
    def price(self):
        return self.get_value("price")

    @property
    def rfq_id(self):
        return self.get_value("rfq_id")

    def get_value(self, k):
        return self.json[k]


def get_rfq(instrument, quantity, side):

    post_data = {
        'instrument': instrument,
        'side': side,
        'quantity': quantity,
        'client_rfq_id': uuid4().urn
    }

    response = validate_response(requests.post('https://sandboxapi.b2c2.net/request_for_quote/', json=post_data, headers=get_auth_headers()))

    return Rfq(json.loads(response.text))