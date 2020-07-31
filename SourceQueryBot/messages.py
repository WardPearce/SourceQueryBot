import aiofiles
import typing

from os import path, getcwd

from .exceptions import NoSuchConfigFile


class Messages:
    _saved_messages = []

    def __init__(self,
                 location: str = path.join(getcwd(), "messages.txt")) -> None:

        self.location = location

    async def get(self) -> list:
        """
        Gets discord message IDs.

        Returns
        -------
        list
            List of discord message IDs.

        Raises
        ------
        NoSuchConfigFile
            Raised when config file doesn't exist.

        Notes
        -----
        Truncates all file data once loaded.
        """

        if path.exists(self.location):
            async with aiofiles.open(self.location, "r+") as file:
                async for line in file:
                    yield line

                await file.truncate(0)
        else:
            raise NoSuchConfigFile()

    async def save(self, line: typing.Any) -> None:
        """
        Saves data into file.

        Paramters
        ---------
        line: str
            line to save.
        """

        if line not in self._saved_messages:
            self._saved_messages.append(line)

            async with aiofiles.open(self.location, mode="a") as file:
                await file.write("{}\n".format(line))
