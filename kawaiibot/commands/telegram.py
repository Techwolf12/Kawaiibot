from kawaiibot.bot import kawaiibot

@kawaiibot.command('start')
def start(args):
    # This needs working on, telegram automatically issues this command when you talk to the bot for the first time.
    return 'This bot searches Imgur and Duckduckgo. It also has some other fun usages.'

@kawaiibot.command('commands')
def commands(args):
    return 'Imgur: /r DuckDuckGo: /ddg Tableflip: /flip Table back: /back Kaf image: /kaf'
