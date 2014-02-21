dudebot
=======

Installation
------------

I'd strongly recommend using virtualenv (http://www.virtualenv.org).
That way once you create and activate the virtual env, you can simply
 install it with pip.

.. code::

    pip install git+https://github.com/sujaymansingh/dudebot.git


Basic usage
-----------

Let us take an example file: ``bots.py``.

We can add the following.

.. code::

    import dudebot

    class Ping(dudebot.BotAI):
        def respond(self, sender_nickname, message):
            if message == "ping":
                return "pong"

This defines a Bot AI that will reply to any message of ``ping`` with
``pong``. All other messages will be ignored.

Then simply add some connection details to ``bots.py``.

.. code::

    NICKNAME = "<nickname of bot>"

    PROTOCOL = "jabber"
    USERNAME = "<jabber account username including @blah.com>"
    PASSWORD = "<jabber account password>"

    CHATROOMS = ["full chat room name (including @blah.com)"]
    BOT_AIS = [
        Ping()
    ]

Now you can run the dudebot with your filename (without the ``.py``
extension).

.. code::

    python -m dudebot run bots

Responding by name
------------------

The nickname of the sender is ``sender_nickname``.

So add a new Bot AI to bots.py:

.. code::

    class Hello(dudebot.BotAI):
        def respond(self, sender_nickname, message):
            if message == "hello":
                return "hello " + sender_nickname

and

::

    BOT_AIS = [
        Ping(),
        Hello()
    ]

Some useful decorators
----------------------

There are some decorators that can be used.

.. code::

    class Echo(dudebot.BotAI):
        @dudebot.message_must_begin_with("echo")
        def respond(self, sender_nickname, message):
            # The decorator ensures that if we reach here, then the original
            # message began with echo. Also, the decorator strips out the prefix.

            # Return everything after "echo "
            #
            return message

Add ``Echo()`` to ``BOT_AIS`` and run again.

Other decorators:

.. code::

    class READMEBot(core.BotAI):
    
        def __init__(self, prefix, readme_filename):
            self.prefix = prefix
            self.readme = open(readme_filename, "r+").read()

        @dudebot.message_must_begin_with_attr("prefix")
        def respond(self, sender_nickname, message):
            if message == "top":
                return self.readme[:50]
            elif message == "all":
                return self.readme

    # Now we can add multiple instances, and each instance will only respond to
    # messages that begin with the value of its prefix attribute.
    #
    bot1 = READMEBot("git", "git/README.txt")
    bot2 = READMEBot("svn", "svn/README.txt")

Also, ``@dudebot.message_must_begin_with_nickname`` will make the bot AI
only respond if the message began with the bot's nickname.

Debugging
---------

If you want to debug without actually connecting to a server, use the
``debug`` option. It will simulate a debug chatroom with some fake
users. (The bot will also be in the chatroom of course.)

.. code::

    $ python -m dudebot debug bots with-fake-users ed mike chris james paul
    People in chatroom: ['bot', 'ed', 'mike', 'chris', 'james', 'paul']
    /changeto nickname <- Changes to given nickname
    Otherwise, just type to chat
    (Hit enter after each line!)
    ed> hi all
    ed> ping
    bot> pong
    ed> hello
    bot> hello ed
    ed> echo this is a test
    bot> this is a test
    ed> /changeto chris
    chris> hello
    bot> hello chris
    chris>

Examples
--------

SedBot
~~~~~~

Add ``dudebot.examples.sedbot.SedBot()`` to your settings.

.. code::

    $ python -m dudebot debug bots with-fake-users u1 u2
    INFO:root:Starting...
    People in chatroom: ['Dude Bot', 'u1', 'u2']
    /changeto nickname <- Changes to given nickname
    Otherwise, just type to chat
    (Hit enter after each line!)
    u1> I have to catch a tain
    u1> s/tain/train
    Dude Bot> What u1 meant to say was: I have to catch a train
    u1>


Google Examples
---------------

There are some examples defined in ``dudebot.examples.google``

Consider an example ``google_examples.py``:

.. code::

    import dudebot.examples.google

    NICKNAME = "googlebot"

    PROTOCOL = "doesnt matter"
    USERNAME = "doesnt matter"
    PASSWORD = "doesnt matter"

    CHATROOMS = ["doesnt matter"]
    BOT_AIS = [
        dudebot.examples.google.YoutubeSearch(),
        dudebot.examples.google.GoogleSearch()
    ]

Google Search
~~~~~~~~~~~~~

.. code::

    $ python -m dudebot debug google with-fake-users matt
    People in chatroom: ['googlebot', 'matt']
    /changeto nickname <- Changes to given nickname
    Otherwise, just type to chat
    (Hit enter after each line!)
    matt> goog.search linus torvalds
    googlebot> 1 of 4
    http://en.wikipedia.org/wiki/Linus_Torvalds Linus Torvalds - Wikipedia, the free encyclopedia
    matt> goog.next
    googlebot> 2 of 4
    https://plus.google.com/%2BLinusTorvalds Linus Torvalds - Google+
    matt> goog.next
    googlebot> 3 of 4
    http://en.wikiquote.org/wiki/Linus_Torvalds Linus Torvalds - Wikiquote
    matt> goog.search asgbasijgbasipbgasijbgasojrnasorjynaoprjybarybw
    googlebot> No results for asgbasijgbasipbgasijbgasojrnasorjynaoprjybarybw
    matt>

Youtube Search
~~~~~~~~~~~~~~

.. code::

    $ python -m dudebot debug google with-fake-users matt
    People in chatroom: ['googlebot', 'matt']
    /changeto nickname <- Changes to given nickname
    Otherwise, just type to chat
    (Hit enter after each line!)
    matt> yt.search benton dog deer
    googlebot> 1 of 25
    http://www.youtube.com/watch?v=3GRSbr0EYYU&feature=youtube_gdata JESUS CHRIST IN RICHMOND PARK: ORIGINAL UPLOAD
    matt> yt.next
    googlebot> 2 of 25
    http://www.youtube.com/watch?v=lWv2wtvK6hg&feature=youtube_gdata Irate man chases Fenton the dog in Richmond Park
    matt> yt.next
    googlebot> 3 of 25
    http://www.youtube.com/watch?v=Y9QurgFU7U0&feature=youtube_gdata Fenton (aka Benton) the dog catches a Deer in the big hairy forest of Richmond Park
    matt>
