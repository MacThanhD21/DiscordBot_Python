import discord
import os
import asyncio
import pytz
from apikeys import *

from dataclasses import dataclass
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import timedelta
from dataclasses import dataclass

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_DISCORD_ID'))


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

session = Session()

MAX_SESSION_TIME_MINUTES = 45


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"{bot.user.name} has connected to channel!")


@bot.event
async def on_member_join(member):
    print(f"Member {member.name} just have joined the server.")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to my channel!")


@bot.event
async def on_member_remove(member):
    print(f"Member {member.name} left the server.")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Goodbye {member.name}. See you later!")



@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=3)
async def break_reminder():

    # Ignore the first execution of this command.
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes.")


VIETNAM_TZ = pytz.timezone('Asia/Ho_Chi_Minh')


@bot.command()
async def start(ctx):

    '''Bắt đầu phiên làm việc của Người Dùng'''

    user_name = ctx.author.display_name

    await ctx.send(f'```BardBot reply {user_name} :```')
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.astimezone(
        VIETNAM_TZ).strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")


@bot.command()
async def end(ctx):
    '''Kết Thúc Phiên Làm Việc của người dùng'''
    user_name = ctx.author.display_name

    await ctx.send(f'```BardBot reply {user_name} :```')
    if not session.is_active:
        await ctx.send("No active session to end.")
        return

    session.is_active = False
    human_readable_end_time = ctx.message.created_at.astimezone(
        VIETNAM_TZ).strftime("%H:%M:%S")

    await ctx.send(f"Session ended at {human_readable_end_time}. ")
    break_reminder.cancel()


@bot.command()
async def cls(ctx, ammount=""):
    ''' Clear messages '''
    if ammount == "" or ammount == "all":
        await ctx.channel.purge(limit=None)
    else:
        await ctx.channel.purge(limit=int(ammount))


async def load():
    for fileName in os.listdir("./cogs"):
        if fileName.endswith(".py"):
            await bot.load_extension(f"cogs.{fileName[:-3]}")


async def main():
    await load()
    await bot.start(BOT_TOKEN)


asyncio.run(main())
