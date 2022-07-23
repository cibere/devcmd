from discord.ext import commands
from discord.ext.commands import *
import discord
import io, os
from typing import Literal, Optional
import inspect
import mystbin
from io import StringIO
from traceback import format_exc as geterr
from textwrap import indent
import sys, traceback
import subprocess

mystbin_client = mystbin.Client()
VERSION = "0.0.5.2"

class CodeBlock(commands.Converter):
    async def convert(self,ctx, block:str):
        lines=block.split("\n")
        if "`" in lines[0]:
            lines.pop(0)
        if "`" in lines[len(lines)-1]:
            li = lines[len(lines)-1].rsplit('```', 1)
            lines[len(lines)-1] = ''.join(li)
        return "\n".join(lines)

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
        return self._string_io.getvalue()

class devcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True, invoke_without_command=True, name="devcmd", aliases=['dev', 'dc'])
    @is_owner()
    async def _devcmd(self, ctx, *, extra_args=None):
        if extra_args == None:
            await ctx.send("Invalid Syntax")
        else:
            raise discord.ext.commands.CommandNotFound(f'Command "{ctx.invoked_with} {extra_args}" is not found')

    @_devcmd.command(aliases=['logs'], name="audit")
    @is_owner()
    async def _cd_audit(self, ctx:commands.Context, num:int):
        await ctx.channel.typing()
        audits = []
        async for entry in ctx.guild.audit_logs(limit=num):
            audits.append(f'{entry.user} did {entry.action} to {entry.target} with the reason of: {entry.reason}')
        nl = '\n'
        embed=discord.Embed(color=discord.Color.yellow(), title="Audit", description=nl.join(audits))
        try:
            await ctx.reply(embed=embed)
        except:
            with open(f"temp/{ctx.author.id}.txt", "w") as f:
                f.write(embed.description)
            await ctx.send(file=discord.File(f"temp/{ctx.author.id}.txt"))

    @_devcmd.command(aliases=['clean', 'clear'], name="purge")
    @is_owner()
    async def _dc_purge(self, ctx, num:int):
        num += 1
        deleted = await ctx.channel.purge(limit=num)
        await ctx.author.send(f"Deleted {len(deleted)} messages")

    @_devcmd.command(name="restart")
    @is_owner()
    async def _dc_restart(self, ctx):
        await ctx.channel.typing()
        embed=discord.Embed(color=discord.Color.green(), title="Restarting now...")
        await ctx.send(embed=embed)
        os.execv(sys.executable, ['python'] + sys.argv)
    
    @_devcmd.command(name="shutdown", aliases=['logout'])
    @is_owner()
    async def _dc_shutdown(self, ctx):
        await ctx.channel.typing()
        await ctx.reply("Logging out...")
        await self.bot.close()

    @_devcmd.command(name="load", aliases=['reload', 'unload'])
    @is_owner()
    async def _dc_load(self, ctx, extension:str=None):
        await ctx.channel.typing()
        if ctx.invoked_with == "reload" and extension == None:
            extension = "devcmd"
        elif extension == None:
            await ctx.reply("`Extension` argument is required")
            return
        if ctx.invoked_with == "unload":
            try:
                await self.bot.unload_extension(extension)
                return await ctx.send(f"`✅ unloaded {extension}`")
            except Exception:
                try:
                    await ctx.message.add_reaction('‼️')
                except:
                    pass
                return await ctx.author.send(f"""```py\n{traceback.format_exc()}\n```""")
        try:
            await self.bot.unload_extension(extension)
            text = "reloaded"
        except Exception:
            text = "loaded"
        try:
            await self.bot.load_extension(extension)
            await ctx.send(f"`✅ {text} {extension}`")
        except Exception:
            error = traceback.format_exc()
            try:
                await ctx.message.add_reaction('‼️')
            except:
                pass
            try:
                await ctx.author.send(f"""```py\n{error}\n```""")
            except:
                paste = await mystbin_client.post(error, syntax="python")
                await ctx.send(f"Error is too long to send here, so error was sent to {str(paste)}")

    @_devcmd.command(name="source", aliases=['src'])
    @is_owner()
    async def _dc_source(self, ctx, *, command_name: str):
        await ctx.channel.typing()
        command = self.bot.get_command(command_name)
        if not command:
            await ctx.send(f"Command `{command_name}` not found")
            return
        try:
            source_lines, _ = inspect.getsourcelines(command.callback)
        except:
            await ctx.send(f"I could not find the source code for `{command}`.")
            return
        source_text = ''.join(source_lines)
        await ctx.send(file=discord.File(
            filename="source.py",
            fp=io.BytesIO(source_text.encode('utf-8'))))
    

    @_devcmd.command(name="eval", aliases=['```py', '```', 'py', 'python', 'run', 'exec', 'execute'])
    @is_owner()
    async def _dc_eval(self, ctx, *,code:CodeBlock):
        await ctx.channel.typing()
        env={
            "ctx":ctx,
            "bot":self.bot,
            "message":ctx.message,
            "author":ctx.author,
            "guild":ctx.guild,
            "channel":ctx.channel,
            "discord":discord,
            "commands":commands,
            "os":os,
            "io":io,
            "sys":sys
        }

        function="async def func():\n"+indent(code,"    ")
        with RedirectedStdout() as otp:
            try:
                exec(function,env)
                func=env["func"]
                res= await func()
            except Exception as e:
                msg = f"```py\n{otp}\n{e}{geterr()}\n```"
                if os.getenv("NAME") in msg.lower():
                    msg = msg.replace(os.getenv("NAME"), "<my name>")
                errorEm = discord.Embed(title="Eval Error", description=msg, color=discord.Color.red())
                await ctx.send(embed=errorEm)
                return
            if res:
                msg = f"```py\n{res}\n#output\n{otp}\n```"
                if os.getenv("NAME") in msg.lower():
                    msg = msg.replace(os.getenv("NAME"), "<my name>")
                returnedEm = discord.Embed(title="Returned", description=msg, color=discord.Color.green())
                await ctx.send(embed=returnedEm)
            else:
                msg = f"```py\n{otp}\n```"
                if os.getenv("NAME") in msg.lower():
                    msg = msg.replace(os.getenv("NAME"), "<my name>")
                outputEm = discord.Embed(title="Output", description=msg, color=discord.Color.green())
                await ctx.send(embed=outputEm)

    @_devcmd.command(name="sync", help="""
Works like:
`!sync` -> global sync
`!sync ~` -> sync current guild
`!sync *` -> copies all global app commands to current guild and syncs
`!sync ^` -> clears all commands from the current guild target and syncs (removes guild commands)
`!sync id_1 id_2` -> syncs guilds with id 1 and 2""")
    @is_owner()
    @commands.guild_only()
    async def _dc_sync(self, ctx, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None):
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @_devcmd.command(name="github")
    @is_owner()
    async def _dc_github(self, ctx):
        await ctx.reply('https://github.com/cibere/devcmd')
    
    @_devcmd.command(name="disable")
    @is_owner()
    async def _dc_disable(self, ctx, raw: str):
        em=discord.Embed()
        command = self.bot.get_command(raw)
        if command == None:
            raise BadArgument(f'Command "{raw}" not found')
        if not command.enabled:
            em.color = discord.Color.red()
            em.description = f"{command.name} is already disabled"
            return await ctx.send(embed=em)
        command.update(enabled=False)
        em.description = f"Disabled {command.name}"
        em.color = discord.Color.darker_gray()
        await ctx.send(embed=em)

    @_devcmd.command(name="enable")
    @is_owner()
    async def _dc_enable(self, ctx, raw: str):
        command = self.bot.get_command(raw)
        if command == None:
            raise BadArgument(f'Command "{raw}" not found')
        em = discord.Embed()
        command.update(enabled=True)
        em.description = f"Enabled {command.name}"
        em.color = discord.Color.green()
        await ctx.send(embed=em)

    @_devcmd.command(name="update")
    @is_owner()
    async def _dc_update(self, ctx):
        em=discord.Embed(title="Updating devcmd")
        await ctx.channel.typing()
        subprocess.run("pip install git+https://github.com/cibere/devcmd", shell=True)
        await self.bot.unload_extension('devcmd')
        await self.bot.load_extension('devcmd')
        em.description = f"Successfully updated to devcmd version {VERSION}"
        await ctx.send(embed=em)
    
    @_devcmd.command(name="version")
    @is_owner()
    async def _dc_version(self, ctx):
        await ctx.send(f"Running devcmd version {VERSION}")

    @_devcmd.command(name="docs")
    @is_owner()
    async def _dc_docs(self, ctx):
        await ctx.send(f"https://gist.github.com/cibere/da22060df5ab6282b452e972f08d269b")

async def setup(bot):
    await bot.add_cog(devcmd(bot))