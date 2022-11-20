import discord
from discord.ext import commands

from .base_section import BaseSection, command


class CommandsSection(BaseSection):
    @command(name="disable", description="Disables a command")
    async def cmd_disable(self, ctx: commands.Context, command_name: str):
        command = ctx.bot.get_command(command_name)

        if command == None:
            return await self.send_error(ctx, f'Command "{command_name}" not found')
        elif not command.enabled:
            return await self.send_error(ctx, f"{command.name} is already disabled")

        command.update(enabled=False)

        await self.send_success(ctx, f"Disabled {command.name}")

    @command(name="enable", description="Enables a command")
    async def cmd_enable(self, ctx: commands.Context, command_name: str):
        command = ctx.bot.get_command(command_name)

        if command == None:
            return await self.send_error(ctx, f'Command "{command_name}" not found')
        elif command.enabled:
            return await self.send_error(ctx, f"{command.name} is already enabled")

        command.update(enabled=True)

        await self.send_success(ctx, f"Enabled {command.name}")
