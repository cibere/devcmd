from typing import Literal

from discord.ext import commands

from .errors import InvalidArgument


class CodeBlockConvertor(commands.Converter):
    async def convert(self, ctx: commands.Context, raw_code: str):
        block = raw_code.removeprefix("```py").removesuffix("```")
        return block


class SyncConvertor(commands.Converter):
    async def convert(
        self, ctx: commands.Context, raw_argument: str
    ) -> Literal["global", "guild"]:
        arg = raw_argument.lower()

        if arg in ("global", "globally", "go", "*"):
            arg = "global"
        elif arg in ("guild", "server", "s", "~"):
            arg = "guild"
        else:
            raise InvalidArgument(ctx.command.name, raw_argument)  # type: ignore

        return arg
