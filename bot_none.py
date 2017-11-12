import discord

client = discord.Client()

async def send(message: discord.Message, text: str, *args: list, type=True):
    if type : await client.send_typing(message.channel)
    return await client.send_message(message.channel, text,*args)

async def func(message, args):
    if len(args) > 0:
        await send(message, args[0])

class Program :

    def __init__(self):
        pass



commands = {'!func':(func, 'display first argument')}



@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return


    cmd = message.content.strip().split()
    func = commands.get(cmd[0], False)

    if func != False:
        if isinstance(func[0],Program):
            await func[0].main(message, cmd[1:])
        else :
            await func[0](message, cmd[1:])
    elif cmd[0] == '!list':
        out = ""
        client.send_typing(message.channel)
        for k in commands :
            out += "{0}\t→\t{1:>10}\n".format(k, commands[k][1])
        await send(message, out , type=False)

silent = True
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    if not silent:
        for c in client.get_all_channels():
            if c.type == discord.ChannelType.text :
                await client.send_message(c,"{} is now online !!!!\nYou can view code at {}".format(client.user.name,
                                                                            'https://github.com/thanadolps/dis-bot'))


#to use it with your bot either
#  remove 'Import Info' and replace Info.token with your bot token
#  create Info.py in same dictionary and have varaible 'token' be your string token
from Testing import Info

client.run(Info.token)