import json
import os

import asyncio
import aiohttp

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot

with open("{}/config.json".format(os.path.dirname(os.path.realpath(__file__)))) as config_file:  
    config = json.load(config_file)

with open("{}/translations.json".format(os.path.dirname(os.path.realpath(__file__)))) as translations_file:  
    translations = json.load(translations_file)

language = config["general"]["language"]

if discord.version_info.major == 1:
    client = commands.Bot(command_prefix=config["general"]["prefix"])

    @client.event
    async def on_ready():
        print(translations[language]["connection-successful"].format(client, config["general"]["community-name"], discord.__version__, "2.0.0"))

    async def background_task():
        await client.wait_until_ready()

        server_list_messages = {}
        session = aiohttp.ClientSession()

        while not client.is_closed():
            for catagory, values in config["source-query"].items():
                channel = client.get_channel(values["server-list-channel"])
                
                async with session.get("http://districtnine.host/api/serverquery/?ip={}".format(values["server-ips"])) as r:
                    if r.status == 200:
                        server = await r.json()

                        server_details = ""
                        for query in server:
                            if query["error"] == "none":
                                server_details += translations[language]["server-details-online"].format(query["name"], query["map"], query["players"], query["maxplayers"], query["ip"])
                            else:
                                server_details += translations[language]["server-details-offline"].format(query["ip"])

                        embed = discord.Embed(title=catagory.replace("-", " "), colour=discord.Colour(0x9a9faa), description=server_details)

                        if catagory in server_list_messages:
                            await server_list_messages[catagory].edit(embed=embed)
                        else:
                            msg = await channel.send(embed=embed)
                            server_list_messages.update({catagory:msg})

            await asyncio.sleep(config["general"]["update-time"])
        else:
            await session.close()

    client.loop.create_task(background_task())

    client.run(config["general"]["bot-token"])
else:
    print(translations[language]["wrong-version"].format(discord.__version__))
