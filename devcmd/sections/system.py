import os
import sys

import discord
from discord.ext import commands


class SystemSection(commands.Cog):
    @commands.command(name="restart", description="Restarts the bot", parent="devcmd")
    async def restart(self, ctx):
        await ctx.channel.typing()
        embed = discord.Embed(color=discord.Color.green(), title="Restarting now...")
        await ctx.send(embed=embed)
        os.execv(sys.executable, ["python"] + sys.argv)

    @commands.command(
        name="shutdown",
        aliases=["logout"],
        description="Shutsdown/logs out the bot",
        parent="devcmd",
    )
    async def shutdown(self, ctx):
        await ctx.channel.typing()
        embed = discord.Embed(color=discord.Color.green(), title="Logging out...")
        await ctx.reply(embed=embed)
        await ctx.bot.close()
