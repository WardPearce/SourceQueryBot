[![GitHub issues](https://img.shields.io/github/issues/WardPearce/SourceQueryBot)](https://github.com/WardPearce/SourceQueryBot/issues)
[![GitHub license](https://img.shields.io/github/license/WardPearce/SourceQueryBot)](https://github.com/WardPearce/SourceQueryBot/blob/master/LICENSE)
[![Actions Status](https://github.com/WardPearce/SourceQueryBot/workflows/Python%20application/badge.svg)](https://github.com/WardPearce/SourceQueryBot/actions)

#### Smart Presence Requires python 3.7 or higher!

# About
This discord bot can edit multiple messages for multiple source servers containing game details, e.g. player count, map and server name. This allows you to create separate messages for different gamemodes etc.

#### Status: Stable

## Index
- [Setup](#setup)
- [Supported languages](#languages)
- [API](#api)
- [Preview](#preview)

## Setup
- ``pip3 install SourceQueryBot``
- Create a file like [run.py](https://github.com/WardPearce/SourceQueryBot/blob/Development/run.py) & enter your bot token.
- Run ``run.py`` using pm2 or screen!

## Languages
- English (Default) - ``SourceQueryBot.translations.English``
- Russian - ``SourceQueryBot.translations.Russian``

## API
- ``from SourceQueryBot import SourceQueryBot``
    ```
    Pass any discord bot client args / parameters.

    Parameters
    ----------
    catagories: list
        List of category objects.
    language: TranslationBase
        Defaults to english, pass it any language class.
    messages: Messages
        Handles message caching.
    smart_presence: bool
        Defaults to false, if enabled presence will rotate between maps.
    ```

- ``from SourceQueryBot.settings import Category``
    ```
    Handles server commands.

    Parameters
    ----------
    name: str
        Name of category
    server_name_limit: int
        Limits how many characters the server name can be.
    channel: int
        Discord channel ID for this category.
    color: hex
        Hex color code.
    servers: list
        List of Server objects.
    inline: bool
        Defaults to false, if servers should be inline.
    ```

- ``from SourceQueryBot.settings import Server``
    ```
    Handles server settings.

    Parameters
    ----------
    ip: str
        IP address of server.
    port: int
        Port of server, defaults to 27015.
    alt_name: str
        Optionally set a name what will overwrite the servers name.
    ```

## Preview
#### Server List
![Preview](http://i.imgur.com/Ph9iZgR.png)

#### Smart Presence
Updates the bot's presence every 10 seconds to a different server.

![Smart Presence](https://i.imgur.com/Hb5LNaq.png)

#### Normal Presence
Displays total server stats.

![Normal Presence](https://i.imgur.com/WYsuujT.png)
