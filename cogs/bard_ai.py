import discord
import os
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from bardapi import Bard


load_dotenv()
BARDAPI_KEY = os.getenv('BARDAPI_KEY')
CHANNEL_ID = int(os.getenv('CHANNEL_DISCORD_ID'))


bard = Bard(token=BARDAPI_KEY)

class BardAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question):
        ''' Ask BARD AI a question '''
        
        try:
            user_name = ctx.author.display_name

            await ctx.send(f'```BardBot reply {user_name} :```')

            # response = bard.get_answer(prompt)

            # response = bard.get_answer(prompt)['content']
            # await ctx.send(response)

            # Split the content into lines
            # lines = response.split('\n')
            # for line in lines:
            #     if line.strip():
            #         await ctx.send(line)

            # print(urls)

            response = bard.get_answer(question)
            content = response.get('content', '')
            image_urls_set = response.get('images', list())
            image_urls = list(image_urls_set)
            lines = content.split('\n')

            # print(response)
            # print(*lines)
            # print(*image_urls)

            j = 0

            for i in range(len(lines)):
                if j < len(image_urls) and lines[i].strip() and lines[i].startswith("[Image"):
                    await ctx.send(image_urls[j])
                    j += 1
                if lines[i].strip() and not lines[i].startswith("[Image"):
                    await ctx.send(lines[i])
            # check = False
            # channel = self.bot.get_channel(CHANNEL_ID)
            # await channel.send(f"Sure 😊! Waiting for a moment...")
            # response = bard.get_answer(question)["content"]
            # if len(response) < 2000:
            #     await ctx.send(response)
            # else:
            #     answer = response.split("\n")
            #     images = list(bard.get_answer(question)["images"])
            #     for paragraph in answer:
            #         if paragraph == "":
            #             continue
            #         elif paragraph.startswith("[Image"):
            #             check = True
            #         await ctx.send(paragraph)
            #     if check:
            #         await ctx.send("Some images I can find: ")
            #         for image in images:
            #             await ctx.send(image)
        except Exception as e:
            error_message = (
                f"**Error 😣:**\n\n"
                f"```\n"
                f"{str(e)}\n"
                f"```\n"
            )
            await ctx.send(error_message)


async def setup(bot):
    await bot.add_cog(BardAI(bot))
