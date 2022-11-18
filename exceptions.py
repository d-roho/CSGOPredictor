# List of Custom Exceptions used to capture known potential errors\t


class Error(Exception):
    # Base class for other exceptions
    pass


class EmptyServer(Error):
    # Raised when server has a population of zero
    pass


class MatchNotStarted(Error):
    # Raised when user is not currently spectating a Match (usually occurs when they've just exited out of a match)
    pass


class WarmUp(Error):
    # Raised when match is in "Warm Up" phase (usually occurs when user changes from one match to another (which is in Warm Up phase))
    pass
