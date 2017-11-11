import discord
import random
import asyncio
from random import randrange,choice
from re import finditer
from time import time
from Brainfuck_python_interpreter.Interpreter import BF
from discord.utils import find


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
    await asyncio.sleep(0.5)
    await client.edit_message(mess, "[System] {} shutdowned".format(client.user.name))
    await client.close()

async def show_play(message, args):
    if len(args) > 0 :
        game = discord.Game(name=" ".join(args))
        await client.change_presence(game=game)
        await send(message,'Bot now playing : {0}'.format(" ".join(args)))
    else :
        await send(message,'Please Specify what\'s to play')

async def brain_fuck(message, args):

    if len(args) > 0:
        await send(message, "[Brainfuck]\t" + BF().compile(args[0]))

async def avatar(message ,args):
    if len(args) > 0 :
        author = message.server.get_member_named(args[0])
        if not author :
            await send(message, "{} doesn't exist, Trust me I've search everywhere".format(args[0]))
            return
    else :
        author = message.author
    await send (message, author.avatar_url)



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
                self.tryed += 1

                if guess in self.words :
                    #choice Impressive , Wow ...
                    await send(message,'{0} was correct!\n moving on'.format(guess))

                    for m in finditer(guess, self.words):
                        self.current[m.start()] = self.words[m.start()]

                else :
                    await send(message, '✖ ' + choice(['Sorry, it\'s just probability', 'Maybe next time?', 'Try again!']))

                await send(message, "  ".join(self.current))

                if('*' not in self.current):
                    await send(message, "Congrate! we have successfully consumed {0:0.2f}s of your time\n"
                                        "try : {}".format(time() - self.timestamp, self.tryed))
                    self.started = False

        elif self.started:
            await send(message, "  ".join(self.current))
        else :
            self.started = True
            self.words = choice(['python', 'javascript', 'php'])
            #print(self.words)
            self.current = ['*'] * len(self.words)
            self.timestamp = time()
            self.tryed = 0
            await send(message,'Hangman has just start\n\ntypes \'!hangman list\' to see sub-command')


class Music(Program) :

    def __init__(self):
        super(Music, self).__init__()

        self.queue = []
        self.voice_client = None
        self.ytdl_player = None


    async def join_channel(self, message):
        # Join voice channel
        if not self.voice_client:
            self.voice_client = client.voice_client_in(message.server)

            if not self.voice_client:
                voice_channel = find(lambda x: x.type == discord.ChannelType.voice, message.server.channels)
                self.voice_client = await client.join_voice_channel(voice_channel)

    def async_play_next(self, player):
        try:
            player.stop()
            print(type(player))
            coro = self.play_next()
            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)

            fut.result()
        except Exception as e:
            print(e)

    async def play_next(self,message=None):

        self.ytdl_player = await self.voice_client.create_ytdl_player("https://www.youtube.com/watch?v=" + self.queue[0],
                                                                      after=self.async_play_next)

        #await show_play(message, [self.ytdl_player.title])

        self.ytdl_player.start()

        self.queue.pop(0)



    async def main(self, message: discord.Message, args : list):

        try:

            await self.join_channel(message)
            print(self.voice_client)

            if len(args) > 0:

                if args[0] == 'queue':
                    #Change to complied thread in list????
                    out = ""
                    for i in self.queue:
                        out += "https://www.youtube.com/watch?v={}\n".format(i)
                    await send(message,out)
                elif args[0] =='clear':
                    self.queue = []
                else :
                    self.queue.append(args[0])
                    await send(message, "Music Added to queue")
                    print(self.queue)

                    if not self.ytdl_player:
                        await self.play_next(message)

            else:
                await send(message, '!music url [channel=first_voice_channel]')

        except Exception as e:
            await send(message, 'Error : {0}'.format(e))


commands = {'!info':(info,'Display Server Information'),
            '!hangman' : (Hangman(),'Play Hangman'),
            '!close' : (close,'Close and Exit'),
            '!show_play' : (show_play, 'Make bot play a \"Game\"'),
            '!send_all' : (send_all, 'Propel Message To All Channel'),
            '!brain_fuck' : (brain_fuck, 'Interpret brain-fuck command'),
            '!avatar' : (avatar, 'Get user avatar'),
            '!music' : (Music(), 'Play youtube music')}


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return

    cmd = message.content.strip().split(" ")
    func = commands.get(cmd[0], False)

    if func:
        if isinstance(func[0],Program):
            await func[0].main(message, cmd[1:])
        else :
            await func[0](message, cmd[1:])
    elif cmd[0] == '!list':

        out = ""
        client.send_typing(message.channel)
        for k in commands :
            out += "{0}\t→\t{1}\n".format(k, commands[k][1])
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
#  create Info.py in same dictionary and have varaible 'toekn' be your string token
import Info
client.run(Info.token)