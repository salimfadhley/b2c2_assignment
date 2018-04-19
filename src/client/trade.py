import json
import logging

import requests

from client.auth import get_auth_headers
from client.query import validate_response
from client.trade_result import TradeResult

log = logging.getLogger(__name__)


class Trade():

    def __init__(self, rfq):
        self.rfq = rfq


    def execute(self):
        log.info("Executing trade.")


        post_data = {
            'instrument': self.rfq.instrument,
            'side': self.rfq.side,
            'quantity': self.rfq.quantity,
            'price': self.rfq.price,
            'rfq_id': self.rfq.rfq_id
        }

        response = validate_response(requests.post('https://sandboxapi.b2c2.net/trade/', json=post_data, headers=get_auth_headers()))

        return TradeResult(json.loads(response.text))

