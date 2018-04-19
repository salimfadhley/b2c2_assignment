import json
import logging

from client.errors import APIException

log = logging.getLogger(__name__)


def validate_response(response, expected_status=201):
    """
    Validate that we got a 201, or blow up.
    """
    if response.status_code != expected_status:
        for error in json.loads(response.text)["errors"]:
            log.critical("{code}: {message}".format(**error))
        raise APIException("%i" % (response.status_code))

    return response