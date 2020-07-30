from SourceQueryBot import SourceQueryBot
from SourceQueryBot.settings import Category, Server


bot_client = SourceQueryBot(
    [
        Category(
            "Retake",
            705852327550124062,
            [
                Server("216.52.148.47")
            ]
        )
    ]
)

if __name__ == "__main__":
    bot_client.run("<bot token>")
