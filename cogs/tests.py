import datetime
import nextcord as discord
from nextcord import client
from nextcord.ext import commands
from nextcord.ui import view
import time

class testButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="1", style=discord.ButtonStyle.primary)
    async def button1(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 1")
        self.value = True
    @discord.ui.button(label="2", style=discord.ButtonStyle.primary)
    async def button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 2")
        self.value = True
    @discord.ui.button(label="3", style=discord.ButtonStyle.primary)
    async def button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 3")
        self.value = True
    @discord.ui.button(label="4", style=discord.ButtonStyle.primary)
    async def button4(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 4")
        self.value = True
    @discord.ui.button(label="5", style=discord.ButtonStyle.primary)
    async def button5(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 5")
        self.value = True
    @discord.ui.button(label="6", style=discord.ButtonStyle.primary)
    async def button6(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 6")
        self.value = True
    @discord.ui.button(label="7", style=discord.ButtonStyle.primary)
    async def button7(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 7")
        self.value = True
    @discord.ui.button(label="8", style=discord.ButtonStyle.primary)
    async def button8(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 8")
        self.value = True
    @discord.ui.button(label="9", style=discord.ButtonStyle.primary)
    async def button9(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Kliknięto 9")
        self.value = True
        self.stop

class tests(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("tests - ready")

    @commands.command()
    async def test(self, ctx):
        view = testButtons()
        await ctx.send("Przycisk", view = view)
        await view.wait()

def setup(client):
    client.add_cog(tests(client))