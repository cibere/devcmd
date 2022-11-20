import inspect

from discord.ext import commands

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
import logging

import ciberedev

from devcmd.sections import ALL_SECTIONS

logger = logging.getLogger("devcmd")
logger.setLevel(logging.INFO)


class Devcmd(*ALL_SECTIONS):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.cdev = ciberedev.Client()

        found = [getattr(self, x) for x in dir(self) if x.startswith("cmd_")]
        for found_cmd in found:
            cmd_info = found_cmd.cmd_info
            cmd = commands.Command(
                name=cmd_info["name"],  # type: ignore
                description=cmd_info["desc"],
                aliases=cmd_info["aliases"],
            )
            self.the_group.add_command(cmd)

    @commands.group(hidden=True, invoke_without_command=True, name="devcmd", description="the devcmd group", aliases=["dc", "dev"])  # type: ignore
    async def the_group(self, ctx: commands.Context):
        await ctx.send("Devcmd is loaded")

    async def cog_load(self):
        await self.cdev.start()

    async def cog_unload(self):
        await self.cdev.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(Devcmd(bot))  # type: ignore
