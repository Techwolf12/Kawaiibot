from kawaiibot.bot import kawaiibot
from kawaiibot.models import duckduckgo
import logging

@kawaiibot.command('ddg')
def duck(args):
    arg = ''.join(args.message.text.split(' ')[1::])
    user = args.message.from_user.username if args.message.from_user.username else args.message.from_user.first_name

    if not arg:
        return '@{} I can\'t hear you -- I\'m using the scrambler.'.format(user)

    return '@{} {}'.format(user, duckduckgo.search(arg))

