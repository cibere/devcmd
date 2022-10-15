import discord

class EmbedPaginator(discord.ui.View):
    def __init__(self, *, user: discord.Member = None, pages: list[discord.Embed]) -> None:
        super().__init__(timeout=None)
        self.user = user
        self.pages = pages
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        if len(self.pages) == 1:
            self.rightButton.disabled=True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user:
            if self.user.id != interaction.user.id:
                await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
                return False
            return True
        else:
            return True

    @discord.ui.button(emoji='⏮️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_text_paginator:first")
    async def firstPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = False
        self.lastPageButton.disabled = False
        
        self.firstPageButton.disabled = True
        self.leftButton.disabled = True
        
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_embed_paginator:left")
    async def leftButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page - 1 == 0:
            self.leftButton.disabled = True
        self.rightButton.disabled = False
        self.current_page -= 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True, custom_id="devcmd_embed_paginator:index")
    async def indexButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple, custom_id="devcmd_embed_paginator:right")
    async def rightButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page + 1 == len(self.pages) - 1:
            self.rightButton.disabled = True
        self.leftButton.disabled = False
        self.current_page += 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(emoji='⏭️', style=discord.ButtonStyle.blurple, custom_id="devcmd_text_paginator:last")
    async def lastPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = True
        self.lastPageButton.disabled = True
        
        self.firstPageButton.disabled = False
        self.leftButton.disabled = False
        
        self.current_page = len(self.pages) - 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

class TextPaginator(discord.ui.View):
    def __init__(self, *, user: discord.Member = None, pages: list[str]) -> None:
        super().__init__(timeout=None)
        self.user = user
        self.pages = pages
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        if len(self.pages) == 1:
            self.rightButton.disabled=True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user:
            if self.user.id != interaction.user.id:
                await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
                return False
            return True
        else:
            return True

    @discord.ui.button(emoji='⏮️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_text_paginator:first")
    async def firstPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = False
        self.lastPageButton.disabled = False
        
        self.firstPageButton.disabled = True
        self.leftButton.disabled = True
        
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(content=self.pages[self.current_page], view=self)

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_text_paginator:left")
    async def leftButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page - 1 == 0:
            self.leftButton.disabled = True
        self.rightButton.disabled = False
        self.current_page -= 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(content=self.pages[self.current_page], view=self)

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True, custom_id="devcmd_text_paginator:index")
    async def indexButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple, custom_id="devcmd_text_paginator:right")
    async def rightButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page + 1 == len(self.pages) - 1:
            self.rightButton.disabled = True
        self.leftButton.disabled = False
        self.current_page += 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(content=self.pages[self.current_page], view=self)
    
    @discord.ui.button(emoji='⏭️', style=discord.ButtonStyle.blurple, custom_id="devcmd_text_paginator:last")
    async def lastPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = True
        self.lastPageButton.disabled = True
        
        self.firstPageButton.disabled = False
        self.leftButton.disabled = False
        
        self.current_page = len(self.pages) - 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(content=self.pages[self.current_page], view=self)

