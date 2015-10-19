from kawaiibot.bot import kawaiibot

@kawaiibot.command('start')
def start(args):
    # This needs working on, telegram automatically issues this command when
    # you talk to the bot for the first time.
    return 'This bot searches Imgur and DuckDuckGo. It also has some other fun usages. \
See /commands for everything I can do!'

@kawaiibot.command('commands')
def commands(args):
    return '''Imgur: /r <sub>\n
DuckDuckGo: /ddg <query>\n
Tableflip: /flip\n
Table back: /back\n
Kaf image: /kaf\n
DuckDuckGo bang: /!<bang> <query>'''
