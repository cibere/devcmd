import inspect

from .base_section import BaseSection, command


class SourceSection(BaseSection):
    @command(
        name="source",
        aliases=["src"],
        description="Gives the source code for the specified command",
    )
    async def cmd_source(self, ctx, *, command_name: str):
        await ctx.channel.typing()
        command = ctx.bot.get_command(command_name)
        if not command:
            return await self.send_error(ctx, f"Command `{command_name}` not found")
        try:
            source_lines, _ = inspect.getsourcelines(command.callback)
        except:
            return await self.send_error(
                ctx, f"I could not find the source code for `{command}`."
            )
        source_text = "".join(source_lines)
        await self.send_info(ctx, f"{command_name}s source code", source_text)

    @command(
        name="file",
        description="Sends the code for the specified file",
    )
    async def cmd_file(self, ctx, file: str):
        await ctx.channel.typing()
        try:
            with open(file, "r", encoding="utf-8") as f:
                code = str(f.read())
        except FileNotFoundError:
            return await self.send_error(ctx, f"I could not file a file at `{file}`")

        name = file.split("/")
        name = name[len(name) - 1]
        await self.send_info(ctx, file, code)
