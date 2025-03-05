import os
import discord
from discord.ext import commands
import google.generativeai as genai

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')

    @commands.command(name='chat')
    async def chat(self, ctx, *, message: str):

        try:
            response = await self.model.generate_content_async(message)
            # Split response into chunks if it's too long
            if len(response.text) > 2000:
                chunks = [response.text[i:i+2000] for i in range(0, len(response.text), 2000)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(response.text)
        except Exception as e:
            await ctx.send(f"Error processing your request: {str(e)}")

async def setup(bot):
    await bot.add_cog(Chat(bot))
