from http.client import HTTPException
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
from dotenv import load_dotenv
load_dotenv()

mystbin_client = mystbin.Client()
VERSION = "beta-1.0.0.19"
url = "https://github.com/cibere/devcmd@beta"

masterEmbeds = {
    'doc':discord.Embed(
        title="Devcmd Documentation",
        description="https://gist.github.com/cibere/da22060df5ab6282b452e972f08d269b",
        color=discord.Color.blue()
    ),
    'git':discord.Embed(
        title="Devcmd Github",
        description="""[Stable/Main Version](https://github.com/cibere/devcmd)\n[Development/Beta Version](https://github.com/cibere/devcmd/tree/beta)""",
        color=discord.Color.blue()
    ),
    'color':discord.Embed(
        title="Embed Color Code",
        description="""
> **Blue:**
> __Informational Embed__

> **Green**
> __Successfull Embed__

> **Red**
> __An Error Embed__

> **Orange**
> __A Error has been sent to your dms Embed__
""",
        color=discord.Color.blue()
    ),
}

class infoDropdown(discord.ui.Select):
    def __init__(self, owner, docDef=False, gitDef=False, colorDef=False):
        self.owner = owner
    
        options = [
            discord.SelectOption(label='Docs', description='Gives you the devcmd docs', value='doc', default=docDef),
            discord.SelectOption(label='Github', description='Gives you the devcmd github page', value='git', default=gitDef),
            discord.SelectOption(label='Embed Colors', description='Gives you info about the coloring of embeds', value='color', default=colorDef),
        ]

        super().__init__(placeholder='Choose a option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner.id:
            return await interaction.response.send_message(f"This is for my owner(s) only.", ephemeral=True)
        val = self.values[0]
        if val == "doc":
            em = masterEmbeds['doc']
            view=infoDropdownView(self.owner, docDef=True)
        elif val == "git":
            em = masterEmbeds['git']
            view=infoDropdownView(self.owner, gitDef=True)
        elif val == "color":
            em = masterEmbeds['color']
            view=infoDropdownView(self.owner, colorDef=True)
        await interaction.response.edit_message(embed=em, view=view)

class infoDropdownView(discord.ui.View):
    def __init__(self, owner, docDef=False, gitDef=False, colorDef=False):
        super().__init__(timeout=None)
        self.owner = owner
        self.x = infoDropdown(owner, docDef, gitDef, colorDef)
        self.add_item(self.x)
    
    @discord.ui.button(label='X', style=discord.ButtonStyle.red, row=2)
    async def _exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner.id:
            return await interaction.response.send_message(f"This is for my owner(s) only.", ephemeral=True)
        self.x.disabled = True
        self._exit.disabled = True
        await interaction.response.edit_message(view=self)

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
        """the devcmd base group"""
        if extra_args == None:
            await ctx.send("Invalid Syntax")
        else:
            raise discord.ext.commands.CommandNotFound(f'Command "{ctx.invoked_with} {extra_args}" is not found')

    @_devcmd.command(name="info", aliases=['about', 'github', 'docs'])
    @is_owner()
    async def _dc_info(self, ctx):
        """Gives you a view that gives you information about devcmd"""
        em = discord.Embed(title="Please make a selection", color=discord.Color.blue())
        await ctx.send(embed=em, view=infoDropdownView(ctx.author))

    @_devcmd.command(aliases=['logs'], name="audit")
    @is_owner()
    async def _cd_audit(self, ctx:commands.Context, num:int):
        """Shows the last amount of audit log entries"""
        await ctx.channel.typing()
        audits = []
        async for entry in ctx.guild.audit_logs(limit=num):
            audits.append(f'{entry.user} did {entry.action} to {entry.target} with the reason of: {entry.reason}')
        nl = '\n'
        embed=discord.Embed(color=discord.Color.blue(), title="Audit", description=nl.join(audits))
        try:
            await ctx.reply(embed=embed)
        except:
            with open(f"temp/{ctx.author.id}.txt", "w") as f:
                f.write(embed.description)
            await ctx.send(file=discord.File(f"temp/{ctx.author.id}.txt"))

    @_devcmd.command(aliases=['clean', 'clear'], name="purge")
    @is_owner()
    async def _dc_purge(self, ctx, num:int):
        """Purges the specifies amount of messages"""
        num += 1
        deleted = await ctx.channel.purge(limit=num)
        embed=discord.Embed(color=discord.Color.green(), description=f"Deleted {len(deleted)} messages")
        await ctx.author.send(embed=embed)

    @_devcmd.command(name="restart")
    @is_owner()
    async def _dc_restart(self, ctx):
        """Restarts the bot"""
        await ctx.channel.typing()
        embed=discord.Embed(color=discord.Color.green(), title="Restarting now...")
        await ctx.send(embed=embed)
        os.execv(sys.executable, ['python'] + sys.argv)
    
    @_devcmd.command(name="shutdown", aliases=['logout'])
    @is_owner()
    async def _dc_shutdown(self, ctx):
        """Shutsdown/logs out the bot"""
        await ctx.channel.typing()
        embed=discord.Embed(color=discord.Color.green(), title="Logging out...")
        await ctx.reply(embed=embed)
        await self.bot.close()

    @_devcmd.command(name="load", aliases=['reload', 'unload'])
    @is_owner()
    async def _dc_load(self, ctx, extension:str=None):
        """Loads/reloads/unloads the specified extension"""
        await ctx.channel.typing()
        if ctx.invoked_with == "reload" and extension == None:
            extension = "devcmd"
        elif extension == None:
            raise BadArgument(f'"Extension" is a required argument')
        if ctx.invoked_with == "unload":
            try:
                await self.bot.unload_extension(extension)
                em = discord.Embed(title="", description=f"`✅ unloaded {extension}`", color=discord.Color.green())
                return await ctx.send(embed=em)
            except Exception:
                em = discord.Embed(title="Error", description=f"""```py\n{traceback.format_exc()}\n```""", color=discord.Color.red())
                msg = await ctx.author.send(embed=em)
                em2 = discord.Embed(title="", description=f"(Error has been sent to your dms)[{msg.jump_url}]", color=discord.Color.green())
                return await ctx.send(embed=em2)
        try:
            await self.bot.unload_extension(extension)
            text = "reloaded"
        except Exception:
            text = "loaded"
        try:
            await self.bot.load_extension(extension)
            em = discord.Embed(title="", description=f"`✅ {text} {extension}`", color=discord.Color.green())
            await ctx.send(embed=em)
        except Exception:
            error = traceback.format_exc()
            error = error.replace(os.getenv("NAME"), "<my name>")
            try:
                em = discord.Embed(title="Error", description=f"```py\n{error}\n```", color=discord.Color.red())
                msg = await ctx.author.send(embed=em)
                em2 = discord.Embed(title="", description=f"(Error has been sent to your dms)[{msg.jump_url}]", color=discord.Color.orange())
                await ctx.send(embed=em2)
            except discord.errors.Forbidden:
                em = discord.Embed(title="Error", description=f"```py\n{error}\n```", color=discord.Color.red())
                em2 = discord.Embed(title="", description=f"I am unable to send you a dm, so error will be sent here.", color=discord.Color.red())
                await ctx.send(embeds=[em, em2])
            except:
                paste = await mystbin_client.post(error, syntax="python")
                em = discord.Embed(title="Error", description=f"(Error is too long to send here, so it was sent here)[{str(paste)}]", color=discord.Color.red())
                await ctx.send(embed=em)    

    @_devcmd.command(name="eval", aliases=['```py', '```', 'py', 'python', 'run', 'exec', 'execute'])
    @is_owner()
    async def _dc_eval(self, ctx, *,code:CodeBlock):
        """Evaluates the given code"""
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
                try:
                    await ctx.send(embed=errorEm)
                except:
                    paste = await mystbin_client.post(msg)
                    errorEm = discord.Embed(title="Error", description=f"[Your error was too long, so I sent it here]({str(paste)})", color=discord.Color.red())
                    await ctx.send(embed=errorEm)
                return
            if res:
                msg = f"```py\n{res}\n{otp}\n```"
                if os.getenv("NAME") in msg.lower():
                    msg = msg.replace(os.getenv("NAME"), "<my name>")
                returnedEm = discord.Embed(title="Returned", description=msg, color=discord.Color.green())
                try:
                    await ctx.send(embed=returnedEm)
                except:
                    paste = await mystbin_client.post(msg)
                    returnedEm = discord.Embed(title="Returned", description=f"[Your output was too long, so I sent it here]({str(paste)})", color=discord.Color.green())
                    await ctx.send(embed=returnedEm)
            else:
                msg = f"```py\n{otp}\n```"
                if os.getenv("NAME") in msg.lower():
                    msg = msg.replace(os.getenv("NAME"), "<my name>")
                outputEm = discord.Embed(title="Output", description=msg, color=discord.Color.green())
                try:
                    await ctx.send(embed=outputEm)
                except:
                    paste = await mystbin_client.post(msg)
                    outputEm = discord.Embed(title="Output", description=f"[Your output was too long, so I sent it here]({str(paste)})", color=discord.Color.green())
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
        """Syncs app_commands to the given thing"""
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
        em = discord.Embed(description=f"Synced the tree to {ret}/{len(guilds)}", color=discord.Color.green())
        await ctx.send(embed=em)
    
    @_devcmd.command(name="disable")
    @is_owner()
    async def _dc_disable(self, ctx, raw: str):
        """Disables a command"""
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
        em.color = discord.Color.green()
        await ctx.send(embed=em)

    @_devcmd.command(name="enable")
    @is_owner()
    async def _dc_enable(self, ctx, raw: str):
        """Enables a command"""
        command = self.bot.get_command(raw)
        if command == None:
            raise BadArgument(f'Command "{raw}" not found')
        em = discord.Embed()
        command.update(enabled=True)
        em.description = f"Enabled {command.name}"
        em.color = discord.Color.green()
        await ctx.send(embed=em)

    @_devcmd.command(name="update", aliases=['update-msg'])
    @is_owner()
    async def _dc_update(self, ctx):
        """Lets you update your devcmd"""
        if ctx.invoked_with == "update-msg":
            em=discord.Embed(title="Updating devcmd")
            em.description = f"Successfully updated devcmd to version {VERSION}"
            em.color = discord.Color.green()
            return await ctx.send(embed=em)
        
        await ctx.channel.typing()
        subprocess.run(f"pip install git+{url}", shell=True)
        await self.bot.unload_extension('devcmd')
        await self.bot.load_extension('devcmd')
        msg = ctx.message
        msg.content += "-msg"
        await self.bot.process_commands(msg) 
        

    @_devcmd.command(name="version")
    @is_owner()
    async def _dc_version(self, ctx):
        """Sends the current version of devcmd you are running"""
        em = discord.Embed(description=f"Running Devcmd Version {VERSION}", color=discord.Color.blue())
        await ctx.send(embed=em)

    @_devcmd.command(name="source", aliases=['src'])
    @is_owner()
    async def _dc_source(self, ctx, *, command_name: str):
        """Gives the source code for the specified command"""
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

    @_devcmd.command(name="file")
    @is_owner()
    async def _dc_file(self, ctx, file:str):
        """Sends the code for the specified file"""
        if "env" in file:
            raise BadArgument(f'"{file}" is not a safe file')
        try:
            with open(file, 'r', encoding="utf-8") as f:
                code = str(f.read())
        except FileNotFoundError:
            raise BadArgument(f'"{file}" is not a valid file')
        
        name = file.split('/')
        name = name[len(name) - 1]
        await ctx.send(file=discord.File(
            filename=name,
            fp=io.BytesIO(code.encode('utf-8'))))

    @_devcmd.command(name="blocking", aliases=['blocking-code'])
    async def _dc_blocking(self, ctx):
        """Searches your code for blocking code"""
        em = discord.Embed(description="Searching your code for blocking code... this might take a while")
        await ctx.send(embed=em)
        async with ctx.channel.typing():
            path =os.getcwd()
            list_of_files = []
            cases = 0
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        list_of_files.append(os.path.join(root,file))
            for name in list_of_files:
                xname = name.replace(os.getenv("NAME"), "<my name>")
                await ctx.send(f"started checking {xname}")
                with open(name, 'r', encoding='utf-8') as f:
                    code = str(f.read())
                lines = code.splitlines()
                for line in lines:
                    if line.replace(" ", "").replace("  ", "").startswith("def"):
                        if line.replace(" ", "").replace("  ", "").startswith("def__init__") == False:
                            em=discord.Embed(title="Possible Blocking Code Found", description=f"Line: `{lines.index(line) +1}`\nFile: `{xname}`\nReason: non async function found", color=discord.Color.blue())
                            await ctx.send(embed=em)
                            cases += 1
                    if "import requests" in line:
                        em=discord.Embed(title="Possible Blocking Code Found", description=f"Line: `{lines.index(line)+1}`\nFile: `{xname}`\nReason: importing `requests`, which is a blocking", color=discord.Color.blue())
                        await ctx.send(embed=em)
                        cases += 1
                    if "from requests" in line:
                        em=discord.Embed(title="Possible Blocking Code Found", description=f"Line: `{lines.index(line)+1}`\nFile: `{xname}`\nReason: importing `requests`, which is a blocking module", color=discord.Color.blue())
                        await ctx.send(embed=em)
                        cases += 1
                await ctx.send(f"finished checking {xname}")

            em=discord.Embed(title="Scanning Complete", description=f"Completed with {cases} cases of possible blocking code found.", color=discord.Color.blue())
        await ctx.send(embed=em)
        

async def setup(bot):
    await bot.add_cog(devcmd(bot))