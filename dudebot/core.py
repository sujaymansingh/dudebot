class BotAI(object):

    def __init__(self):
        pass

    def set_nickname(self, nickname):
        self.nickname = nickname

    def respond(self, sender_nickname, message):
        return None


class ConnectorMount(type):
    """This metaclass will ensure that any Connector classes defined can
    found later.
    """

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'connectors'):
            cls.connectors = []
        else:
            cls.connectors.append(cls)


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
