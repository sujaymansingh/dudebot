import string
from dudebot import ai


class Echo(ai.BotAI):
    """Echos everything!"""

    def respond(self, sender_nickname, message):
        return message


class EchoOnlyIfAddressed(ai.BotAI):
    """Using the decorator, only echo if directly addressed."""

    @ai.message_must_begin_with_nickname
    def respond(self, sender_nickname, message):
        return message


class ROT13(ai.BotAI):

    @ai.message_must_begin_with_prefix('rot13')
    def respond(self, sender_nickname, message):
        rot13 = string.maketrans(
            "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
            "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
        )
        return string.translate(message, rot13)

