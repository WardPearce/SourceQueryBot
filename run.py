import discord
import asyncio

from settings import CONFIG
from aioquery import aioquery

class SourceQueryBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.query_task())

    def config_error(self, message):
        print("[WARNING]: {}".format(message))

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def query_task(self):
        await self.wait_until_ready()

        config_cache = {}
        for name, values in CONFIG["servers"].items():
            if values.get("channel") and values.get("servers"):
                channel = self.get_channel(values["channel"])

                if channel != None:
                    config_cache[name] = {
                        "channel": channel,
                        "servers": [],
                    }

                    for server in values["servers"]:
                        ip_port = server.split(":")

                        config_cache[name]["servers"].append(aioquery(ip_port[0], int(ip_port[1])))
                else:
                    self.config_error("Unable to pull channel with ID {}.".format(values["channel"]))
            else:
                self.config_error("Unable to pull [{}], no channel, servers or players given.".format(name))

        while not self.is_closed():
            for name, values in config_cache.items():
                embed = discord.Embed(title="__**{}**__".format(name), colour=discord.Colour(CONFIG["bot"]["embed_color"]))

                for server in values["servers"]:
                    server_info = await server.get_info()

                    if server_info != False:
                        embed.add_field(name=server_info["hostname"][:CONFIG["servers"][name]["char_limit"]], value="**Map:** {}\n**Players:** {}/{}\n**Connect:**\nsteam://connect/{}:{}".format(
                            server_info["map"], 
                            server_info["players"],
                            server_info["max_players"],
                            server.ip,
                            server.port,
                        ), inline=False)

                    if values.get("msg"):
                        try:
                            await values["msg"].edit(embed=embed)
                        except:
                            self.config_error("Couldn't edit {}".format(values["msg"].id))
                    else:
                        try:
                            config_cache[name]["msg"] = await values["channel"].send(embed=embed)
                        except:
                            self.config_error("Couldn't message {}".format(values["channel"].id))
            
            await asyncio.sleep(CONFIG["refresh_rate"])


client = SourceQueryBot()
client.run(CONFIG["bot"]["token"])
