import discord

class Paginator(discord.ui.View):
    def __init__(self, user, pages):
        self.user = user
        self.pages = pages
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        if len(self.pages) == 1:
            self.rightButton.disabled=True
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user.id != interaction.user.id:
            await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
            return False

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True)
    async def leftButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page - 1 == 0:
            self.leftButton.disabled = True
        self.rightButton.disabled = False
        self.current_page -= 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True)
    async def indexButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple)
    async def rightButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page + 1 == len(self.pages) - 1:
            self.rightButton.disabled = True
        self.leftButton.disabled = False
        self.current_page += 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)