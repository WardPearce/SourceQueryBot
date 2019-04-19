![DNH Logo](https://camo.githubusercontent.com/742c455547018630cf337754b6e93a16e880dbd2/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f3433353630313839363836323930383433372f3533383532363832363139323936313533362f6e626664666864666864686468642e706e67)

# About
This discord bot can edit multiple messages for multiple source servers containing game details, e.g. player count, map and server name. This allows you to create separate messages for different gamemodes etc.

# Setup

### Configuring
- Edit config.json

#### General
```
language | Bot currently only has translations for english.
bot-token | Discord Bot token, https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
prefix | Command prefix, e.g. !rank & !top.
community-name | Name of your community.
update-time | How long in seconds should the stats take to update, 25 or above recommended.
```

#### Source Query
Add servers and categories.

``-`` is used to represent spaces.
category-title must be unique.

```
        "category-title": {
            "server-ips": "ip:port-ip:port-ip:port",
            "server-list-channel": 465887902920867841
        },
```
Last category should end with just ``}`` not ``},``

### Hosting
- Create a VPS running ubuntu 16.04 or above.
- Install python3.6 ``sudo add-apt-repository ppa:jonathonf/python-3.6``
- Run ``sudo apt-get install python3.6``
- Install pip3 ``sudo apt-get -y install python3-pip``
- Install discord.py rewrite ``python3 -m pip install -U discord.py``
- Install aiohttp ``pip3 install aiohttp``
- Install screen ``sudo apt-get install screen``

### Finally
- Upload bot files into the VPS.
- Run ``screen -R sourcequery``
- Then ``python3 source_query_rewrite.py``
- Press ``ctrl a, d`` to exit the screen.
- DONE!

# Preview
![Bot Preview](https://i.imgur.com/sHLPyeg.png)
