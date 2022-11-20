import inspect
import io

import discord
from discord.ext import commands

from .base_section import BaseSection, command


class SourceSection(BaseSection):
    @command(
        name="source",
        aliases=["src"],
        description="Gives the source code for the specified command",
    )
    async def cmd_source(self, ctx, *, command_name: str):
        await ctx.channel.typing()
        command = ctx.bot.get_command(command_name)
        if not command:
            await ctx.send(f"Command `{command_name}` not found")
            return
        try:
            source_lines, _ = inspect.getsourcelines(command.callback)
        except:
            return await ctx.send(f"I could not find the source code for `{command}`.")
        source_text = "".join(source_lines)
        await ctx.send(
            file=discord.File(
                filename="source.py", fp=io.BytesIO(source_text.encode("utf-8"))
            )
        )

    @command(
        name="file",
        description="Sends the code for the specified file",
    )
    async def cmd_file(self, ctx, file: str):
        await ctx.channel.typing()
        try:
            with open(file, "r", encoding="utf-8") as f:
                code = str(f.read())
        except FileNotFoundError:
            return await ctx.send(f"I could not file a file at `{file}`")

        name = file.split("/")
        name = name[len(name) - 1]
        await ctx.send(
            file=discord.File(filename=name, fp=io.BytesIO(code.encode("utf-8")))
        )
