class APIError(Exception):
    """ Raised for API errors.

    Attributes :
        message : String detailing the error details
    """

    def __init__(self, message):
        self.message = message