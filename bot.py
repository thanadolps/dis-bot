import discord
import random
import asyncio
from random import randrange,choice
from re import finditer
from time import time

client = discord.Client()

async def send(message: discord.Message, text: str, *args: list, type=True) -> discord.Message:
    if type : await client.send_typing(message.channel)
    return await client.send_message(message.channel, text,*args)

async def info(message,args):
    await client.send_message(message.channel, "Server\t->\t{0.name}\n"
                                               "Create \t->\t{0.created_at}".format(message.server))

async def send_all(message,args):
    for chan in message.server.channels:
        if chan.type == discord.ChannelType.text:
            await client.send_message(chan, str(message.author) + ':speech_left:\n' + " ".join(args))

async def close(message: discord.Message, args: list) -> None:
    mess = await send(message, "no! please don't do that, don't kill me")
    await client.edit_message(mess, "[System] {} shutdowned".format(client.user.name))
    await client.close()

async def show_play(message, args):
    if len(args) > 0 :
        game = discord.Game(name=" ".join(args))
        await client.change_presence(game=game)
        await send(message,'Bot now playing : {0}'.format(" ".join(args)))
    else :
        await send(message,'Please Specify what\'s to play')

class Program :

    def __init__(self):
        pass


class Hangman(Program) :

    def __init__(self):
        super().__init__()
        self.started = False

    #Where's the function design??????
    async def main(self,message,args):

        if(len(args) > 0):


            if(args[0] == 'list'):
                await send(message,"list \t→\t show sub-command \n"
                                   "stop \t→\t stop hangman prematurely\n"
                                   "{guess} \t→\t (default) guess current word")

            elif(args[0] == 'stop'):
                if not self.started:
                    await send(message, 'Hangman hasn\'t started yet')
                else:
                    self.started = False
                    await send(message, 'Bot\'s Stopping')
            else:
                if(len(args[0]) > 1):
                    await send(message,"[Warning]\tIt's RECOMMEND to use single CHARACTER, NOT a whole STRING")
                guess = args[0][0]

                if guess in self.words :
                    #choice Impressive , Wow ...
                    await send(message,'{0} was correct!\n moving on'.format(guess))

                    for m in finditer(guess, self.words):
                        self.current[m.start()] = self.words[m.start()]

                else :
                    await send(message, '✖ ' + choice(['Sorry, it\'s just probability', 'Maybe next time?', 'Try again!']))

                await send(message, "  ".join(self.current))

                if('*' not in self.current):
                    await send(message, "Congrate! we have successfully consumed {0:0.2f}s of your time".format(time() - self.timestamp))
                    self.started = False

        elif self.started:
            await send(message, "  ".join(self.current))
        else :
            self.started = True
            self.words = choice(['python', 'javascript', 'php'])
            #print(self.words)
            self.current = ['*'] * len(self.words)
            self.timestamp = time()
            await send(message,'Hangman has just start\n\ntypes \'!hangman list\' to see sub-command')



commands = {'!info':(info,'Display Server Information'),
            '!hangman' : (Hangman(),'Play Hangman'),
            '!close' : (close,'Close and Exit'),
            '!show_play' : (show_play, 'Make bot play a \"Game\"'),
            '!send_all' : (send_all, 'Propel Message To All Channel')}

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return


    cmd = message.content.strip().split();
    func = commands.get(cmd[0], False);

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

    if False:
        if message.author == client.user:
            return

        if message.content.startswith('$guess'):
            await client.send_message(message.channel, 'Guess a number between 1 to 10')

            def guess_check(m):
                return m.content.isdigit()

            guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
            answer = random.randint(1, 10)
            if guess is None:
                fmt = 'Sorry, you took too long. It was {}.'
                await client.send_message(message.channel, fmt.format(answer))
                return
            if int(guess.content) == answer:
                await client.send_message(message.channel, 'You are right!')
            else:
                await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for c in client.get_all_channels():
        if c.type == discord.ChannelType.text :
            await client.send_message(c,"{} is now online !!!!".format(client.user.name))

#to use it with your bot either
#  remove 'Import Info' and replace Info.token with your bot token
#  create Info.py in same dictionary and have varaible 'toekn' be your string token
import Info
client.run(Info.token)