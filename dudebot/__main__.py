import logging
import json
import optparse
import sys
import traceback
from dudebot import jabber
from dudebot import classutil


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option("--config_filename", dest="config_filename", help="The name of the json file with all the details", metavar="CONFIG")
    parser.add_option("--name", dest="name", help="The name of the bot to run", metavar="NAME")

    options, args = parser.parse_args()

    # Read the config file.
    with open(options.config_filename, 'r') as config_file:
        config_data = json.load(config_file)

    # Grab all we need!
    username = config_data['username']
    password = config_data['password']
    nickname = config_data['nickname']
    chatrooms = config_data['chatrooms']
    botais = config_data['botais']

    # Set up logging.
    if getattr(config_data, 'logfile', None) is None:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(filename=config_data.logfile, mode='at+', level=logging.DEBUG)

    logging.info('about to start connecting')
    connector = jabber.JabberBot(username, password, nickname)

    for botai in botais:
        # TODO!
        klass = classutil.get_class(botai)
        botai_obj = klass()
        botai_obj.initialise(None)
        botai_obj.set_nickname(nickname)
        connector.add_botai(botai_obj)

    for chatroom in chatrooms:
        logging.debug('about to join {0} as {1}'.format(chatroom, nickname))
        connector.join_room(chatroom, nickname)

    try:
        connector.serve_forever()
    except Exception as e:
        traceback.print_exc()
