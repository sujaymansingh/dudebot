"""Implement search and replace strings (sed style)."""
import datetime
import collections

from dudebot import core


class SedBot(core.BotAI):
    """Keep track of what people say. If they post a message of the form s/x/y
    then apply that search and replace to their last message and post.
    (Only if the search and replace actually does something though!)
    """
    def __init__(self, message_lifetime_in_secs=10):
        self.last_lines = collections.defaultdict(lambda : (None, None))
        self.message_lifetime = datetime.timedelta(seconds=message_lifetime_in_secs)

    def respond(self, sender_nickname, message):
        if message.startswith('s/'):
            parts = self.__parse_search_replace_string(message)
            if parts is None:
                return None

            # Has the person actually said anything?
            #
            time_said, previous_message = self.last_lines[sender_nickname]

            # If not, there is nothing to apply the search and replace to.
            #
            if previous_message is None:
                return None

            # Also, it may have been too long ago!
            #
            now = datetime.datetime.now()
            if time_said < (now - self.message_lifetime):
                return None
            
            # We have some valid search/replace params!
            #
            old, new, global_replace = parts

            if global_replace == True:
                new_message = previous_message.replace(old, new)
            else:
                new_message = previous_message.replace(old, new, 1)

            if new_message == previous_message:
                return None
            else:
                return 'What {0} meant to say was: {1}'.format(sender_nickname, new_message)
            
        else:
            self.__store_message(sender_nickname, message)

    def __store_message(self, sender_nickname, message):
        self.last_lines[sender_nickname] = (datetime.datetime.now(), message)

    def __parse_search_replace_string(self, s):
        if not s.startswith('s/'):
            return None
        
        # Strip off the s/ prefix.
        #
        s = s[2:]

        # Now split by '/'.
        #
        parts = s.split('/')
        if len(parts) < 2:
            return None

        global_replace = False
        old = parts[0]
        new = parts[1]

        if len(parts) > 2:
            if not (parts[2] == '' or parts[2] == 'g'):
                # We can only accept a 'g' or ''
                #
                return None
            else:
                global_replace = (parts[2] == 'g')

        return old, new, global_replace
        

