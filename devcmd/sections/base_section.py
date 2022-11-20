from discord.ext import commands


@commands.is_owner()
class BaseSection(commands.GroupCog, group_name="devcmd", aliases=["dc", "dev"]):
    pass
