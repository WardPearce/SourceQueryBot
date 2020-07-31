from .settings import Category
from .exceptions import InvalidChannel

from discord import channel


CACHED_CATAGORIES = {}


class CachedMessaging:
    def __init__(self, catgory: Category, channel: channel,
                 *args, **kwargs) -> None:
        self.catgory = catgory
        self.args = args
        self.kwargs = kwargs
        self.channel = channel

    async def send_edit(self) -> channel:
        if self.catgory in CACHED_CATAGORIES:
            await CACHED_CATAGORIES[self.catgory].edit(**self.kwargs)
        else:
            if self.channel:
                message = await self.channel.send(*self.args, **self.kwargs)

                CACHED_CATAGORIES[self.catgory] = message
            else:
                raise InvalidChannel()

        return CACHED_CATAGORIES[self.catgory]
