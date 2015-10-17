import os
import sys
import json
import logging

try:
    import telegram
except ImportError as e:
    print('Failed to import one of the required modules. Did you run pip install -r requirements.txt?', file=sys.stderr)
    sys.exit(1)

if not os.path.isdir('~/.kawaiibot/'):
    try:
        os.mkdir(os.path.expanduser('~/.kawaiibot'))
    except FileExistsError:
        pass

try:
    with open(os.path.expanduser('~/.kawaiibot/config.json')) as f:
        config = json.load(f)
except FileNotFoundError as e:
    print('The required configuration file was not found. Are you sure that \'~/.kawaiibot/config.json\' exist?', file=sys.stderr)
    sys.exit(1)

log_format = "%(asctime)s [%(levelname)-5.5s] %(message)s"
logging.basicConfig(filename=os.path.expanduser('~/.kawaiibot/kawaiibot.log'),
                    format=log_format, level=logging.INFO)

# stdout logger
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(log_format))

logging.getLogger('').addHandler(console)

class Bot:
    commands = {}
    last_id = None

    def __init__(self, attributes={}, prefix='!'):
        self.__dict__ = attributes
        self.prefix = prefix

    def command(self, handle):
        """
        Create a new command entry, saved in self.commands
        @handle: The unique handle for the command call.
        """

        def arguments(function):
            if type(function).__name__ == 'function':
                self.commands[handle] = function
            else:
                logging.warning('{}.{} -> {}'.format(self.__class__.__name__, '__name__',
                         'Detected argument was not a function'))
            logging.info('Found command -> {}'.format(handle))
            return self.commands
        return arguments

    def run(self):
        """Initially start listening for chat events."""
        bot = telegram.Bot(token=config['telegram']['token'])
        # Disable Telegram API's logger to prevent spam
        bot.logger.disabled = True

        # TODO: Make this not hacky with tries.
        try:
            self.last_id = bot.getUpdates()[-1].update_id
        except IndexError:
            self.last_id = None

        try:
            while True:
                for update in bot.getUpdates(offset=self.last_id, timeout=10):
                    message = update.message.text[1::]
                    prefix = update.message.text[0]
                    instances = [{'name':n, 'found':n == message} for n in self.commands]

                    for instance in instances:
                        if (instance['found'] and prefix == self.prefix):
                            bot.sendMessage(
                                chat_id=update.message.chat_id,
                                text=self.commands[instance['name']]()
                            )
                            self.last_id = update.update_id + 1
        except KeyboardInterrupt:
            bot.sendMessage(chat_id=update.message.chat_id, text="Afk")

kawaiibot = Bot()
