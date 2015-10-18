from kawaiibot import config
from kawaiibot.bot import kawaiibot
from imgurpython import ImgurClient
import logging
import random

IMGUR_CLIENT = ImgurClient(config['imgur']['id'], config['imgur']['secret'])
SUB_BLACKLIST = ['traps']

@kawaiibot.command("hey")
def hey(args):
    return "Hi!"

@kawaiibot.command("sub")
def sub(args):
    arg = args.split(" ")[1] if len(args.split(" ")) > 1 else None
    random_sort = random.choice(['time', 'top'])

    if arg in SUB_BLACKLIST:
        return "You speak an infinite deal of nothing"

    try:
        items = IMGUR_CLIENT.subreddit_gallery(arg, sort=random_sort, window='week', page=0)
    except Exception as e:
        logging.info("ImgurClient: {}".format(e))
        return "I can't help you at this time. Try again later."

    if not items:
        return "My pet ferret can type better than you!"

    return random.choice(items).link

@kawaiibot.command("kaf")
def kaf(args):
    random_sort = random.choice(['time', 'top'])
    try:
        items = IMGUR_CLIENT.subreddit_gallery('awwnime', sort=random_sort, window='week', page=0)
    except Exception:
        return "I can't help you at this time. Try again later."

    return random.choice(items).link
