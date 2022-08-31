from .core import VERSION, devcmd
from .utils import Paginator

async def setup(bot):
    await bot.add_cog(devcmd(bot))