import discord
import asyncio

from discord.ext import commands
from tictactoe import *
from rps import *


class MiniGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def load_game(self, ctx):
        '''play games'''
        user_name = ctx.author.display_name

        await ctx.send(f'```BardBot reply {user_name} :```')
        bot = self.bot
        embed = discord.Embed(
            title='Choose game:\n',
            description='1. Tic-Tac-Toe! \n2. Rock-paper-scissors.',
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('❌')


        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '❌']
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Timed out.')
            return
        else:
            if str(reaction.emoji) == '1️⃣':
                await ctx.send('Starting Tic-Tac-Toe!')
                await tictactoe(ctx, bot)
            elif str(reaction.emoji) == '2️⃣':
                await ctx.send('Starting Rock-paper-scissors!')
                await rps(ctx, bot)
            else:
                await ctx.send('Cancelled.')


async def setup(bot):
    await bot.add_cog(MiniGames(bot))
