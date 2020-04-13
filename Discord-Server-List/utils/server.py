import asyncio
import discord

class Server(object):
    def __init__(self, obj):
        self.obj = obj

    presence_completed = True

    async def smart_presence(self, players, max_players, title, loop_index):
        if loop_index == self.obj.sever_amount:
            self.presence_completed = False

        sleep = loop_index * 10

        await asyncio.sleep(sleep)

        await self.obj.change_presence(status=discord.Status.online, activity=discord.Game(self.obj.TRANSLATIONS["smart_presence"].format(
            players,
            max_players,
            title
        )))

        if loop_index == self.obj.sever_amount:
            self.presence_completed = True

    async def format_message(self):
        total_players = 0
        total_max_players = 0

        loop_index = -1

        for name, values in self.obj.config_cache.items():
            embed = discord.Embed(title=self.obj.TRANSLATIONS["title"].format(name), colour=discord.Colour(self.obj.CONFIG["bot"]["embed_color"]))

            for server in values["servers"]:
                loop_index += 1

                ip_port = "{}:{}".format(server.ip, server.port)

                server_info = await server.get_info()

                if server_info != False:
                    if self.obj.CONFIG["servers"][name]["servers"][ip_port] == False:
                        server_name = server_info["hostname"][:self.obj.CONFIG["servers"][name]["char_limit"]]
                    else:
                        server_name = self.obj.CONFIG["servers"][name]["servers"][ip_port]

                    embed.add_field(name=server_name, value=self.obj.TRANSLATIONS["successful"].format(
                        server_info["map"], 
                        server_info["players"],
                        server_info["max_players"],
                        ip_port
                    ), inline=False)

                    if self.obj.CONFIG["smart_presence"]["enable"]:
                        if self.presence_completed:
                            if self.obj.CONFIG["smart_presence"]["name"]:
                                title = server_name
                            else:
                                title = server_info["map"]

                            asyncio.create_task(self.smart_presence(players=server_info["players"], max_players=server_info["max_players"],
                                                                    title=title, loop_index=loop_index))
                    else:
                        total_players += server_info["players"]
                        total_max_players += server_info["max_players"]
                else:
                    if self.obj.CONFIG["servers"][name]["servers"][ip_port] == False:
                        server_name = self.obj.TRANSLATIONS["fail_title"]
                    else:
                        server_name = self.obj.CONFIG["servers"][name]["servers"][ip_port]

                    embed.add_field(name=server_name, value=self.obj.TRANSLATIONS["fail"], inline=False)

                await asyncio.sleep(0.1)

            if values.get("msg"):
                try:
                    await values["msg"].edit(embed=embed)
                except Exception as error:
                    self.obj.config_error("Couldn't edit {}\n\nError\n{}".format(values["msg"], error))
            else:
                try:
                    self.obj.config_cache[name]["msg"] = await values["channel"].send(embed=embed)
                except Exception as error:
                    self.obj.config_error("Couldn't message {}\n\nError\n{}".format(values["channel"], error))
                else:
                    try:
                        await self.obj.config.update(values["channel"].id, self.obj.config_cache[name]["msg"].id)
                    except Exception as error:
                        self.obj.config_error(error)

            await asyncio.sleep(0.1)

        if not self.obj.CONFIG["smart_presence"]["enable"]:
            await self.obj.change_presence(status=discord.Status.online, activity=discord.Game(self.obj.TRANSLATIONS["total_players"].format(total_players, total_max_players)))