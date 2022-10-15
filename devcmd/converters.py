from discord.ext import commands

class CodeBlockConvertor(commands.Converter):
    async def convert(self, ctx, block: str):
        return block.replace("```py", "").replace("```", "")