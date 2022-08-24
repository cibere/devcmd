import discord

class Paginator(discord.ui.View):
    def __init__(self, user, pages):
        self.user = user
        self.pages = pages
        self.current_page = 0
        super().__init__(timeout=None)
        self._dc_hb_num.label = f"{self.current_page + 1}/{len(self.pages)}"
        if len(self.pages) == 1:
            self._dc_hb_right.disabled=True

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True)
    async def _dc_hb_left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
        if self.current_page - 1 == 0:
            self._dc_hb_left.disabled = True
        self._dc_hb_right.disabled = False
        self.current_page -= 1
        self._dc_hb_num.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True)
    async def _dc_hb_num(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple)
    async def _dc_hb_right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            return await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
        if self.current_page + 1 == len(self.pages) - 1:
            self._dc_hb_right.disabled = True
        self._dc_hb_left.disabled = False
        self.current_page += 1
        self._dc_hb_num.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)