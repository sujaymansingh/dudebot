"""Some useful decorators.
"""

class message_must_begin_with(object):
    """A simple decorator so that a bot AI can ignore all messages that don't
    begin with the given prefix.
    That way you can have your dude bot only respond to messages that, for
    example, begin with 'dude '.
    """

    def __init__(self, desired_prefix):
        self.desired_prefix = desired_prefix

    def __call__(self, func):
        def wrapped_func(botai, sender_nickname, message, *args, **kwargs):
            startswith, suffix = extract_suffix(message, self.desired_prefix)
            if startswith:
                return func(botai, sender_nickname, suffix, *args, **kwargs)
            else:
                return None
        return wrapped_func


class message_must_begin_with_attr(object):
    """This decorator states that the bot AI will ignore all messages that
    don't begin with the given attr of the botAI.
    """

    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __call__(self, func):
        def wrapped_func(botai, sender_nickname, message, *args, **kwargs):
            prefix = getattr(botai, self.attr_name)
            startswith, suffix = extract_suffix(message, prefix)
            if startswith:
                return func(botai, sender_nickname, suffix, *args, **kwargs)
            else:
                return None
        return wrapped_func


def message_must_begin_with_nickname(func):
    """A simple decorator so that a bot AI can ignore all messages that don't
    begin with the bot AI's nickname.
    """
    def wrapped_func(botai, sender_nickname, message, *args, **kwargs):
        startswith, suffix = extract_suffix(message, botai.nickname)
        if startswith:
            return func(botai, sender_nickname, suffix, *args, **kwargs)
        else:
            return None
    return wrapped_func


def extract_suffix(message, prefix):
    """Extract everything after the prefix. If message doesn't start with the
    prefix then return (False, '') otherwise (True, suffix).
    Note that it will remove any whitespace between the prefix and the rest of
    the message.

    >>> extract_suffix('hoohah test message', 'hoohah')
    (True, 'test message')
    >>> extract_suffix('hoohah test 2 ', 'something')
    (False, '')
    >>> extract_suffix('hoohah', 'hoohah')
    (True, '')
    """
    if not message.startswith(prefix):
        return False, ''

    suffix = message[len(prefix):]

    # I hate leading whitespace!
    #
    return True, suffix.lstrip()


