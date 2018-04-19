class APIException(RuntimeError):
    """
    Something happened while querying the API
    """

class UserError(APIException):
    """
    User provided bogus data
    """

class UserAbort(APIException):
    """
    User decided not to proceed with the trade.
    """

class RfqHasExpired(APIException):
    """
    User took too long to accept the trade.
    """