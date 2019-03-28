import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
import asyncio
import aiohttp
import time

###################################################################################################################################################################
# Config
bot_token = "" # Discord bot token. Find at https://discordapp.com/developers/applications/me
set_prefix = '!' # Sets command prefix.
server_channel = '' # Channel ID for servers to be posted in.
embed_color = 0xE8CA11   # Do not remove 0x  || Message Color. Hex, 6 characters. Do NOT include # | Helpful link https://htmlcolorcodes.com/color-picker/
update_time  = 120 # How many seconds should it take to update.

ips = "ip:port-ip:port-ip:port" # The amount of servers are limited due to discord's message character limit.
###################################################################################################################################################################

bot = commands.Bot(command_prefix=set_prefix)


async def task():
    await bot.wait_until_ready()
    while True:
        await asyncio.sleep(1)
        print("{} | Running".format(time.strftime("%Y-%m-%d %H:%M")))

def handle_exit():
    print("{} | Handling".format(time.strftime("%Y-%m-%d %H:%M")))
    bot.loop.run_until_complete(bot.logout())
    for t in asyncio.Task.all_tasks(loop=bot.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            bot.loop.run_until_complete(asyncio.wait_for(t, 5, loop=bot.loop))
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass

while True:
    @bot.event
    async def on_ready():
        print("Bot connected!\nCurrently linked to {}".format(bot.user.name))

    async def background_loop():
        await bot.wait_until_ready()
        first_load = 1
        while not bot.is_closed:
            try:
                server_details = ''
                async with aiohttp.get('http://districtnine.host/api/serverquery/?ip={}'.format(ips)) as r:
                    if r.status == 200:
                        data = await r.json()
                        for query in data:
                            if query["error"] == "none":
                                server_details += "\n\n**Name:** {} \n**Map**: {}\n**Players:** {}\{} \nsteam://connect/{}".format(query["name"], query["map"], query["players"], query["maxplayers"], query["ip"])
                            else:
                                server_details += "\n\n**IP:** {} \n**Status:** Offline".format(query["ip"])
                        embed = discord.Embed(colour=discord.Colour(embed_color))
                        embed.add_field(name="SERVERS", value=server_details, inline=False)
                        if first_load == 1:
                            first_load = 0
                            msg = await bot.send_message(bot.get_channel(server_channel), embed=embed)
                        else:
                            await bot.edit_message(msg, embed=embed)
            except:
                if first_load == 0:
                    first_load = 1
                    await bot.delete_message(msg)

            await asyncio.sleep(update_time)

    bot.loop.create_task(background_loop())

    bot.loop.create_task(task())
    try:
        bot.loop.run_until_complete(bot.start(bot_token))
    except SystemExit:
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()
        bot.loop.close()
        print("{} | Program ended".format(time.strftime("%Y-%m-%d %H:%M")))
        break

    print("{} | Bot restarting".format(time.strftime("%Y-%m-%d %H:%M")))
    bot = discord.bot(loop=bot.loop)
