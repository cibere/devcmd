import io
import os
import sys
import time
from io import StringIO
from textwrap import indent
from traceback import format_exc as geterr

import aiohttp
import discord
import import_expression
from discord.ext import commands

from ..converters import CodeBlockConvertor
from ..utils import filter_text


class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io.getvalue()  # type: ignore


class ReplSection(commands.Cog):
    async def _handle_eval(self, env, ctx, function, as_generator=False):
        with RedirectedStdout() as otp:
            try:
                import_expression.exec(function, env)
                func = env["func"]
                ping = time.monotonic()
                if not as_generator:
                    res = await func()
                else:
                    res = None
                    async for x in func():
                        print(x)
            except Exception as e:
                if (
                    str(e)
                    == "object async_generator can't be used in 'await' expression"
                ):
                    return await self._handle_eval(env, ctx, function, True)
                err = geterr()
                try:
                    err = err.split("return compile(source, filename, mode, flags,")[1]
                except:
                    try:
                        err = err.split("res = await func()")[1]
                    except:
                        pass
                msg = f"n```py\n{err}\n```"
                msg = filter_text(msg)
                errorEm = discord.Embed(
                    title="Eval Error", description=msg, color=discord.Color.red()
                )
                await ctx.send(embed=errorEm)
                return
            ping = time.monotonic() - ping
            ping = ping * 1000
            if res:
                msg = f"```py\n{res}\n{otp}\n```"
                msg = filter_text(msg)
                returnedEm = discord.Embed(
                    title="Returned", description=msg, color=discord.Color.green()
                )
                returnedEm.set_footer(text=f"Finished in {ping}ms")
                await ctx.send(embed=returnedEm)
            else:
                msg = f"```py\n{otp}\n```"
                msg = filter_text(msg)
                outputEm = discord.Embed(
                    title="Output", description=msg, color=discord.Color.green()
                )
                outputEm.set_footer(text=f"Finished in {ping}ms")
                await ctx.send(embed=outputEm)

    @commands.command(
        name="eval",
        aliases=["```py", "```", "py", "python", "run", "exec", "execute"],
        description="Evaluates the given code",
        parent="devcmd",
    )
    async def _eval(self, ctx, *, code: CodeBlockConvertor):
        await ctx.channel.typing()
        env = {
            "ctx": ctx,
            "bot": ctx.bot,
            "message": ctx.message,
            "author": ctx.author,
            "guild": ctx.guild,
            "channel": ctx.channel,
            "discord": discord,
            "commands": commands,
            "os": os,
            "io": io,
            "sys": sys,
            "aiohttp": aiohttp,
        }

        function = "async def func():\n" + indent(str(code), "    ")
        function = function.splitlines()
        x = function[-1].removeprefix("    ")
        if (
            not x.startswith("print")
            and not x.startswith("return")
            and not x.startswith(" ")
            and not x.startswith("yield")
            and not x.startswith("import")
        ):
            function.pop(function.index(function[-1]))
            function.append(f"    return {x}")
        function = "\n".join(function)
        await self._handle_eval(env, ctx, function)
