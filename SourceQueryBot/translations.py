class TranslationBase:
    shutdown: str
    on_ready: str


class English(TranslationBase):
    shutdown = "The bot is shutting down, please DO NOT press ctrl + C"
    on_ready = "Logged on as {}"
