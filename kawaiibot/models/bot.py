import os
import sys

try:
    import telegram
    import json
except ImportError as e:
    print('You\'ve failed to import one of the required modules. Did you pip the requirements? {}'.format(e), file=sys.stderr)
    sys.exit(1)
try:
    with open(os.path.expanduser('~/.config/kawaiibot.json')) as f:
        config = json.load(f)
except FileNotFoundError as e:
    print('The require configuration file was not found. Are you sure that \'~/.config/kawaiibot.json\' exist? {}'.format(e), file=sys.stderr)
    sys.exit(1)

class Bot():
    logfile = os.path.expanduser('~/kawaiibot.log')
    commands = {}
    last_id = None

    def __init__(self, attributes={}, prefix='!'):
        self.__dict__ = attributes
        self.prefix = prefix

    def log(self, message, status):
        """ Create a new log entry.
            @message: A brief explanation regarding the log entry.
            @status: 0: Success, 1: Warning, 2: Error.
        """

        with open(self.logfile, 'a') as f:
            f.write('{} [{}]'.format(message, status))

        if status in [2, 3]:
            print(message, file=sys.stderr)
        print(message, file=sys.stdout)

    def command(self, handle):
        """ Create a new command entry, saved in self.commands
            @handle: The unique handle for the command call.
        """

        self.log('Attempting to create new command', 0)
        def arguments(function):
            if type(function).__name__ == 'function':
                self.commands[handle] = function
            else:
                self.log('{}.{} -> {}'.format(self.__class__.__name__, '__name__',
                         'Detected argument was not a function'), 2)
            self.log('Succesfully created a new command -> {}'.format(handle), 0)
            return self.commands
        return arguments

    def run(self):
        """ Initially start listening for chat events. """
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

kawaiibot = Bot()
