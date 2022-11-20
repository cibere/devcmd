import os
import sys

import discord
from discord.ext import commands

from .base_section import BaseSection, command


class SystemSection(BaseSection):
    @command(name="restart", description="Restarts the bot")
    async def cmd_restart(self, ctx: commands.Context, _: str = ""):
        await ctx.channel.typing()

        await self.send_success(ctx, "Restarting now...")
        os.execv(sys.executable, ["python"] + sys.argv)

    @command(
        name="shutdown",
        aliases=["logout"],
        description="Shutsdown/logs out the bot",
    )
    async def cmd_shutdown(self, ctx: commands.Context, _: str = ""):
        await ctx.channel.typing()

        await self.send_success(ctx, "Logging out...")
        await ctx.bot.close()

    @command(name="os", description="lets you execute stuff in your console")
    async def cmd_os(self, ctx: commands.Context, query: str):
        pass
