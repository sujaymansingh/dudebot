class BotAI(object):

    def __init__(self):
        pass

    def set_nickname(self, nickname):
        self.nickname = nickname

    def respond(self, sender_nickname, message):
        return None


class Connector(object):
    """A basic chat type connector.
    """
    name = 'generic'

    def __init__(self):
        self.botais = []

    def add_botai(self, botai):
        self.botais.append(botai)

    def join_chatroom(self, roomname):
        pass

    def run_forever(self):
        pass
