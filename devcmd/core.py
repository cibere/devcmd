from discord.ext import commands

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
import ciberedev

from devcmd.sections import ALL_SECTIONS
from devcmd.sections.base_section import BaseSection

from .errors import NotAuthorized


class Devcmd(*ALL_SECTIONS, BaseSection):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.cdev = ciberedev.Client()

        found = [getattr(self, x) for x in dir(self) if x.startswith("cmd_")]
        for found_cmd in found:
            cmd_info = found_cmd.cmd_info
            cmd = commands.Command(
                found_cmd,
                name=cmd_info["name"],
                description=cmd_info["desc"],
                aliases=cmd_info["aliases"],
            )
            self.the_group.add_command(cmd)

    @commands.group(hidden=True, invoke_without_command=True, name="devcmd", description="the devcmd group", aliases=["dc", "dev"])  # type: ignore
    async def the_group(self, ctx: commands.Context):
        await self.send_info(ctx, "", "Devcmd is loaded")

    async def cog_load(self):
        await self.cdev.start()

    async def cog_unload(self):
        await self.cdev.close()

    async def cog_check(self, ctx: commands.Context) -> bool:
        if self.bot.owner_id:
            owners = [self.bot.owner_id]
        elif self.bot.owner_ids:
            owners = [self.bot.owner_ids]
        else:
            app = await self.bot.application_info()
            if app.team:
                self.bot.owner_ids = {m.id for m in app.team.members}
                owners = [self.bot.owner_ids]
            else:
                self.bot.owner_id = app.owner.id
                owners = [self.bot.owner_id]

        if ctx.author.id not in owners:
            raise NotAuthorized(str(ctx.author))
        else:
            return True


async def setup(bot: commands.Bot):
    await bot.add_cog(Devcmd(bot))  # type: ignore
