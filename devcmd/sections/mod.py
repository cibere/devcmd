import io

import discord
from discord.ext import commands

from .base_section import BaseSection, command


class ModSection(BaseSection):
    @command(name="audit", description="gives you audit logs")
    @commands.guild_only()
    async def cmd_audit(self, ctx: commands.Context, num: int):
        await ctx.channel.typing()
        audits = []
        async for entry in ctx.guild.audit_logs(limit=num):  # type: ignore
            audits.append(
                f"{entry.user} did {entry.action} to {entry.target} with the reason of: {entry.reason}"
            )
        nl = "\n"
        await self.send_info(ctx, "Audit Logs", nl.join(audits))

    @command(name="cleanup", description="cleans up the bots messages")
    async def cmd_cleanup(self, ctx: commands.Context, num: int):
        await ctx.channel.typing()

        count = 0
        async for msg in ctx.history(limit=num, before=ctx.message):
            if msg.author == ctx.me and not (msg.mentions or msg.role_mentions):
                await msg.delete()
                count += 1

        await self.send_success(ctx, f"Cleaned up {count} messages")
