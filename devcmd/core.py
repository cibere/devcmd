from discord.ext import commands

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
import ciberedev

from .sections import ALL_SECTIONS


class Devcmd(*ALL_SECTIONS):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cdev = ciberedev.Client()

    async def cog_load(self):
        await self.cdev.start()

    async def cog_unload(self):
        await self.cdev.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(Devcmd(bot))  # type: ignore
