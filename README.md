dudebot
=======


Installation
------------

I'd strongly recommend using virtualenv (http://www.virtualenv.org).
That way once you create and activate the virtual env, you can simply add install.
```bash
pip install -e git+https://github.com/sujaymansingh/dudebot#egg=dudebot
```


Overview
--------

```python
from dudebot import core

class Ping(core.BotAI):
    """Respond to ping (and only ping) with pong."""

    def respond(self, sender_nickname, message):
        if message == 'ping':
            return 'pong'
        else:
            return None
```

This creates a bot that will respond to a message of 'ping' with 'pong'.
It ignores other messages by returning None.
```
real_person> Hello all
real_person> ping
bot> pong
```

There is also a utility decorator for if you want to only respond to messages
that start with a given string.
```python
from dudebot import core

class Echo(core.BotAI):
    """Echos everything after the beginning 'echo'."""

    @core.message_must_begin_with_prefix('echo')
    def respond(self, sender_nickname, message):
        return message
```
Note that the decorator also strips the prefix from the message.
```
real_person> Hi
real_person> echo this is a test
bot> this is a test
```


Usage
-----

I've used json for the config file format.
An example (test.json)
```json
{
    "type": "jabber",
    "username": "joeyjojo@example.com",
    "password": "junior-shabadoo",
    "nickname": "jeoyjojo",
    "chatrooms": ["something@conference.example.com"],
    "botais": ["dudebot.examples.demos.Ping"]
}
```

Then you can simply run it:
```bash
python -m dudebot --config_filename=test.json
```
You can pass more than one botais, but only the first one that returns a
response to a specific message will do so.
(I.e. if you have two botais bot1 and bot2 in the same dudebot, if bot1
responds then bot2 won't be checked.
If you need both of them then perhaps use two different dudebots.)
