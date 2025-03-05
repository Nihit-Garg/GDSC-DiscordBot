import discord
from discord.ext import commands
import json
import asyncio
from utils.storage import save_json, load_json

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = load_json('data/polls.json')

    @commands.command(name='createpoll')
    async def create_poll(self, ctx, question: str, *options):
        """Create a new poll. Usage: !createpoll "Question" "Option1" "Option2" ..."""
        if len(options) < 2:
            await ctx.send("Please provide at least 2 options for the poll.")
            return

        poll_id = str(len(self.polls) + 1)
        poll = {
            'question': question,
            'options': list(options),
            'votes': {str(i): [] for i in range(len(options))},
            'creator': ctx.author.id
        }

        self.polls[poll_id] = poll
        save_json('data/polls.json', self.polls)

        # Create embed for poll
        embed = discord.Embed(title="📊 Poll", description=question, color=0x00ff00)
        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i+1}", value=option, inline=False)

        poll_msg = await ctx.send(embed=embed)
        
        # Add reaction options
        for i in range(len(options)):
            await poll_msg.add_reaction(f"{i+1}\u20e3")

    @commands.command(name='pollresults')
    async def poll_results(self, ctx, poll_id: str):
        """Show results for a specific poll"""
        if poll_id not in self.polls:
            await ctx.send("Poll not found.")
            return

        poll = self.polls[poll_id]
        embed = discord.Embed(title="📊 Poll Results", description=poll['question'], color=0x00ff00)
        
        for i, option in enumerate(poll['options']):
            votes = len(poll['votes'][str(i)])
            embed.add_field(
                name=f"Option {i+1}: {option}",
                value=f"Votes: {votes}",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        # Check if reaction is on a poll
        message = reaction.message
        for poll_id, poll in self.polls.items():
            if str(reaction.emoji)[0].isdigit():
                option_num = int(str(reaction.emoji)[0]) - 1
                if option_num < len(poll['options']):
                    if user.id not in poll['votes'][str(option_num)]:
                        poll['votes'][str(option_num)].append(user.id)
                        save_json('data/polls.json', self.polls)

async def setup(bot):
    await bot.add_cog(Polls(bot))
