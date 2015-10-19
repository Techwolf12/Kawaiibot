import os
import re
import sys
import logging
import telegram
import kawaiibot
import kawaiibot.commands
import kawaiibot.models

from kawaiibot import config, config_dir

# set up logging
log_format = '%(asctime)s [%(levelname)-5.5s] %(message)s'
logging.basicConfig(filename='{}/kawaiibot.log'.format(config_dir),
                    format=log_format, level=logging.INFO)

# stdout logger
console = logging.StreamHandler()
console.setFormatter(logging.Formatter(log_format))

logging.getLogger('').addHandler(console)

class Bot:
    commands = {}
    last_id = None
    disabled = []

    def __init__(self, attributes={}, prefix='/'):
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
            logging.info('Found command -> {}'.format(function.__name__))
            return self.commands
        return arguments

    def get_command(self, message):
        """
        Gets command from message
        @message Message that could contain a command
        """
        for command in self.commands:
            if re.match(r'^({0}$|{0}\ \w*)'.format(command), message):
                return self.commands[command]

        return False

    def run(self):
        """Initially start listening for chat events."""
        bot = telegram.Bot(token=config['telegram']['token'])
        # Disable Telegram API's logger to prevent spam
        bot.logger.disabled = True

        logging.info('Started bot')

        # TODO: Make this not hacky with tries.
        try:
            self.last_id = bot.getUpdates()[-1].update_id
        except IndexError:
            self.last_id = None
        except telegram.error.TelegramError as e:
            logging.critical('Failed to start bot: {} (is your Telegram token correct?)'.format(e))
            sys.exit(1)

        try:
            while True:
                for update in bot.getUpdates(offset=self.last_id, timeout=10):
                    if not update.message['text']:
                        continue

                    message = update.message.text[1::]
                    prefix = update.message.text[0]
                    command = self.get_command(message)

                    if prefix == self.prefix and command and command not in self.disabled:
                        bot.sendMessage(
                            chat_id=update.message.chat_id,
                            text=command(update)
                        )
                        self.last_id = update.update_id + 1
        except KeyboardInterrupt:
            logging.info('Stopped bot')

kawaiibot = Bot()
