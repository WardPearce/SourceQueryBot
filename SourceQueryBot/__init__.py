import discord
from discord.ext import tasks

from .translations import TranslationBase, English
from .messages import Messages


__version__ = "0.0.1"


class SourceQueryBot(discord.Client):
    refresh_rate = 0.0

    def __init__(self, catagories: list, refresh_rate: float = 30.0,
                 lanague: TranslationBase = English,
                 messages: Messages = Messages(),
                 *args, **kwargs):
        """
        Pass any discord bot client args / paramters.

        Paramters
        ---------
        refresh_rate: int
            How many seconds to refresh, defaults to 30.
        lanague: TranslationBase
            Defaults to english.
        messages: Messages
            Handles message caching.
        """

        self.lanague = lanague
        self.refresh_rate = refresh_rate

        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(self.lanague.on_ready.format(self.user))

    async def close(self):
        print(self.lanague.shutdown)
        self.query_task.cancel()

    @tasks.loop(seconds=refresh_rate)
    async def query_task(self):
        pass

    @query_task.before_loop
    async def before_query_task(self):
        pass
