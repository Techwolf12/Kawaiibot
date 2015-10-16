#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random

from imgurpython import ImgurClient as Client
import telegram as Telegram

from sys import exit as die

LAST_UPDATE_ID  = None

with open('config.ini', 'r+') as f:
    for line in f.readlines():
        exec(line)

class Bot():
    def __init__(self, attributes = {}):
        self.__dict__ = attributes
        self.commands = {}
        self.prefix = "!"

    def log(self, to, message, status):
        """ Create a new log entry.
            @to: The logfile to write to.
            @message: A brief explanation regarding the log entry.
            @status: Success, failure, warning.
        """

        with open(to, 'a') as f:
            f.write("{} [{}]".format(message, status))
        return

    def command(self, handle):
        """ Create a new command entry, saved in self.commands
            @handle: The unique handle for the command call.
        """

        def arguments(function):
            if type(function).__name__ == 'function':
                self.commands[handle] = function
            return self.commands
        return arguments

    def main(self):
        """ Initially start listening for chat events.
        """
        bot = Telegram.Bot(token=TELEGRAM_TOKEN)


        # TODO: Make this not hacky with tries.
        try:
            LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
        except IndexError:
            LAST_UPDATE_ID = None

        while True:
            for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
                message = update.message.text[1::]
                prefix = update.message.text[0]
                instances = [{'name':n, 'found':n == message} for n in self.commands]

                for instance in instances:
                    if (instance['found'] and prefix == self.prefix):
                        bot.sendMessage(
                            chat_id = update.message.chat_id,
                            text = self.commands[instance['name']]()
                        )
                        LAST_UPDATE_ID = update.update_id + 1

if __name__ == '__main__':
    botname = Bot()

    @botname.command("hey")
    def purestofmemes():
        return "Hi!"

    @botname.command("kaf2")
    def evenfinermemes():
        client = Client(IMGUR_ID, IMGUR_SECRET)
        random_sort = random.choice(['time', 'top'])
        items = client.subreddit_gallery('awwnime', sort=random_sort, window='week', page=0)

        return random.choice(items).link

    botname.main()
