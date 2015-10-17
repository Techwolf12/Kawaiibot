from kawaiibot.models.bot import kawaiibot
from imgurpython import ImgurClient as Client
import random

@kawaiibot.command("hey")
def hey():
    return "Hi!"

@kawaiibot.command("kaf")
def kaf():
    client = Client(bot.config['imgur']['id'], bot.config['imgur']['secret'])
    random_sort = random.choice(['time', 'top'])
    items = client.subreddit_gallery('awwnime', sort=random_sort, window='week', page=0)

    return random.choice(items).link
