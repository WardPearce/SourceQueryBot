import aiofiles
import aioquery
import os


class Config(object):
    def __init__(self, obj):
        self.obj = obj

    def cache(self):
        """ Caches config into memeory and initializes needed objects. """

        for name, values in self.obj.CONFIG["servers"].items():
            if values.get("channel") and values.get("servers"):
                channel_obj = self.obj.get_channel(values["channel"])

                if channel_obj:
                    self.obj.config_cache[name] = {
                        "channel": channel_obj,
                        "servers": [],
                    }

                    for server in values["servers"].keys():
                        self.obj.sever_amount += 1

                        ip_port = server.split(":")
                        self.obj.config_cache[name]["servers"].append(
                            aioquery.client(ip_port[0], int(ip_port[1]))
                        )
                else:
                    self.obj.config_error(
                        "Unable to pull channel with ID {}.".format(
                            values["channel"]
                        )
                    )
            else:
                self.obj.config_error(
                    "Unable to pull [{}], no channel, servers or players given.".format(
                        name
                    )
                )

    async def load(self):
        """ Loads message_ids config. """

        if os.path.isfile(self.obj.CONFIG["message_ids"]):
            async with aiofiles.open(
                    self.obj.CONFIG["message_ids"], mode="r+") as file:
                async for line in file:
                    channel_msg = line.split(":")

                    channel = self.obj.get_channel(int(channel_msg[0]))
                    if channel:
                        msg = await channel.fetch_message(int(channel_msg[1]))
                        if msg:
                            await msg.delete()

                await file.truncate(0)

                await file.close()

    async def update(self, message_id, channel_id):
        """ Updates message_ids config. """

        async with aiofiles.open(
                self.obj.CONFIG["message_ids"], mode="a") as file:
            await file.write("{}:{}\n".format(message_id, channel_id))
            await file.close()
