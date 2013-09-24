"""
Usage:
    dudebot run-from-settings <settings-module>
    dudebot (-h | --help)

Options:
    -h --help          Show this screen.
"""
import docopt

import classutil
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

    if arguments.get("run-from-settings"):
        settings_module_name = arguments["<settings-module>"]

        # Try to import this as a module.
        #
        settings = classutil.import_module(settings_module_name)

        connector = get_connector(settings)

        for bot_ai in settings.BOT_AIS:
            connector.add_botai(bot_ai)

        for chatroom in settings.CHATROOMS:
            connector.join_chatroom(chatroom)

        try:
            connector.run_forever()
        except KeyboardInterrupt:
            pass
