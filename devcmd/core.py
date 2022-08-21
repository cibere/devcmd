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

disallowedLibs = ['requests', 'urllib', 'time', 'ImageMagick', 'PIL', 'sqlite3', 'postgres', "easy_pil", 'json']

mystbin_client = mystbin.Client()
VERSION = "BETA-3.1.1"
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

class CodeBlock(commands.Converter):
    async def convert(self,ctx, block:str):
        block = block.replace("```py", "").replace("```", "")
        return block
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

class helpButtons(discord.ui.View):
    def __init__(self, user, pages):
        self.user = user
        self.pages = pages
        self.current_page = 0
        super().__init__(timeout=None)
        self._dc_hb_num.label = f"{self.current_page + 1}/{len(self.pages)}"

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True)
    async def _dc_hb_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id is not interaction.user.id:
            return await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
        if self.current_page - 1 == 0:
            self._dc_hb_left.disabled = True
        self._dc_hb_right.disabled = False
        self.current_page -= 1
        self._dc_hb_num.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True)
    async def _dc_hb_num(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple)
    async def _dc_hb_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id is not interaction.user.id:
            return await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
        if self.current_page + 1 == len(self.pages) - 1:
            self._dc_hb_right.disabled = True
        self._dc_hb_left.disabled = False
        self.current_page += 1
        self._dc_hb_num.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

class devcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True, invoke_without_command=True, name="devcmd", aliases=['dev', 'dc'], description="the devcmd base group")
    @is_owner()
    async def _devcmd(self, ctx, *, extra_args=None):
        if extra_args == None:
            await ctx.send("Invalid Syntax")
        else:
            raise discord.ext.commands.CommandNotFound(f'Command "{ctx.invoked_with} {extra_args}" is not found')

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
            em.add_field(name="Usage", value=f"devcmd {c.qualified_name} {c.signature}")
            pages.append(em)
            x += 1
        await ctx.send(view=helpButtons(user=ctx.author, pages=pages), embed=pages[0])

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

    @_devcmd.command(aliases=['clear'], name="purge", description="Purges the specifies amount of messages")
    @is_owner()
    async def _dc_purge(self, ctx, num:int):
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=num)
        embed=discord.Embed(color=discord.Color.green(), description=f"Deleted {len(deleted)} messages in {ctx.channel.mention}")
        await ctx.author.send(embed=embed)

    @_devcmd.command(name="restart", description="Restarts the bot")
    @is_owner()
    async def _dc_restart(self, ctx):
        await ctx.channel.typing()
        embed=discord.Embed(color=discord.Color.green(), title="Restarting now...")
        await ctx.send(embed=embed)
        os.execv(sys.executable, ['python'] + sys.argv)
    
    @_devcmd.command(name="shutdown", aliases=['logout'], description="Shutsdown/logs out the bot")
    @is_owner()
    async def _dc_shutdown(self, ctx):
        await ctx.channel.typing()
        embed=discord.Embed(color=discord.Color.green(), title="Logging out...")
        await ctx.reply(embed=embed)
        await self.bot.close()

    @_devcmd.command(name="load", aliases=['reload', 'unload'], description="Loads/reloads/unloads the specified extension")
    @is_owner()
    async def _dc_load(self, ctx, extension:str=None):
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
                em2 = discord.Embed(title="", description=f"[Error has been sent to your dms]({msg.jump_url})", color=discord.Color.green())
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
                em2 = discord.Embed(title="", description=f"[Error has been sent to your dms]({msg.jump_url})", color=discord.Color.orange())
                await ctx.send(embed=em2)
            except discord.errors.Forbidden:
                em = discord.Embed(title="Error", description=f"```py\n{error}\n```", color=discord.Color.red())
                em2 = discord.Embed(title="", description=f"I am unable to send you a dm, so error will be sent here.", color=discord.Color.red())
                await ctx.send(embeds=[em, em2])
            except:
                paste = await mystbin_client.create_paste(filename="error.py", content=error, syntax="python")
                em = discord.Embed(title="Error", description=f"(Error is too long to send here, so it was sent here)[{str(paste)}]", color=discord.Color.red())
                await ctx.send(embed=em)    

    @_devcmd.group(invoke_without_command=True, name="eval", aliases=['```py', '```', 'py', 'python', 'run', 'exec', 'execute'], description="Evaluates the given code")
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
                    file = mystbin.File(filename="error.py", content=msg, syntax="py")

                    paste = await mystbin_client.create_multifile_paste(files=[file])
                    outputEm2 = discord.Embed(title="Output", description=f"[Your output was too long, so I sent it here]({str(paste.files[0].content)})", color=discord.Color.green())
                    await ctx.send(embed=outputEm2)

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
    
    @_devcmd.command(name="disable", description="Disables a command")
    @is_owner()
    async def _dc_disable(self, ctx, command_name: str):
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
    async def _dc_enable(self, ctx, command_name: str):
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
        subprocess.run(f"pip install git+{url}", shell=True)
        await self.bot.unload_extension('devcmd')
        await self.bot.load_extension('devcmd')
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
                xname = name.replace(os.getenv("NAME"), "<my name>")
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
                                em=discord.Embed(title="Possible Blocking Code Found", description=f"Line: `{lines.index(line)+1}`\nFile: `{xname}`\nReason: importing `{lib}`, which is not a whitelisted module", color=discord.Color.blue())
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
            return await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=f"`{cog_name}` is not a cog that is currently loaded"))
        await self.bot.remove_cog(cog_name)
        await ctx.send(embed=discord.Embed(color=discord.Color.green(), description=f"Successfully removed `{cog_name}`"))
    
    @_devcmd.command(name="cogs", description="lists all loaded cogs")
    @is_owner()
    async def _dc_cogs(self, ctx):
        cogs = [f"`{str(cog)}`" for cog in self.bot.cogs]
        em = discord.Embed(title="Loaded Cogs", color=discord.Color.blue(), description=', '.join(cogs))
        await ctx.send(embed=em)

    @_devcmd.group(name="clean", description="cleans the given text of your name", invoke_without_command=True)
    @is_owner()
    async def _dc_clean(self, ctx, *, text):
        txt = text.replace(os.getenv("NAME"), "<my name>")
        await ctx.reply(embed=discord.Embed(description=f"```{txt}```", color=discord.Color.blue(), title=f"Your cleaned text"), mention_author=False)
        try:
            await ctx.message.delete()
        except:
            pass

    @_dc_clean.command(name="raw", description="clean command, but for mobile!")
    @is_owner()
    async def _dc_clean_raw(self, ctx, *, text):
        txt = text.replace(os.getenv("NAME"), "<my name>")
        await ctx.reply(txt, mention_author=False)
        try:
            await ctx.message.delete()
        except:
            pass

async def setup(bot):
    await bot.add_cog(devcmd(bot))