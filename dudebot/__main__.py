import logging
import json
import optparse
import sys
import traceback
from dudebot import jabber
from dudebot import classutil
from dudebot import core


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option("--config_filename", dest="config_filename", help="The name of the json file with all the details", metavar="CONFIG")
    parser.add_option("--name", dest="name", help="The name of the bot to run", metavar="NAME")

    options, args = parser.parse_args()

    # Read the config file.
    with open(options.config_filename, 'r') as config_file:
        all_config_data = json.load(config_file)

    # Have we been told to only look at a particular key?
    if getattr(options, 'name') is None:
        config_data = all_config_data
    else:
        config_data = all_config_data[options.name]

    # Grab all we need!
    nickname = config_data['nickname']
    chatrooms = config_data['chatrooms']
    botais = config_data['botais']

    # Set up logging.
    if getattr(config_data, 'logfile', None) is None:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(filename=config_data.logfile, mode='at+', level=logging.DEBUG)

    logging.info('about to start connecting')

    connector_class = classutil.get_class(config_data['type'])
    connector = connector_class(config_data)

    for botai in botais:
        if isinstance(botai, str):
            classname = botai
            params = {}
        else:
            classname = botai[0]
            params = botai[1]

        # TODO!
        klass = classutil.get_class(classname)
        botai_obj = klass(params)
        botai_obj.set_nickname(nickname)
        connector.add_botai(botai_obj)

    for chatroom in chatrooms:
        logging.debug('about to join {0} as {1}'.format(chatroom, nickname))
        connector.join_room(chatroom, nickname)

    try:
        connector.run_forever()
    except Exception as e:
        traceback.print_exc()
