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

masterEmbeds = {
    'doc':discord.Embed(
        title="Devcmd Documentation",
        description="https://gist.github.com/cibere/da22060df5ab6282b452e972f08d269b",
        color=discord.Color.blue()
    ),
    'git':discord.Embed(
        title="Devcmd Github",
        description="""(Stable/Main Version)[https://github.com/cibere/devcmd]\n(Development/Beta Version)[https://github.com/cibere/devcmd/tree/beta]""",
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
    )
}

masterOptions = {
    'doc':[
            discord.SelectOption(label='Docs', description='Gives you the devcmd docs', value='doc', default=True),
            discord.SelectOption(label='Github', description='Gives you the devcmd github page', value='git'),
            discord.SelectOption(label='Embed Colors', description='Gives you info about the coloring of embeds', value='color'),
    ],
    'git':[
            discord.SelectOption(label='Docs', description='Gives you the devcmd docs', value='doc'),
            discord.SelectOption(label='Github', description='Gives you the devcmd github page', value='git', default=True),
            discord.SelectOption(label='Embed Colors', description='Gives you info about the coloring of embeds', value='color'),
    ],
    'color':[
            discord.SelectOption(label='Docs', description='Gives you the devcmd docs', value='doc'),
            discord.SelectOption(label='Github', description='Gives you the devcmd github page', value='git'),
            discord.SelectOption(label='Embed Colors', description='Gives you info about the coloring of embeds', value='color', default=True),
    ],
    'normal':[
            discord.SelectOption(label='Docs', description='Gives you the devcmd docs', value='doc'),
            discord.SelectOption(label='Github', description='Gives you the devcmd github page', value='git'),
            discord.SelectOption(label='Embed Colors', description='Gives you info about the coloring of embeds', value='color'),
    ],
}

class infoDropdown(discord.ui.Select):
    def __init__(self, owner, options):
        self.owner = owner

        super().__init__(placeholder='Choose a option', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner.id:
            return await interaction.response.send_message(f"This is for my owner(s) only.", ephemeral=True)
        await interaction.response.edit_message(embed=masterEmbeds[self.values[0]], view=infoDropdown(self.owner, masterOptions[self.values[0]]))

class infoDropdownView(discord.ui.View):
    def __init__(self, owner, options):
        super().__init__(timeout=None)

        self.add_item(infoDropdown(owner, options))

class devcmd_base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True, invoke_without_command=True, name="devcmd", aliases=['dev', 'dc'])
    @is_owner()
    async def _devcmd(self, ctx, *, extra_args=None):
        if extra_args == None:
            await ctx.send("Invalid Syntax")
        else:
            raise discord.ext.commands.CommandNotFound(f'Command "{ctx.invoked_with} {extra_args}" is not found')
    
    @_devcmd.command(name="info", alises=['about', 'github', 'docs'])
    @is_owner()
    async def _dc_info(self, ctx):
        em = discord.Embed(title="Please make a selection", color=discord.Color.blue())
        await ctx.send(embed=em, view=infoDropdownView(ctx.author, masterOptions['normal']))

