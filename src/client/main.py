import datetime
import logging
import pprint

import click

from client.balance import get_balances
from client.errors import UserError, RfqHasExpired, APIException
from client.rfq import get_rfq

log = logging.getLogger(__name__)


def user_validate(rfq):
    """Allow the user to accept or abbort the trade"""
    pprint.pprint(rfq.json)
    raw_input("Press return to accept this trade or CTRL-C to cancel.")
    return rfq


def post_user_validate(rfq):
    """Automatically abort the trade if the user has taken too long."""
    if rfq.is_valid_for_time(datetime.datetime.now()):
        return rfq
    raise RfqHasExpired()


def display_result(trade_result):
    log.info("Trade has been executed.")

    print("Trading result:")

    pprint.pprint(trade_result.json)


def display_balances(param):
    print("Fetching balances:")

    pprint.pprint(get_balances().json)


@click.command("Trading Tool")
@click.option("--instrument", default="BTCUSD", help="Which instrument do you want to trade?")
@click.option("--qty", default=0.001, help="How many units to trade?")
@click.option("--side", default="buy", help="buy / sell")
def main(instrument, qty, side):
    if side not in ["buy", "sell"]:
        raise UserError("Invalid side: %s" % side)

    if qty < 0:
        raise UserError("Cannot trade negative quantity")

    try:
        display_result(user_validate(get_rfq(instrument, qty, side)).get_trade().execute())
        display_balances(get_balances())
    except APIException as apie:
        log.critical("Trade failed: %s" % apie[0])



if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.INFO)
    main()