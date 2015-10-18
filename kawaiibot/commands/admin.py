from kawaiibot.bot import kawaiibot
import logging

admin_usernames = ['stevenyo', 'NULLSPHERE']

@kawaiibot.command('disabled')
def disabled(args):
    disabled = [func.__name__ for func in kawaiibot.disabled]
    return ', '.join(disabled) if disabled else 'Nothing is disabled'

@kawaiibot.command('disable')
def disable(args):
    n = []
    if args.message.from_user.username not in admin_usernames:
        return 'You can\'t do that'

    for s in args.message.text.split(' ')[1::]:
        command = kawaiibot.get_command(s)
        if command not in kawaiibot.disabled:
            n.append(s)
            kawaiibot.disabled.append(command)
            logging.info('Command \'{}\' disabled by {}'.format(s, args.message.from_user.username))
    if len(n) > 0:
        return 'Disabled: {}'.format(', '.join(n))
    else:
        return 'Did nothing. Command already disabled.'

@kawaiibot.command('enable')
def enable(args):
    n = []
    if args.message.from_user.username not in admin_usernames:
        return 'You can\'t do that'

    for s in args.message.text.split(' ')[1::]:
        if command in kawaiibot.disabled:
            n.append(command.__name__)
            kawaiibot.disabled.remove(command)
            logging.info('Command \'{}\' enabled by {}'.format(s, args.message.from_user.username))
    if len(n) > 0:
        return 'Enabled: {}'.format(', '.join(n))
    else:
        return 'Did nothing. Command already enabled.'


