"""
Usage:
    dudebot run <settings-module>
    dudebot debug <settings-module> with-fake-users <nickname>...
    dudebot (-h | --help)

Options:
    -h --help          Show this screen.
"""
import docopt

import classutil
import debug
import jabber


class InvalidProtocolException(Exception):
    pass


def get_connector(settings):
    # At the moment, we only support jabber.
    #
    protocol = settings.PROTOCOL
    if protocol.lower() != "jabber":
        raise InvalidProtocolException("Can't handle " + protocol)

    # Return a jabber connector.
    #
    return jabber.JabberConnector(
        username=settings.USERNAME,
        password=settings.PASSWORD,
        nickname=settings.NICKNAME
    )


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version="dudebot 0.5")
    settings_module_name = arguments["<settings-module>"]

    # Try to import this as a module.
    #
    settings = classutil.import_module(settings_module_name)

    if arguments.get("run"):
        connector = get_connector(settings)

    elif arguments.get("debug"):
        connector = debug.SimulatedChatRoom(settings.NICKNAME, arguments.get("<nickname>"))

    for bot_ai in settings.BOT_AIS:
        connector.add_botai(bot_ai)

    for chatroom in settings.CHATROOMS:
        connector.join_chatroom(chatroom)

    try:
        connector.run_forever()
    except KeyboardInterrupt:
        pass
