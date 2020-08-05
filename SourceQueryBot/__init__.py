import discord
from discord import Embed, Color, Status, Game
from discord.ext import tasks

import asyncio
import sys
import logging

from aioquery.exceptions import InvalidServer, DidNotReceive, UnableToConnect

from .translations import TranslationBase, English
from .messages import Messages
from .cached_messaging import CachedMessaging


__version__ = "1.0.2"


logging.basicConfig(level=logging.INFO)


class SourceQueryBot(discord.Client):
    _presence_completed = True
    _total_servers = 0

    def __init__(self, catagories: list,
                 language: TranslationBase = English,
                 messages: Messages = Messages(),
                 smart_presence: bool = False,
                 *args, **kwargs) -> None:
        """
        Pass any discord bot client args / parameters.

        Parameters
        ----------
        catagories: list
            List of category objects.
        language: TranslationBase
            Defaults to english.
        messages: Messages
            Handles message caching.
        smart_presence: bool
            Defaults to false, if enabled presence will rotate between maps.
        """

        super().__init__(*args, **kwargs)

        self.language = language
        self.catagories = catagories
        self.messages = messages

        if not sys.version_info[1] >= 7 and smart_presence:
            self.smart_presence = False
            logging.log(
                logging.INFO,
                language.invalid_py_version.format(
                    sys.version
                )
            )
        else:
            self.smart_presence = smart_presence

        self.query_task.start()

    async def on_ready(self) -> None:
        print(self.language.on_ready.format(self.user))

    async def close(self) -> None:
        print(self.language.shutdown)

        await super().close()
        self.query_task.cancel()

    async def _smart_presence(self, players, max_players,
                              map_name, loop_index) -> None:

        if loop_index == self._total_servers:
            self._presence_completed = False

        await asyncio.sleep(loop_index * 10)

        await self.change_presence(
            status=Status.online,
            activity=Game(
                self.language.smart_presence.format(
                    players,
                    max_players,
                    map_name
                )
            )
        )

        if loop_index == self._total_servers:
            self._presence_completed = True

    @tasks.loop(seconds=30.0)
    async def query_task(self) -> None:
        total_players = 0
        total_max_players = 0

        loop_index = -1

        for catgory in self.catagories:
            embed = Embed(
                title=catgory.name,
                color=Color(catgory.color)
            )

            for server in catgory.servers:
                try:
                    info = await server.interact.info()
                except (InvalidServer, DidNotReceive, UnableToConnect):
                    embed.add_field(
                        name=server.alt_name if server.alt_name else
                        self.language.offline_title,
                        value=self.language.offline_msg
                    )
                else:
                    embed.add_field(
                        name=server.alt_name if server.alt_name else
                        info.hostname[:catgory.server_name_limit] + "...",
                        value=self.language.server.format(
                            info.map,
                            info.players,
                            info.max_players,
                            "{}:{}".format(server.ip, server.port)
                        ),
                        inline=catgory.inline
                    )

                    total_players += info.players
                    total_max_players += info.max_players

                    if self.smart_presence and self._presence_completed:
                        loop_index += 1

                        asyncio.create_task(
                            self._smart_presence(
                                info.players,
                                info.max_players,
                                info.map,
                                loop_index
                            )
                        )

                await asyncio.sleep(0.0001)

            sent_message = await CachedMessaging(
                catgory, self.get_channel(catgory.channel), embed=embed
            ).send_edit()

            await self.messages.save("{}:{}".format(
                catgory.channel, sent_message.id
            ))

            await asyncio.sleep(0.0001)

        if not self.smart_presence:
            await self.change_presence(
                status=Status.online,
                activity=Game(
                    self.language.normal_presence.format(
                        total_players,
                        total_max_players
                    )
                )
            )

    @query_task.before_loop
    async def before_query_task(self) -> None:
        """
        Handles deleting old messages & caching config details.
        """

        await self.wait_until_ready()

        async for message in self.messages.get():
            try:
                channel_id, message_id = message.split(":")
            except ValueError:
                pass
            else:
                channel = self.get_channel(int(channel_id))
                if channel:
                    try:
                        message_obj = await asyncio.wait_for(
                            channel.fetch_message(int(message_id)),
                            3
                        )
                    except Exception:
                        pass
                    else:
                        if message_obj:
                            await message_obj.delete()

        for catgory in self.catagories:
            for server in catgory.servers:
                self._total_servers += 1

            await asyncio.sleep(0.00001)
