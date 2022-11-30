import traceback
from typing import Optional

import discord
from discord.ext import commands

from ..utils import filter_text
from .base_section import BaseSection, command


class ExtensionsSection(BaseSection):
    bot: commands.Bot

    @command(
        name="load",
        aliases=["reload", "unload"],
        description="loads/unloads/reloads an extension",
    )
    async def cmd_load(self, ctx: commands.Context, extension: Optional[str] = None):
        await ctx.channel.typing()

        if ctx.invoked_with == "reload" and extension == None:
            extension = "devcmd"
        if extension == None:
            return await self.send_error(
                ctx, "Extension can only be `None` with reload. Not load/unload"
            )
        if ctx.invoked_with == "unload":
            try:
                await ctx.bot.unload_extension(extension)
                return await self.send_success(ctx, f"`✅ unloaded {extension}`")
            except Exception:
                msg = await self.send_error(
                    ctx.author, f"""```py\n{traceback.format_exc()}\n```"""
                )
                await self.send_error(
                    ctx, f"[Error has been sent to your dms]({msg.jump_url})"
                )
        try:
            await ctx.bot.unload_extension(extension)
            text = "reloaded"
        except Exception:
            text = "loaded"
        try:
            await ctx.bot.load_extension(extension)
            await self.send_success(ctx, f"`✅ {text} {extension}`")
        except Exception:
            error = traceback.format_exc()
            error = filter_text(error)
            try:
                msg = await self.send_error(ctx.author, f"```py\n{error}\n```")
                await self.send_error(
                    ctx, f"[Error has been sent to your dms]({msg.jump_url})"
                )
            except discord.errors.Forbidden:
                await self.send_error(
                    ctx, f"I am unable to send you a dm\n\n```py\n{error}\n```"
                )

    @command(name="remove", description="removes a cog")
    async def cmd_remove(self, ctx: commands.Context, cog_name: str):
        cogs = [str(cog) for cog in ctx.bot.cogs]
        if cog_name not in cogs:
            return await self.send_error(
                ctx, f"`{cog_name}` is not a cog that is currently loaded"
            )

        await ctx.bot.remove_cog(cog_name)
        await self.send_success(ctx, f"Successfully removed `{cog_name}`")

    @command(name="cogs", description="lists all loaded cogs")
    async def cmd_cogs(self, ctx: commands.Context, _: str = ""):
        cogs = [f"`{str(cog)}`" for cog in ctx.bot.cogs]
        await self.send_info(ctx, "Loaded Cogs", ", ".join(cogs))
