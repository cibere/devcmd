import datetime

import discord
from discord.ext import commands


@commands.is_owner()
class BaseSection(commands.Cog):
    async def send_error(self, messageable, message: str) -> None:
        em = discord.Embed(
            title="Error",
            description=message,
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow(),
        )
        await self.send_message(messageable, em)

    async def send_success(self, messageable, message: str) -> None:
        em = discord.Embed(
            title="Success",
            description=message,
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow(),
        )
        await self.send_message(messageable, em)

    async def send_info(self, messageable, title: str, message: str) -> None:
        em = discord.Embed(
            title=title,
            description=message,
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow(),
        )
        await self.send_message(messageable, em)

    async def send_message(self, messageable, embed: discord.Embed) -> None:
        await messageable.send(embed=embed)


def command(*, name: str, description: str, aliases: list[str] = []):
    def inner(func):
        func.cmd_info = {"name": name, "desc": description, "aliases": aliases}
        return func

    return inner
