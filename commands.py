from bot import bot, config
from imgurpython import ImgurClient as Client
import random

@bot.command("hey")
def hey():
    return "Hi!"

@bot.command("kaf")
def kaf():
    client = Client(config['imgur']['id'], config['imgur']['secret'])
    random_sort = random.choice(['time', 'top'])
    items = client.subreddit_gallery('awwnime', sort=random_sort, window='week', page=0)

    return random.choice(items).link
