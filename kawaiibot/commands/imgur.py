from kawaiibot import config
from kawaiibot.bot import kawaiibot
from imgurpython import ImgurClient
import logging
import random

sub_blacklist = ['traps']

try:
    imgur_client = ImgurClient(config['imgur']['id'], config['imgur']['secret'])
except KeyError as e:
    logging.error('Missing imgur[{}] in configuration file. Disabling imgur commands'.format(e) +
                  ' (see config.json.example for an example)')

@kawaiibot.command('r')
def r(args):
    arg = args.message.text.split(' ')[1] if len(args.message.text.split(' ')) > 1 else 'all'
    user = args.message.from_user.username if args.message.from_user.username else arg.message.from_user.first_name

    random_sort = random.choice(['time', 'top'])

    if arg in sub_blacklist:
        return '@{} You speak an infinite deal of nothing'.format(user)

    try:
        items = imgur_client.subreddit_gallery(arg, sort=random_sort, window='week', page=0)
    except Exception as e:
        logging.info('ImgurClient: {}'.format(e))
        return '@{} I can\'t help you at this time. Try again later.'.format(user)

    if not items:
        return 'My pet ferret can type better than you!'

    return '@{} {}'.format(user, random.choice(items).link)

@kawaiibot.command('kaf')
def kaf(args):
    random_sort = random.choice(['time', 'top'])
    user = args.message.from_user.username if args.message.from_user.username else arg.message.from_user.first_name
    try:
        items = sub_blacklist.subreddit_gallery('awwnime', sort=random_sort, window='week', page=0)
    except Exception:
        return '@{} I can\'t help you at this time. Try again later.'.format(user)

    return '@{} {}'.format(user, random.choice(items).link)
