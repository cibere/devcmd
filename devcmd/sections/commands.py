import discord
from discord.ext import commands

from .base_section import BaseSection, command


class CommandsSection(BaseSection):
    @command(name="disable", description="Disables a command")
    async def cmd_disable(self, ctx: commands.Context, command_name: str):
        em = discord.Embed()
        command = ctx.bot.get_command(command_name)
        if command == None:
            return await ctx.send(f'Command "{command_name}" not found')
        if not command.enabled:
            em.color = discord.Color.red()
            em.description = f"{command.name} is already disabled"
            return await ctx.send(embed=em)
        command.update(enabled=False)
        em.description = f"Disabled {command.name}"
        em.color = discord.Color.green()
        await ctx.send(embed=em)

    @command(name="enable", description="Enables a command")
    async def cmd_enable(self, ctx: commands.Context, command_name: str):
        command = ctx.bot.get_command(command_name)
        if command == None:
            return await ctx.send(f'Command "{command_name}" not found')
        em = discord.Embed()
        command.update(enabled=True)
        em.description = f"Enabled {command.name}"
        em.color = discord.Color.green()
        await ctx.send(embed=em)
