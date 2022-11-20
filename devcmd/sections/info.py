import discord
from discord.ext import commands

from .base_section import BaseSection, command

masterEmbeds = {
    "doc": discord.Embed(
        title="Devcmd Documentation",
        description="https://gist.github.com/cibere/da22060df5ab6282b452e972f08d269b",
        color=discord.Color.blue(),
    ),
    "git": discord.Embed(
        title="Devcmd Github",
        description="""[Stable/Main Version](https://github.com/cibere/devcmd)\n[Development/Beta Version](https://github.com/cibere/devcmd/tree/beta)""",
        color=discord.Color.blue(),
    ),
    "color": discord.Embed(
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
        color=discord.Color.blue(),
    ),
}


class infoDropdown(discord.ui.Select):
    def __init__(self, owner, docDef=False, gitDef=False, colorDef=False):
        self.owner = owner

        options = [
            discord.SelectOption(
                label="Docs",
                description="Gives you the devcmd docs",
                value="doc",
                default=docDef,
            ),
            discord.SelectOption(
                label="Github",
                description="Gives you the devcmd github page",
                value="git",
                default=gitDef,
            ),
            discord.SelectOption(
                label="Embed Colors",
                description="Gives you info about the coloring of embeds",
                value="color",
                default=colorDef,
            ),
        ]

        super().__init__(
            placeholder="Choose a option", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner.id:
            return await interaction.response.send_message(
                f"This is for my owner(s) only.", ephemeral=True
            )
        val = self.values[0]
        if val == "doc":
            em = masterEmbeds["doc"]
            view = infoDropdownView(self.owner, docDef=True)
        elif val == "git":
            em = masterEmbeds["git"]
            view = infoDropdownView(self.owner, gitDef=True)
        elif val == "color":
            em = masterEmbeds["color"]
            view = infoDropdownView(self.owner, colorDef=True)
        await interaction.response.edit_message(embed=em, view=view)  # type: ignore


class infoDropdownView(discord.ui.View):
    def __init__(self, owner, docDef=False, gitDef=False, colorDef=False):
        super().__init__(timeout=None)
        self.owner = owner
        self.x = infoDropdown(owner, docDef, gitDef, colorDef)
        self.add_item(self.x)

    @discord.ui.button(label="X", style=discord.ButtonStyle.red, row=2)
    async def _exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner.id:
            return await interaction.response.send_message(
                f"This is for my owner(s) only.", ephemeral=True
            )
        self.x.disabled = True
        self._exit.disabled = True
        await interaction.response.edit_message(view=self)


class InfoSection(BaseSection):
    @command(name="info", description="gives you info about devcmd")
    async def cmd_info(self, ctx: commands.Context, _: str = ""):
        em = discord.Embed(title="Please make a selection", color=discord.Color.blue())
        await ctx.send(embed=em, view=infoDropdownView(ctx.author))

    @command(name="version", description="gives you the devcmd version your running")
    async def cmd_version(self, ctx: commands.Context, _: str = ""):
        import devcmd

        await self.send_info(ctx, "", f"Running Devcmd Version {devcmd.VERSION}")
        del devcmd
