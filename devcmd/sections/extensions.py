import traceback
from typing import Optional

import ciberedev
import discord
from discord.ext import commands

from ..utils import filter_text


class ExtensionsSection(commands.Cog):
    cdev: ciberedev.Client

    @commands.command(
        parent="devcmd",
        name="load",
        aliases=["reload", "unload"],
        description="loads/unloads/reloads an extension",
    )
    async def load(self, ctx: commands.Context, extension: Optional[str] = None):
        await ctx.channel.typing()
        if ctx.invoked_with == "reload" and extension == None:
            extension = "devcmd"

        elif extension == None:
            return await ctx.send(
                "Extension can only be `None` with reload. Not load/unload"
            )

        if ctx.invoked_with == "unload":
            try:
                await ctx.bot.unload_extension(extension)
                em = discord.Embed(
                    title="",
                    description=f"`✅ unloaded {extension}`",
                    color=discord.Color.green(),
                )
                return await ctx.send(embed=em)
            except Exception:
                em = discord.Embed(
                    title="Error",
                    description=f"""```py\n{traceback.format_exc()}\n```""",
                    color=discord.Color.red(),
                )
                msg = await ctx.author.send(embed=em)
                em2 = discord.Embed(
                    title="",
                    description=f"[Error has been sent to your dms]({msg.jump_url})",
                    color=discord.Color.green(),
                )
                return await ctx.send(embed=em2)
        try:
            await ctx.bot.unload_extension(extension)
            text = "reloaded"
        except Exception:
            text = "loaded"
        try:
            await ctx.bot.load_extension(extension)
            em = discord.Embed(
                title="",
                description=f"`✅ {text} {extension}`",
                color=discord.Color.green(),
            )
            await ctx.send(embed=em)
        except Exception:
            error = traceback.format_exc()
            error = filter_text(error)
            try:
                em = discord.Embed(
                    title="Error",
                    description=f"```py\n{error}\n```",
                    color=discord.Color.red(),
                )
                msg = await ctx.author.send(embed=em)
                em2 = discord.Embed(
                    title="",
                    description=f"[Error has been sent to your dms]({msg.jump_url})",
                    color=discord.Color.orange(),
                )
                await ctx.send(embed=em2)
            except discord.errors.Forbidden:
                em = discord.Embed(
                    title="Error",
                    description=f"```py\n{error}\n```",
                    color=discord.Color.red(),
                )
                em2 = discord.Embed(
                    title="",
                    description=f"I am unable to send you a dm, so error will be sent here.",
                    color=discord.Color.red(),
                )
                await ctx.send(embeds=[em, em2])
            except:
                paste = await self.cdev.create_paste(str(error))
                em = discord.Embed(
                    title="Error",
                    description=f"(Error is too long to send here, so it was sent here)[{str(paste)}]",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=em)

    @commands.command(name="remove", description="removes a cog", parent="devcmd")
    async def remove_cog(self, ctx, cog_name: str):
        cogs = [str(cog) for cog in ctx.bot.cogs]
        if cog_name not in cogs:
            return await ctx.send(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description=f"`{cog_name}` is not a cog that is currently loaded",
                )
            )
        await ctx.bot.remove_cog(cog_name)
        await ctx.send(
            embed=discord.Embed(
                color=discord.Color.green(),
                description=f"Successfully removed `{cog_name}`",
            )
        )

    @commands.command(name="cogs", description="lists all loaded cogs", parent="devcmd")
    async def cogs(self, ctx):
        cogs = [f"`{str(cog)}`" for cog in ctx.bot.cogs]
        em = discord.Embed(
            title="Loaded Cogs", color=discord.Color.blue(), description=", ".join(cogs)
        )
        await ctx.send(embed=em)
