import discord
from discord.ext import tasks

from settings import CONFIG
from translations import TRANSLATIONS

from utils.config import Config
from utils.server import Server
from utils.misc import Misc

class SourceQuery(discord.Client, Misc):
    sever_amount = -1
    config_cache = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if CONFIG["lang"] not in TRANSLATIONS:
            raise Exception("Translation doesn't exist")

        self.TRANSLATIONS = TRANSLATIONS[CONFIG["lang"]]
        self.CONFIG = CONFIG

        self.config = Config(obj=self)
        self.server = Server(obj=self)

        self.query_task.start()

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def close(self):
        self.query_task.cancel()

    @tasks.loop(seconds=CONFIG["refresh_rate"])
    async def query_task(self):
        await self.server.format_message()

    @query_task.before_loop
    async def before_query_task(self):
        await self.wait_until_ready()

        try:
            await self.config.load()
        except Exception as error:
            self.config_error(error)

        self.config.cache()
