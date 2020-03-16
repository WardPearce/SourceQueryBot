import discord
from discord.ext import tasks
import aiofiles
import asyncio
import os

from settings import CONFIG
from translations import TRANSLATIONS
from aioquery import aioquery

if CONFIG["lang"] not in TRANSLATIONS:
    raise Exception("Translation doesn't exist")

TRANSLATIONS = TRANSLATIONS[CONFIG["lang"]]

class SourceQueryBot(discord.Client):
    sever_amount = -1
    presence_completed = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query_task.start()

    def config_error(self, message):
        print("[WARNING]: {}".format(message))

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def close(self):
        self.query_task.cancel()

    async def smart_presence(self, players, max_players, map, loop_index):
        if loop_index == self.sever_amount:
            self.presence_completed = False
            print("presence_completed false")

        sleep = loop_index * 10

        await asyncio.sleep(sleep)

        await self.change_presence(status=discord.Status.online, activity=discord.Game(TRANSLATIONS["smart_presence"].format(
            players,
            max_players,
            map
        )))

        if loop_index == self.sever_amount:
            self.presence_completed = True

    @tasks.loop(seconds=CONFIG["refresh_rate"])
    async def query_task(self):
        total_players = 0
        total_max_players = 0

        loop_index = -1

        for name, values in self.config_cache.items():
            embed = discord.Embed(title=TRANSLATIONS["title"].format(name), colour=discord.Colour(CONFIG["bot"]["embed_color"]))

            for server in values["servers"]:
                loop_index += 1

                ip_port = "{}:{}".format(server.ip, server.port)

                server_info = await server.get_info()

                if server_info != False:
                    if CONFIG["servers"][name]["servers"][ip_port] == False:
                        server_name = server_info["hostname"][:CONFIG["servers"][name]["char_limit"]]
                    else:
                        server_name = CONFIG["servers"][name]["servers"][ip_port]

                    embed.add_field(name=server_name, value=TRANSLATIONS["successful"].format(
                        server_info["map"], 
                        server_info["players"],
                        server_info["max_players"],
                        ip_port
                    ), inline=False)

                    if CONFIG["smart_presence"]:
                        if self.presence_completed:
                            asyncio.create_task(self.smart_presence(players=server_info["players"], max_players=server_info["max_players"],
                                                                    map=server_info["map"], loop_index=loop_index))
                    else:
                        total_players += server_info["players"]
                        total_max_players += server_info["max_players"]
                else:
                    if CONFIG["servers"][name]["servers"][ip_port] == False:
                        server_name = TRANSLATIONS["fail_title"]
                    else:
                        server_name = CONFIG["servers"][name]["servers"][ip_port]

                    embed.add_field(name=server_name, value=TRANSLATIONS["fail"], inline=False)

                await asyncio.sleep(0.5)

            if values.get("msg"):
                try:
                    await values["msg"].edit(embed=embed)
                except Exception as error:
                    self.config_error("Couldn't edit {}\n\nError\n{}".format(values["msg"], error))
            else:
                try:
                    self.config_cache[name]["msg"] = await values["channel"].send(embed=embed)
                    
                    if self.writer_close == False:
                        await self.message_id_save.write("{}:{}\n".format(values["channel"].id, self.config_cache[name]["msg"].id))

                except Exception as error:
                    self.config_error("Couldn't message {}\n\nError\n{}".format(values["channel"], error))

            await asyncio.sleep(0.5)

        if CONFIG["smart_presence"] == False:
            await self.change_presence(status=discord.Status.online, activity=discord.Game(TRANSLATIONS["total_players"].format(total_players, total_max_players)))

        if self.writer_close == False:
            self.writer_close = True
            await self.message_id_save.close()

    @query_task.before_loop
    async def before_query_task(self):
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
        
        self.writer_close = False
        self.message_id_save = await aiofiles.open(CONFIG["message_ids"], mode="w")

        self.config_cache = {}
        for name, values in CONFIG["servers"].items():
            if values.get("channel") and values.get("servers"):
                channel_obj = self.get_channel(values["channel"])

                if channel_obj != None:
                    self.config_cache[name] = {
                        "channel": channel_obj,
                        "servers": [],
                    }

                    for server in values["servers"].keys():
                        self.sever_amount += 1

                        ip_port = server.split(":")
                        self.config_cache[name]["servers"].append(aioquery(ip_port[0], int(ip_port[1])))
                else:
                    self.config_error("Unable to pull channel with ID {}.".format(values["channel"]))
            else:
                self.config_error("Unable to pull [{}], no channel, servers or players given.".format(name))

client = SourceQueryBot()
client.run(CONFIG["bot"]["token"])
