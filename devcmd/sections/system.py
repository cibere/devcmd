import os
import sys

import discord
from discord.ext import commands

from .base_section import BaseSection


class SystemSection(BaseSection):
    @commands.command(name="restart", description="Restarts the bot")
    async def cmd_restart(self, ctx):
        await ctx.channel.typing()
        embed = discord.Embed(color=discord.Color.green(), title="Restarting now...")
        await ctx.send(embed=embed)
        os.execv(sys.executable, ["python"] + sys.argv)

    @commands.command(
        name="shutdown",
        aliases=["logout"],
        description="Shutsdown/logs out the bot",
    )
    async def cmd_shutdown(self, ctx):
        await ctx.channel.typing()
        embed = discord.Embed(color=discord.Color.green(), title="Logging out...")
        await ctx.reply(embed=embed)
        await ctx.bot.close()
