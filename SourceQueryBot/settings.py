class Server:
    def __init__(self, ip: str, port: int = 27015,
                 alt_name: str = None) -> None:
        """
        Handles server settings.

        Paramters
        ---------
        ip: str
            IP address of server.
        port: int
            Port of server, defaults to 27015.
        alt_name: str
            Optionally set a name what will overwrite the servers name.
        """

        self.ip = ip
        self.port = port
        self.alt_name = alt_name


class Category:
    def __init__(self, name: str, channel: int,
                 servers: list, server_name_limit: int = 20) -> None:
        """
        Handles server commands.

        Paramters
        ---------
        name: str
            Name of category
        server_name_limit: int
            Limits how many characters the server name can be.
        channel: int
            Discord channel ID for this category.
        servers: list
            List of Server objects.
        """

        self.name = name
        self.server_name_limit = server_name_limit
        self.channel = channel
        self.servers = servers
