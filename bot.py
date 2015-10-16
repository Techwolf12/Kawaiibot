from sys import exit as die
import telegram
import random
import json

with open('config.json') as f:
    config = json.load(f)

class Bot():
    commands = {}
    last_id = None

    def __init__(self, attributes={}, prefix='!'):
        self.__dict__ = attributes
        self.prefix = prefix

    def log(self, to, message, status):
        """ Create a new log entry.
            @to: The logfile to write to.
            @message: A brief explanation regarding the log entry.
            @status: Success, failure, warning.
        """

        with open(to, 'a') as f:
            f.write('{} [{}]'.format(message, status))

    def command(self, handle):
        """ Create a new command entry, saved in self.commands
            @handle: The unique handle for the command call.
        """

        def arguments(function):
            if type(function).__name__ == 'function':
                self.commands[handle] = function
            return self.commands
        return arguments

    def repl(self):
        """ Initially start listening for chat events.
        """
        bot = telegram.Bot(token=config['telegram']['token'])

        # TODO: Make this not hacky with tries.
        try:
            self.last_id = bot.getUpdates()[-1].update_id
        except IndexError:
            self.last_id = None

        while True:
            for update in bot.getUpdates(offset=self.last_id, timeout=10):
                message = update.message.text[1::]
                prefix = update.message.text[0]
                instances = [{'name':n, 'found':n == message} for n in self.commands]

                for instance in instances:
                    if (instance['found'] and prefix == self.prefix):
                        bot.sendMessage(
                            chat_id = update.message.chat_id,
                            text = self.commands[instance['name']]()
                        )
                        self.last_id = update.update_id + 1

bot = Bot()