class ViewPaginator(discord.ui.View):
    def __init__(self, *, user: discord.Member = None, pages: list[discord.ui.View]) -> None:
        """USE 'ViewPaginator.generate(...)' TO GENERATE THE VIEW FOR YOUR FIRST VIEW TO BE ON THE FIRST PAGE"""
        super().__init__(timeout=None)
        self.user = user
        self.pages = pages
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        if len(self.pages) == 1:
            self.rightButton.disabled=True

    async def generate(user: discord.Member, pages: list[discord.ui.View]):
        paginator = ViewPaginator(user, pages)
        await paginator.add_view(pages[0])
        return paginator

    async def add_view(self, view: discord.ui.View) -> None:
        for item in view.children:
            self.add_item(item)
    
    async def clear_views(self) -> None:
        for item in self.children:
            if not item.custom_id.startswith("devcmd"):
                self.remove_item(item)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user:
            if self.user.id != interaction.user.id:
                await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
                return False
            return True
        else:
            return True

    @discord.ui.button(emoji='⏮️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_text_paginator:first")
    async def firstPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = False
        self.lastPageButton.disabled = False
        
        self.firstPageButton.disabled = True
        self.leftButton.disabled = True
        
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_text_paginator:left")
    async def leftButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page - 1 == 0:
            self.leftButton.disabled = True
            self.firstPageButton.disabled = True
        self.rightButton.disabled = False
        self.lastPageButton.disabled = False
        self.current_page -= 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True, custom_id="devcmd_text_paginator:index")
    async def indexButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple, custom_id="devcmd_text_paginator:right")
    async def rightButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page + 1 == len(self.pages) - 1:
            self.rightButton.disabled = True
            self.lastPageButton.disabled = True
        self.leftButton.disabled = False
        self.firstPageButton.disabled = False
        self.current_page += 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page])
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(emoji='⏭️', style=discord.ButtonStyle.blurple, custom_id="devcmd_text_paginator:last")
    async def lastPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = True
        self.lastPageButton.disabled = True
        
        self.firstPageButton.disabled = False
        self.leftButton.disabled = False
        
        self.current_page = len(self.pages) - 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page])
        await interaction.response.edit_message(view=self)

class ViewEmbedPaginator(discord.ui.View):
    def __init__(self, *, user: discord.Member = None, pages: list[list[discord.Embed, discord.ui.View]]) -> None:
        """USE 'ViewEmbedPaginator.generate(...)' TO GENERATE THE VIEW FOR YOUR FIRST VIEW TO BE ON THE FIRST PAGE"""
        super().__init__(timeout=None)
        self.user = user
        self.pages = pages
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        if len(self.pages) == 1:
            self.rightButton.disabled=True

    async def generate(user: discord.Member, pages: list[list[discord.Embed, discord.ui.View]]):
        paginator = ViewEmbedPaginator(user, pages)
        await paginator.add_view(pages[0])
        return paginator

    async def add_view(self, view: discord.ui.View) -> None:
        for item in view.children:
            self.add_item(item)
    
    async def clear_views(self) -> None:
        for item in self.children:
            if not item.custom_id.startswith("devcmd"):
                self.remove_item(item)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user:
            if self.user.id != interaction.user.id:
                await interaction.response.send_message(f"Your not {self.user.mention}... are you?", ephemeral=True)
                return False
            return True
        else:
            return True

    @discord.ui.button(emoji='⏮️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_text_paginator:first")
    async def firstPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = False
        self.lastPageButton.disabled = False
        
        self.firstPageButton.disabled = True
        self.leftButton.disabled = True
        
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page][1])
        await interaction.response.edit_message(view=self, embed=self.pages[self.current_page][0])

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True, custom_id="devcmd_text_paginator:left")
    async def leftButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page - 1 == 0:
            self.leftButton.disabled = True
            self.firstPageButton.disabled = True
        self.rightButton.disabled = False
        self.lastPageButton.disabled = False
        self.current_page -= 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page][1])
        await interaction.response.edit_message(view=self, embed=self.pages[self.current_page][0])

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True, custom_id="devcmd_text_paginator:index")
    async def indexButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple, custom_id="devcmd_text_paginator:right")
    async def rightButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.current_page + 1 == len(self.pages) - 1:
            self.rightButton.disabled = True
            self.lastPageButton.disabled = True
        self.leftButton.disabled = False
        self.firstPageButton.disabled = False
        self.current_page += 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page][1])
        await interaction.response.edit_message(view=self, embed=self.pages[self.current_page][0])
    
    @discord.ui.button(emoji='⏭️', style=discord.ButtonStyle.blurple, custom_id="devcmd_text_paginator:last")
    async def lastPageButton(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.rightButton.disabled = True
        self.lastPageButton.disabled = True
        
        self.firstPageButton.disabled = False
        self.leftButton.disabled = False
        
        self.current_page = len(self.pages) - 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await self.clear_views()
        await self.add_view(self.pages[self.current_page][1])
        await interaction.response.edit_message(view=self, embed=self.pages[self.current_page][0])