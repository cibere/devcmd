import io

import discord
from discord.ext import commands


class ModSection(commands.Cog):
    @commands.command(parent="devcmd", name="audit", description="gives you audit logs")
    @commands.guild_only()
    async def audit(self, ctx: commands.Context, num: int):
        await ctx.channel.typing()
        audits = []
        async for entry in ctx.guild.audit_logs(limit=num):  # type: ignore
            audits.append(
                f"{entry.user} did {entry.action} to {entry.target} with the reason of: {entry.reason}"
            )
        nl = "\n"
        embed = discord.Embed(
            color=discord.Color.blue(), title="Audit", description=nl.join(audits)
        )
        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.send(
                file=discord.File(
                    filename="Audit Logs",
                    fp=io.BytesIO(str(embed.description).encode("utf-8")),
                )
            )

    @commands.command(
        parent="devcmd", name="cleanup", description="cleans up the bots messages"
    )
    async def cleanup(self, ctx: commands.Context, num: int):
        await ctx.channel.typing()

        count = 0
        async for msg in ctx.history(limit=num, before=ctx.message):
            if msg.author == ctx.me and not (msg.mentions or msg.role_mentions):
                await msg.delete()
                count += 1

        embed = discord.Embed(
            color=discord.Color.green(),
            description=f"Cleaned up {count} messages",
        )
        await ctx.author.send(embed=embed)
