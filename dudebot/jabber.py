import re
import time
import jabberbot

class JabberBot(jabberbot.JabberBot):

    def __init__(self, username, password, nickname, *args, **kwargs):
        super(JabberBot, self).__init__(username, password, nickname, *args, **kwargs)
        self.nickname = nickname
        self.botais = []

    def add_botai(self, botAI):
        self.botais.append(botAI)

    def callback_message(self, conn, mess):
        message = mess.getBody()
        if not message:
            return

        if len(self.botais) == 0:
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

        message = message.encode('ascii', 'ignore')

        for botAI in self.botais:
            response = botAI.respond(nickname, message)
            if response != None and response[0] == True:
                # have a tiny pause for dramatic effect
                time.sleep(0.5)
                self.send_simple_reply(mess, response[1])
                break
