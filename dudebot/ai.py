class BotAI(object):

    def set_nickname(self, nickname):
        self.nickname = nickname

    def initialise(self, init_params_as_dict):
        pass

    def respond(self, sender_nickname, message):
        return False, ''


class message_must_begin_with_prefix(object):
    """A simple decorator so that a bot AI can ignore all messages that don't
    begin with the given prefix.
    That way you can have your dude bot only respond to messages that, for 
    example, begin with 'dude '.
    """

    def __init__(self, desired_prefix):
        self.desired_prefix = desired_prefix

    def __call__(self, func):
        def wrapped_func(botai, sender_nickname, message, *args, **kwargs):
            if message.startswith(self.desired_prefix):
                return func(botai, sender_nickname, message, *args, **kwargs)
            else:
                return False, ''
        return wrapped_func


def message_must_begin_with_nickname(func):
    """A simple decorator so that a bot AI can ignore all messages that don't
    begin with the bot AI's nickname.
    """
    def wrapped_func(botai, sender_nickname, message, *args, **kwargs):
        if message.startswith(botai.nickname):
            return func(botai, sender_nickname, message, *args, **kwargs)
        else:
            return False, ''
    return wrapped_func


class Echo(BotAI):

    def respond(self, sender_nickname, message):
        return True, message
