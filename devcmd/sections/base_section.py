from discord.ext import commands


@commands.is_owner()
class BaseSection(commands.Cog):
    pass


def command(*, name: str, description: str, aliases: list[str] = []):
    def inner(func):
        func.cmd_info = {"name": name, "desc": description, "aliases": aliases}
        return func

    return inner
