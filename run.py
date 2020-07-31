from SourceQueryBot import SourceQueryBot
from SourceQueryBot.settings import Category, Server


bot_client = SourceQueryBot(
    [
        Category(
            "Retake",
            705852327550124062,
            0xffffff,
            [
                Server("216.52.148.47"),
                Server("54.37.111.216"),
                Server("92.119.148.18"),
            ]
        ),
        Category(
            "Bhop",
            705852327550124062,
            0x444444,
            [
                Server("92.119.148.31")
            ]
        )
    ],
    smart_presence=True
)

if __name__ == "__main__":
    bot_client.run("<bot token>")
