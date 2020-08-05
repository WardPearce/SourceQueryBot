class TranslationBase:
    shutdown: str
    on_ready: str
    server: str
    offline_title: str
    offline_msg: str
    normal_presence: str
    smart_presence: str
    invalid_py_version: str


class English(TranslationBase):
    shutdown = "The bot is shutting down, please DO NOT press ctrl + C"
    on_ready = "Logged on as {}"
    server = """**Map:** {}\n**Players:** {}/{}
**Connect:**\nsteam://connect/{}"""
    offline_title = "Unknown"
    offline_msg = "**This server is offline.**"
    normal_presence = "{}/{} on our servers."
    smart_presence = "{}/{} on {}"
    invalid_py_version = "Python 3.7 or above is required for" + \
        " smart presence, you're running {}"


class Russian(TranslationBase):
    shutdown = "Бот завершает работу, НЕ нажимайте ctrl + C"
    on_ready = "Вы вошли как {}"
    server = """**Карта:** {}\n**Игроков:** {}/{}
**Присоединиться:**\nsteam://connect/{}"""
    offline_title = "Неизвестно"
    offline_msg = "**Этот сервер офлайн.**"
    normal_presence = "{}/{} на наших серверах."
    smart_presence = "{}/{} на {}"
    invalid_py_version = "Python 3.7 или выше требуется для" + \
        " smart presence, у вас запущен {}"
