from discord.ext import commands
from discord.ext.commands import *
import discord
import io, os
from typing import Literal, Optional
import inspect
import re
from io import StringIO
from traceback import format_exc as geterr
from textwrap import indent
import import_expression
import sys, traceback, aiohttp
import subprocess
from dotenv import load_dotenv
load_dotenv()
from .paginators import EmbedPaginator
from .converters import CodeBlockConvertor
import time
import statistics

disallowedLibs = ['requests', 'urllib', 'time', 'ImageMagick', 'PIL', 'sqlite3', 'postgres', "easy_pil", 'json']
TOKEN_REGEX = re.compile(r'[a-zA-Z0-9_-]{23,28}\.[a-zA-Z0-9_-]{6,7}\.[a-zA-Z0-9_-]{27,}')
VERSION = "BETA-3.3.3"
url = "https://github.com/cibere/devcmd@beta"

class infoCmd:
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
                em = infoCmd.masterEmbeds['doc']
                view=infoCmd.infoDropdownView(self.owner, docDef=True)
            elif val == "git":
                em = infoCmd.masterEmbeds['git']
                view=infoCmd.infoDropdownView(self.owner, gitDef=True)
            elif val == "color":
                em = infoCmd.masterEmbeds['color']
                view=infoCmd.infoDropdownView(self.owner, colorDef=True)
            await interaction.response.edit_message(embed=em, view=view)

    class infoDropdownView(discord.ui.View):
        def __init__(self, owner, docDef=False, gitDef=False, colorDef=False):
            super().__init__(timeout=None)
            self.owner = owner
            self.x = infoCmd.infoDropdown(owner, docDef, gitDef, colorDef)
            self.add_item(self.x)
        
        @discord.ui.button(label='X', style=discord.ButtonStyle.red, row=2)
        async def _exit(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.owner.id:
                return await interaction.response.send_message(f"This is for my owner(s) only.", ephemeral=True)
            self.x.disabled = True
            self._exit.disabled = True
            await interaction.response.edit_message(view=self)

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

def filterTxt(text: str):
    name = os.getenv("NAME")
    if name:
        text = text.replace(name, "[NAME HERE]")
    tokens = [token for token in TOKEN_REGEX.findall(text)]
    for tok in tokens:
        text = text.replace(tok, "[TOKEN HERE]")
    return text

class synced_start_pagination(discord.ui.View):
    def __init__(self, user, synced):
        self.user = user
        self.synced = synced
        super().__init__(timeout=None)

    @discord.ui.button(label='Show All Commands', style=discord.ButtonStyle.blurple)
    async def _start_pagination(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
        pages = []
        for c in self.synced:
            em = discord.Embed(title=f"Command: {c.name}", color=discord.Color.blue(), description=c.description)
            em.add_field(name="ID", value=f"{c.id}")
            em.add_field(name="Usage", value=f"{c.mention}")
            pages.append(em)
        await interaction.response.edit_message(embed=pages[0], view=EmbedPaginator(interaction.user, pages))

class devcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.JSK_INSTALLED = None
        try:
            import jishaku
            del jishaku
            self.JSK_INSTALLED = True
        except ImportError:
            self.JSK_INSTALLED = False

    @commands.group(hidden=True, invoke_without_command=True, name="devcmd", aliases=['dev', 'dc'], description="the devcmd base group")
    @is_owner()
    async def _devcmd(self, ctx, *, extra_args=None):
        if extra_args == None:
            nl = '\n'
            em = discord.Embed(
                title=f"Invalid Syntax",
                color=discord.Color.red(),
                description=f"Please choose from one of my many subcommands:\n>>> {nl.join([cmd.name for cmd in ctx.command.commands])}"
            )
            await ctx.send(embed=em)
        else:
            raise discord.ext.commands.CommandNotFound(f'Command "{ctx.invoked_with} {extra_args}" != found')

    @_devcmd.command(name="help", description="Gives you help with devcmd")
    async def _dc_help(self, ctx):
        pages = []
        em = discord.Embed(title="Devcmd Help", color=discord.Color.blue(), description="""```yaml\n<> - required arguement\n[] - optional argument```""")
        pages.append(em)

        rawcmds = []
        x = 2
        for c in devcmd._devcmd.commands:
            em = discord.Embed(title=f"Help: {c.name}", color=discord.Color.blue(), description=c.description)
            if c.help != None:
                em.add_field(name="Help", value=c.help)
            if c.aliases != []:
                em.add_field(name="Aliases", value=f"`{'`, `'.join(c.aliases)}`")
            em.add_field(name="Usage", value=f"{c.qualified_name} {c.signature}")
            pages.append(em)
            x += 1
        await ctx.send(view=EmbedPaginator(user=ctx.author, pages=pages), embed=pages[0])

    @_devcmd.command(name="info", aliases=['about', 'github', 'docs'], description="Gives you a view that gives you information about devcmd")
    @is_owner()
    async def _dc_info(self, ctx):
        em = discord.Embed(title="Please make a selection", color=discord.Color.blue())
        await ctx.send(embed=em, view=infoCmd.infoDropdownView(ctx.author))

    @_devcmd.command(aliases=['logs'], name="audit", description="Shows the last amount of audit log entries")
    @is_owner()
    async def _cd_audit(self, ctx:commands.Context, num:int):
        await ctx.channel.typing()
        audits = []
        async for entry in ctx.guild.audit_logs(limit=num):
            audits.append(f'{entry.user} did {entry.action} to {entry.target} with the reason of: {entry.reason}')
        nl = '\n'
        embed=discord.Embed(color=discord.Color.blue(), title="Audit", description=nl.join(audits))
        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.send(file=discord.File(
            filename="Audit Logs",
            fp=io.BytesIO(embed.description.encode('utf-8'))))

    @_devcmd.command(name="cleanup", description="cleans up the bots messages")
    @is_owner()
    async def _dc_purge(self, ctx: commands.Context, limit:int):
        async with ctx.channel.typing():
            deleted = []
            async for msg in ctx.channel.history(limit=limit):
                if msg.author.id == ctx.guild.me.id:
                    await msg.delete()
                    deleted.append(msg)
            embed = discord.Embed(color=discord.Color.green(), description=f"Cleaned up {len(deleted)} messages")
            await ctx.send(embed=embed)

    @_devcmd.command(name="restart", description="Restarts the bot")
    @is_owner()
    async def _dc_restart(self, ctx):
        await ctx.channel.typing()
        embed = discord.Embed(color=discord.Color.green(), title="Restarting now...")
        await ctx.send(embed=embed)
        os.execv(sys.executable, ['python'] + sys.argv)
    
    @_devcmd.command(name="shutdown", aliases=['logout'], description="Shutsdown/logs out the bot")
    @is_owner()
    async def _dc_shutdown(self, ctx):
        await ctx.channel.typing()
        embed = discord.Embed(color=discord.Color.green(), title="Logging out...")
        await ctx.reply(embed=embed)
        await self.bot.close()

    @_devcmd.command(name="load", aliases=['reload', 'unload'], description="Loads/reloads/unloads the specified extension")
    @is_owner()
    async def _dc_load(self, ctx, extension:str = None):
        await ctx.channel.typing()
        if extension == "all" and ctx.invoked_with == "reload":
            msg = []
            for extension in list(self.bot.extensions.keys()):
                try:
                    await self.bot.reload_extension(extension)
                    msg.append(f"✅ Reloaded `{extension}`")
                except Exception as e:
                    msg.append(f"❌ Unable to load `{extension}` due to `{e}`")
            em = discord.Embed(title="", description='\n'.join(msg), color=discord.Color.blue())
            return await ctx.send(embed=em)
        elif ctx.invoked_with == "reload" and extension == None:
            extension = "devcmd"
        elif extension == None:
            raise BadArgument(f'"Extension" is a required argument')
        if ctx.invoked_with == "unload":
            try:
                await self.bot.unload_extension(extension)
                em = discord.Embed(title="", description=f"✅ unloaded `{extension}`", color=discord.Color.green())
                return await ctx.send(embed=em)
            except commands.ExtensionNotLoaded:
                em = discord.Embed(title="Error", description=f"""Extension `{extension}` was not previously loaded""", color=discord.Color.red())
                return await ctx.send(embed=em)
            except Exception:
                em = discord.Embed(title="Error", description=f"""```py\n{traceback.format_exc()}\n```""", color=discord.Color.red())
                msg = await ctx.author.send(embed=em)
                em2 = discord.Embed(title="", description=f"[Error has been sent to your dms]({msg.jump_url})", color=discord.Color.green())
                return await ctx.send(embed=em2)
        try:
            await self.bot.unload_extension(extension)
            text = "reloaded"
        except Exception:
            text = "loaded"
        try:
            await self.bot.load_extension(extension)
            em = discord.Embed(title="", description=f"✅ {text} `{extension}`", color=discord.Color.green())
            await ctx.send(embed=em)
        except commands.ExtensionNotFound:
            em = discord.Embed(title="Error", description=f"""Extension `{extension}` not found""", color=discord.Color.red())
            return await ctx.send(embed=em)
        except Exception:
            error = traceback.format_exc()
            error = filterTxt(error)
            try:
                em = discord.Embed(title="Error", description=f"```py\n{error}\n```", color=discord.Color.red())
                msg = await ctx.author.send(embed=em)
                em2 = discord.Embed(title="", description=f"[Error has been sent to your dms]({msg.jump_url})", color=discord.Color.orange())
                await ctx.send(embed=em2)
            except discord.errors.Forbidden:
                em = discord.Embed(title="Error", description=f"```py\n{error}\n```", color=discord.Color.red())
                em2 = discord.Embed(title="", description=f"I am unable to send you a dm, so error will be sent here.", color=discord.Color.red())
                await ctx.send(embeds=[em, em2])

    async def _handle_eval(self, env, ctx, function, as_generator = False):
        with RedirectedStdout() as otp:
            try:
                import_expression.exec(function,env)
                func = env["func"]
                ping = time.monotonic()
                if not as_generator:
                    res = await func()
                else:
                    res = None
                    async for x in func():
                        print(x)
            except Exception as e:
                if str(e) == "object async_generator can't be used in 'await' expression":
                    return await self._handle_eval(env, ctx, function, True)
                msg = f"```py\n{otp}\n{e}{geterr()}\n```"
                msg = f"```py\n{e}```\n```py\n{geterr()}\n```"
                msg = filterTxt(msg)
                errorEm = discord.Embed(title="Eval Error", description=msg, color=discord.Color.red())
                await ctx.send(embed=errorEm)
                return
            ping = time.monotonic() - ping
            ping = ping * 1000
            if res:
                msg = f"```py\n{res}\n{otp}\n```"
                msg = filterTxt(msg)
                returnedEm = discord.Embed(title="Returned", description=msg, color=discord.Color.green())
                returnedEm.set_footer(text=f"Finished in {ping}ms")
                await ctx.send(embed=returnedEm)
            else:
                msg = f"```py\n{otp}\n```"
                msg = filterTxt(msg)
                outputEm = discord.Embed(title="Output", description=msg, color=discord.Color.green())
                outputEm.set_footer(text=f"Finished in {ping}ms")
                await ctx.send(embed=outputEm)

    @_devcmd.group(invoke_without_command=True, name="eval", aliases=['```py', '```', 'py', 'python', 'run', 'exec', 'execute'], description="Evaluates the given code")
    @is_owner()
    async def _dc_eval(self, ctx, *,code: CodeBlockConvertor):
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
            "sys":sys,
            "aiohttp":aiohttp
        }

        function="async def func():\n"+indent(code,"    ")
        function = function.splitlines()
        x = function[-1].removeprefix("    ")
        if not x.startswith("print") and not x.startswith("return") and not x.startswith(" ") and not x.startswith("yield"):
            function.pop(function.index(function[-1]))
            function.append(f"    return {x}")
        function = '\n'.join(function)
        await self._handle_eval(env, ctx, function)
        

    @_devcmd.command(name="sync", help="""
Works like:
`!sync` -> global sync
`!sync ~` -> sync current guild
`!sync *` -> copies all global app commands to current guild and syncs
`!sync ^` -> clears all commands from the current guild target and syncs (removes guild commands)
`!sync id_1 id_2` -> syncs guilds with id 1 and 2""", description="Syncs app_commands according to the given arg")
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
            return await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}", view=synced_start_pagination(ctx.author, synced))
            

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
    
    @_devcmd.command(name="disable", description="Disables a command")
    @is_owner()
    async def _dc_disable(self, ctx, *, command_name: str):
        em=discord.Embed()
        command = self.bot.get_command(command_name)
        if command == None:
            raise BadArgument(f'Command "{command_name}" not found')
        if not command.enabled:
            em.color = discord.Color.red()
            em.description = f"{command.name} is already disabled"
            return await ctx.send(embed=em)
        command.update(enabled=False)
        em.description = f"Disabled {command.name}"
        em.color = discord.Color.green()
        await ctx.send(embed=em)

    @_devcmd.command(name="enable", description="Enables a command")
    @is_owner()
    async def _dc_enable(self, ctx, *, command_name: str):
        command = self.bot.get_command(command_name)
        if command == None:
            raise BadArgument(f'Command "{command_name}" not found')
        em = discord.Embed()
        command.update(enabled=True)
        em.description = f"Enabled {command.name}"
        em.color = discord.Color.green()
        await ctx.send(embed=em)

    @_devcmd.command(name="update", description="Lets you update your devcmd", aliases=['update-msg'])
    @is_owner()
    async def _dc_update(self, ctx):
        if ctx.invoked_with == "update-msg":
            em=discord.Embed(title="Updating devcmd")
            em.description = f"Successfully updated devcmd to version {VERSION}"
            em.color = discord.Color.green()
            return await ctx.send(embed=em)
        
        await ctx.channel.typing()
        subprocess.run(f"py -m pip install git+{url}", shell=True)
        await self.bot.reload_extension('devcmd')
        msg = ctx.message
        msg.content += "-msg"
        await self.bot.process_commands(msg) 
        

    @_devcmd.command(name="version", description="Sends the current version of devcmd you are running")
    @is_owner()
    async def _dc_version(self, ctx):
        em = discord.Embed(description=f"Running Devcmd Version {VERSION}", color=discord.Color.blue())
        await ctx.send(embed=em)

    @_devcmd.command(name="source", aliases=['src'], description="Gives the source code for the specified command")
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

    @_devcmd.command(name="file", description="Sends the code for the specified file")
    @is_owner()
    async def _dc_file(self, ctx, file:str):
        if "env" in file:
            raise BadArgument(f'"{file}" != a safe file')
        try:
            with open(file, 'r', encoding="utf-8") as f:
                code = str(f.read())
        except FileNotFoundError:
            raise BadArgument(f'"{file}" != a valid file')
        
        name = file.split('/')
        name = name[len(name) - 1]
        await ctx.send(file=discord.File(
            filename=name,
            fp=io.BytesIO(code.encode('utf-8'))))

    @_devcmd.command(name="blocking",description="Searches your code for blocking code",  aliases=['blocking-code'])
    @is_owner()
    async def _dc_blocking(self, ctx):
        em = discord.Embed(description="Searching your code for blocking code... this might take a while")
        await ctx.send(embed=em)
        async with ctx.channel.typing():
            path =os.getcwd()
            list_of_files = []
            fileNames = []
            cases = 0
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        list_of_files.append(os.path.join(root,file))
                        fileNames.append(file.split(".")[0])
            for name in list_of_files:
                xname = filterTxt(name)
                with open(name, 'r', encoding='utf-8') as f:
                    code = str(f.read())
                lines = code.splitlines()
                for line in lines:
                    if line.replace(" ", "").replace("  ", "").startswith("def"):
                        if line.replace(" ", "").replace("  ", "").startswith("def__init__") == False:
                            if line.startswith("def "):
                                em=discord.Embed(title="Possible Blocking Code Found", description=f"Line: `{lines.index(line) +1}`\nFile: `{xname}`\nReason: non async function found", color=discord.Color.blue())
                                await ctx.send(embed=em)
                                cases += 1
                    if line.startswith("import") or line.startswith("from"):
                        lib = line.split(" ")[1].split(".")[0].replace(",", "")
                        if lib not in fileNames:
                            if lib in disallowedLibs:
                                em=discord.Embed(title="Possible Blocking Code Found", description=f"Line: `{lines.index(line)+1}`\nFile: `{xname}`\nReason: importing `{lib}`, which != a whitelisted module", color=discord.Color.blue())
                                await ctx.send(embed=em)
                                cases += 1


            em=discord.Embed(title="Scanning Complete", description=f"Completed with {cases} cases of possible blocking code found.", color=discord.Color.blue())
        await ctx.send(embed=em)

    @_devcmd.command(name="invite", description="gives you a url to invite your bot")
    @is_owner()
    async def _dc_invite(self, ctx, perms=0):
        try:
            url = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=perms))
            embed=discord.Embed(title="Invite Url", description=url, color=discord.Color.blue())
        except:
            url = discord.utils.oauth_url(self.bot.user.id)
            embed=discord.Embed(title="Invite Url", description=f"`{perms}` are not valid permissions. Here is a blank invite url:\n{url}", color=discord.Color.blue())
        await ctx.send(embed=embed)

    @_devcmd.command(name="remove", description="removes a cog")
    @is_owner()
    async def _dc_remove(self, ctx, cog_name:str):
        cogs = [str(cog) for cog in self.bot.cogs]
        if (cog_name not in cogs):
            return await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=f"`{cog_name}` != a cog that is currently loaded"))
        await self.bot.remove_cog(cog_name)
        await ctx.send(embed=discord.Embed(color=discord.Color.green(), description=f"Successfully removed `{cog_name}`"))
    
    @_devcmd.command(name="cogs", description="lists all loaded cogs")
    @is_owner()
    async def _dc_cogs(self, ctx):
        cogs = [f"`{str(cog)}`" for cog in self.bot.cogs]
        em = discord.Embed(title="Loaded Cogs", color=discord.Color.blue(), description=', '.join(cogs))
        await ctx.send(embed=em)


    async def cleanCallback(self, ctx, text, method:Literal['pc', 'mobile']):
        txt = filterTxt(text)
        if method == "pc":
            await ctx.reply(embed=discord.Embed(description=f"```{txt}```", color=discord.Color.blue(), title=f"Your cleaned text"), mention_author=False)
        elif method == 'mobile':
            await ctx.reply(txt, mention_author=False)
        try:
            await ctx.message.delete()
        except:
            pass

    @_devcmd.group(name="clean", description="cleans the given text of your name", invoke_without_command=True)
    @is_owner()
    async def _dc_clean(self, ctx, *, text):
        await self.cleanCallback(ctx, text, 'pc')
        

    @_dc_clean.command(name="raw", description="clean command, but for mobile!")
    @is_owner()
    async def _dc_clean_raw(self, ctx, *, text):
        await self.cleanCallback(ctx, text, 'mobile')

    @_devcmd.group(name="ping", description="ping subgroup", invoke_without_command=True)
    async def _dc_ping(self, ctx):
        nl = '\n'
        em = discord.Embed(
                title=f"Invalid Syntax",
                color=discord.Color.red(),
                description=f"Please choose from one of my many subcommands:\n>>> {nl.join([cmd.name for cmd in ctx.command.commands])}"
        )
        await ctx.send(embed=em)
    
    @_dc_ping.command(name="websocket", description="determines the bots websocket latency", aliases=['web', 'w', 'socket'])
    async def _dc_ping_websocket(self, ctx):
        em = discord.Embed(title="Websock Latency", description=f"{round(self.bot.latency * 1000, 2)}ms", color=discord.Color.blue())
        await ctx.send(embed=em)
    
    @_dc_ping.command(name="message", description="determines the bots message latency", aliases=['msg', 'm'])
    async def _dc_ping_message(self, ctx, amount=3):
        em = discord.Embed(title="Message Latency", description="", color=discord.Color.blue())
        em.add_field(name="Average", value=f"```N/A```", inline=False)
        em.set_footer(text=f"Currently on round 1/{amount}")
        oringMsg = await ctx.send(embed=em)
        em = oringMsg.embeds[0]
        
        pings = []
        for x in range(amount):          
            ping = time.monotonic()
            msg = await oringMsg.edit(embed=em)
            ping = time.monotonic() - ping
            msgP = round(ping * 1000, 2)
            pings.append(msgP)
            em = msg.embeds[0]
            if not x + 3 > amount - 1:
                em.set_footer(text=f"Currently on round {x + 2}/{amount}")
            try:
                em.description += f"\nRound {x + 1}: {msgP}ms"
            except:
                em.description = f"\nRound {x + 1}: {msgP}ms"
        
        em.set_footer(text=f"Finished")
        em.set_field_at(0, value=f"```{round(statistics.mean(pings), 2)}ms```", name='Average', inline=False)
        await oringMsg.edit(embed=em, content="")
        
    @_devcmd.command(name="jishaku", description = "toggles jishaku", aliases=['jsk'])
    @is_owner()
    async def _dc_jsk(self, ctx):
        if self.JSK_INSTALLED == False:
            return await ctx.reply("You do not have jsk installed. Install it via ```pip install -U jishaku```")
        if self.JSK_INSTALLED == None:
            try:
                import jishaku
                del jishaku
                self.JSK_INSTALLED = True
            except ImportError:
                self.JSK_INSTALLED = False
            return self.bot.process_commands(ctx.message)
        if 'Jishaku' in self.bot.cogs:
            await self.bot.unload_extension('jishaku')
            em = discord.Embed(title="", description="`✅ unloaded jishaku`", color=discord.Color.green())
            await ctx.send(embed=em)
        else:
            await self.bot.load_extension('jishaku')
            em = discord.Embed(title="", description="`✅ loaded jishaku`", color=discord.Color.green())
            await ctx.send(embed=em)