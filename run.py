import discord
import aiofiles
import asyncio
import os

from settings import CONFIG
from aioquery import aioquery

class SourceQueryBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.loop.create_task(self.query_task())

    def config_error(self, message):
        print("[WARNING]: {}".format(message))

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def query_task(self):
        await self.wait_until_ready()

        if os.path.isfile(CONFIG["message_ids"]):
            async with aiofiles.open(CONFIG["message_ids"]) as f:
                async for line in f:
                    channel_msg = line.split(":")

                    channel = self.get_channel(int(channel_msg[0]))
                    if channel != None:
                        msg = await channel.fetch_message(int(channel_msg[1]))
                        if msg != None:
                            await msg.delete()
        
        writer_close = False
        message_id_save = await aiofiles.open(CONFIG["message_ids"], mode="w")

        config_cache = {}
        for name, values in CONFIG["servers"].items():
            if values.get("channel") and values.get("servers"):
                channel = self.get_channel(values["channel"])

                if channel != None:
                    config_cache[name] = {
                        "channel": channel,
                        "servers": [],
                    }

                    for server in values["servers"].keys():
                        ip_port = server.split(":")

                        config_cache[name]["servers"].append(aioquery(ip_port[0], int(ip_port[1])))
                else:
                    self.config_error("Unable to pull channel with ID {}.".format(values["channel"]))
            else:
                self.config_error("Unable to pull [{}], no channel, servers or players given.".format(name))

        while not client.is_closed():
            for name, values in config_cache.items():
                embed = discord.Embed(title="__**{}**__".format(name), colour=discord.Colour(CONFIG["bot"]["embed_color"]))

                for server in values["servers"]:
                    ip_port = "{}:{}".format(server.ip, server.port)

                    server_info = await server.get_info()

                    if server_info != False:
                        if CONFIG["servers"][name]["servers"][ip_port] == False:
                            server_name = server_info["hostname"][:CONFIG["servers"][name]["char_limit"]]
                        else:
                            server_name = CONFIG["servers"][name]["servers"][ip_port]

                        embed.add_field(name=server_name, value="**Map:** {}\n**Players:** {}/{}\n**Connect:**\nsteam://connect/{}".format(
                            server_info["map"], 
                            server_info["players"],
                            server_info["max_players"],
                            ip_port
                        ), inline=False)

                if values.get("msg"):
                    try:
                        await values["msg"].edit(embed=embed)
                    except:
                        self.config_error("Couldn't edit {}".format(values["msg"]))
                else:
                    try:
                        config_cache[name]["msg"] = await values["channel"].send(embed=embed)
                        
                        if writer_close == False:
                            await message_id_save.write("{}:{}\n".format(values["channel"].id, config_cache[name]["msg"].id))
                    except:
                        self.config_error("Couldn't message {}".format(values["channel"]))

                await asyncio.sleep(1)

            if writer_close == False:
                writer_close = True
                await message_id_save.close()

            await asyncio.sleep(CONFIG["refresh_rate"])


client = SourceQueryBot()
client.run(CONFIG["bot"]["token"])
