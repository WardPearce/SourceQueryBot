import aiofiles
import typing

from os import path

from .exceptions import NoSuchConfigFile


class Messages:
    def __init__(self,
                 location: str = path.join(
                     path.dirname(path.realpath(__file__)),
                     "messages.txt")) -> None:

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
            async with aiofiles.open(self.location) as file:
                data = await file.read()

                await file.truncate(0)

                return data.split("\n")
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

        async with aiofiles.open(self.location, mode="a") as file:
            await file.write(str(line))
