import os
import sys

from discord.ext import commands

from ..utils import RedirectedStdout
from .base_section import BaseSection, command


class SystemSection(BaseSection):
    @command(name="restart", description="Restarts the bot")
    async def cmd_restart(self, ctx: commands.Context, _: str = ""):
        await ctx.channel.typing()

        if hasattr(ctx.bot, "shutdown_check"):
            if not bool(ctx.bot.shutdown_check()):
                return await self.send_error(ctx, "Restart Check Failed")

        await self.send_success(ctx, "Restarting now...")
        os.execv(sys.executable, ["py"] + sys.argv)

    @command(
        name="shutdown",
        aliases=["logout"],
        description="Shutsdown/logs out the bot",
    )
    async def cmd_shutdown(self, ctx: commands.Context, _: str = ""):
        await ctx.channel.typing()

        if hasattr(ctx.bot, "shutdown_check"):
            if not bool(ctx.bot.shutdown_check()):
                return await self.send_error(ctx, "Shutdown Check Failed")

        await self.send_success(ctx, "Logging out...")
        await ctx.bot.close()

    @command(name="os", description="lets you execute stuff in your console")
    async def cmd_os(self, ctx: commands.Context, query: str):
        async with RedirectedStdout() as opt:
            os.system(query)
            await self.send_info(ctx, "OS Output", str(opt))
