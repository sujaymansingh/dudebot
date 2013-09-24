import re
import time
import jabberbot
from dudebot import core


class JabberConnector(core.Connector):

    def __init__(self, username="", password="", nickname=""):
        super(JabberConnector, self).__init__()
        self.nickname = nickname
        self.jabber_bot = JabberBot(username, password, nickname, self)

    def join_chatroom(self, roomname):
        self.jabber_bot.join_room(roomname, self.nickname)

    def run_forever(self):
        self.jabber_bot.serve_forever()

        
class JabberBot(jabberbot.JabberBot):

    def __init__(self, username, password, nickname, parent, *args, **kwargs):
        super(JabberBot, self).__init__(username, password, nickname, *args, **kwargs)
        self.nickname = nickname
        self.parent = parent

    def callback_message(self, conn, mess):
        message = mess.getBody()
        if not message:
            return

        if len(self.parent.botais) == 0:
            return

        try:
            messtime = time.mktime(time.strptime(mess.getTimestamp(), '%Y%m%dT%H:%M:%S'))
            currtime = time.time()
            if (messtime < (currtime - 1)):
                return
            else:
                pass
        except Exception as e:
            pass

        sender = "%s" % mess.getFrom()
        prog = re.compile('.*@.*/(.*)$')
        result = prog.match(sender)
        if not result:
            return
        nickname = result.group(1)

        # We don't want to reply to ourselves
        if (nickname == self.nickname):
            return

        for botAI in self.parent.botais:
            response = botAI.respond(nickname, message)
            if response is not None:
                # have a tiny pause for dramatic effect
                time.sleep(0.5)
                self.send_simple_reply(mess, response)
                break
