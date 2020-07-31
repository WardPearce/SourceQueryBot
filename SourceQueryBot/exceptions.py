class NoSuchConfigFile(Exception):
    """
    Raised when config file doesn't exist.
    """

    pass


class InvalidChannel(Exception):
    """
    Raised when a channel ID is invalid or can't be accessed.
    """

    pass
