from kawaiibot.bot import kawaiibot

@kawaiibot.command('start')
def start(args):
    # This needs working on, telegram automatically issues this command when
    # you talk to the bot for the first time.
    return 'This bot searches Imgur and DuckDuckGo. It also has some other fun usages.'

@kawaiibot.command('hey')
def hey(args):
    return 'Hi!'

@kawaiibot.command('flip')
def flip(args):
    return '(╯°□°)╯︵ ┻━┻'

@kawaiibot.command('back')
def back(args):
    return '┬─┬ ノ( ゜-゜ノ)'
