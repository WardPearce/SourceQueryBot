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


class Chinese(TranslationBase):
    shutdown = "机器人正在关闭，请不要按 ctrl + C"
    on_ready = "登录为 {}"
    server = """**地图名:** {}\n**玩家:** {}/{}
**连接:**\nsteam://connect/{}"""
    offline_title = "未知"
    offline_msg = "**此服务器离线.**"
    normal_presence = "{}/{} 在我们的服务器上."
    smart_presence = "{}/{} 在 {}"
    invalid_py_version = "需要 Python 3.7或更高版本" + \
        " smart presence, 您正在运行 {}"
