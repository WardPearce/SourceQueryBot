import os

CURRECT_DIR = os.path.dirname(os.path.realpath(__file__))

CONFIG = {
    "bot": {
        "token": "",
        "embed_color": 0xaeb8da,
    },

    "lang": "en",

    "refresh_rate": 30,
    
    "smart_presence": True,

    "message_ids": "{}/message_ids.txt".format(CURRECT_DIR),

    "servers": {
        "Retakes": {
            "char_limit": 25,
            "channel": 653839007829983252,
            "servers": {
                "216.52.148.47:27015": "#1 | WS | KNIFE",
                "87.98.228.196:27040": "#2 | WS | KNIFE",
            },
        },
        "Bhop": {
            "char_limit": 25,
            "channel": 653839007829983252,
            "servers": {
                "92.119.148.31:27015": False,
                "92.119.148.18:27015": False,
            },
        },
    },
}