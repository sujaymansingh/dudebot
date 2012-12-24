class BotAI(object):

    def set_nickname(self, nickname):
        self.nickname = nickname

    def initialise(self, init_params_as_dict):
        pass

    def respond(self, sender_nickname, message):
        pass


class Echo(BotAI):

    def respond(self, sender_nickname, message):
        return True, message
