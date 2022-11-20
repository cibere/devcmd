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


class Devcmd(*ALL_SECTIONS):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.cdev = ciberedev.Client()

        def check(x):
            if inspect.isfunction(x):
                return hasattr(x, "cmd_info")
            else:
                return False

        found = inspect.getmembers(self, predicate=check)
        for found_cmd in found:
            cmd_info = found_cmd[1].cmd_info
            cmd = commands.Command(
                name=cmd_info["name"],  # type: ignore
                description=cmd_info["description"],
                aliases=cmd_info["description"],
            )
            self.the_group.add_command(cmd)
            logging.info(f"Added command: {cmd_info['name']}")

    @commands.group(hidden=True, invoke_without_command=True, name="devcmd", description="the devcmd group", aliases=["dc", "dev"])  # type: ignore
    async def the_group(self, ctx: commands.Context):
        await ctx.send("Devcmd is loaded")

    async def cog_load(self):
        await self.cdev.start()

    async def cog_unload(self):
        await self.cdev.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(Devcmd(bot))  # type: ignore
