from kawaiibot.bot import kawaiibot

ADMIN_USERNAMES = ('stevenyo', 'NULLSPHERE')

@kawaiibot.command("disabled")
def disabled(args):
    return ', '.join(kawaiibot.disabled)

@kawaiibot.command("disable")
def disable(args):
    n = []
    if args.message.from_user.username not in ADMIN_USERNAMES:
        return 'Fuck off. You can\'t do this'
    for s in args.message.text.split(' ')[1::]:
        if s not in kawaiibot.disabled:
            n.append(s)
            kawaiibot.disabled.append(s)
    if len(n) > 0:
        return "Disabled: {}".format(', '.join(n))
    else:
        return "Did nothing. Command already disabled."


