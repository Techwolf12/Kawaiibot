from kawaiibot.bot import kawaiibot
import logging

admin_usernames = ['stevenyo', 'NULLSPHERE']

@kawaiibot.command('disabled')
def disabled(args):
    return ', '.join(kawaiibot.disabled)

@kawaiibot.command('disable')
def disable(args):
    n = []
    if args.message.from_user.username not in admin_usernames:
        return 'You can\'t do that'
    for s in args.message.text.split(' ')[1::]:
        if s not in kawaiibot.disabled:
            n.append(s)
            kawaiibot.disabled.append(s)
            logging.info('Command \'{}\' by {}'.format(s, args.message.from_user.username))
    if len(n) > 0:
        return 'Disabled: {}'.format(', '.join(n))
    else:
        return 'Did nothing. Command already disabled.'


