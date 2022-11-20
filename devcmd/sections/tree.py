import discord
from discord.ext import commands

from ..converters import SyncConvertor
from .base_section import BaseSection, command

sync_description = """
lets you sync your slash commands

works like this:
sync global -> syncs globally
sync guild -> syncs to the current guild

accepted versions of global:
global, globally, go

accepted versions of guild:
guild/gu/server/s"""


class TreeSection(BaseSection):
    @command(name="sync", description=sync_description)
    async def sync(self, ctx: commands.Context, scope: SyncConvertor):
        await ctx.typing()

        if scope == "global":
            cmds = await ctx.bot.tree.sync()
        else:
            cmds = await ctx.bot.tree.sync(guild=ctx.guild)

        em = discord.Embed(
            description=f'Synced {len(cmds)} {"globally" if scope == "global" else "to the current guild"}',
            color=discord.Color.blue(),
        )
        await ctx.send(embed=em)
