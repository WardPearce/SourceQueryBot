import json
import os

import asyncio
import aiohttp
from aiopickle import aiopickle

import discord

with open("{}/config/config.json".format(os.path.dirname(os.path.realpath(__file__)))) as config_file:  
    config = json.load(config_file)

with open("{}/config/translations.json".format(os.path.dirname(os.path.realpath(__file__)))) as translations_file:  
    translations = json.load(translations_file)

language = config["general"]["language"]

if discord.version_info.major == 1:

    client = discord.Client()

    @client.event
    async def on_ready():
        print(translations[language]["connection-successful"].format(client, config["general"]["community-name"], discord.__version__, "3.0.0"))

    async def query_loop():
        await client.wait_until_ready()

        server_messages = {}

        while not client.is_closed():
            for category, values in config["source-query"].items():

                channel = client.get_channel(values["server-list-channel"])

                async with aiohttp.ClientSession() as session:
                    async with session.get("https://districtnine.host/api/serverquery/?ip={}".format(values["server-ips"])) as r:
                        server_details = await r.json()

                        server_message = ""
                        for server_query in server_details:
                            if server_query["error"] == "none":
                                server_message += translations[language]["server-details-online"].format(server_query["name"], server_query["map"], server_query["players"], server_query["maxplayers"], server_query["ip"])
                            else:
                                server_message += translations[language]["server-details-offline"].format(server_query["ip"])

                        embed = discord.Embed(title=category, colour=discord.Colour(0x9a9faa), description=server_message)

                        if category in server_messages:
                            await server_messages[category].edit(embed=embed)
                        else:
                            msg_object = await channel.send(embed=embed)
                            server_messages[category] = msg_object

                await asyncio.sleep(1.5)

            await asyncio.sleep(config["general"]["update-time"])

    client.loop.create_task(query_loop())
    client.run(config["general"]["bot-token"])
else:
    print(translations[language]["wrong-version"].format(discord.__version__))
