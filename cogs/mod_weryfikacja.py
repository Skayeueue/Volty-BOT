import nextcord as discord
from nextcord import embeds
from nextcord.ext import commands
from nextcord.ui import view

class verifyButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="✅ Zweryfikuj się!", style=discord.ButtonStyle.success)
    async def weryfikacja(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.user.send(f"\✅ Zweryfikowałeś się na **{interaction.guild.name}**")
        self.value = True
        self.stop

class mod_verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("mod(verify) - ready")

    @commands.command()
    async def weryfikacja(self, ctx):
        view = verifyButtons()
        await ctx.send("Kliknij przycisk `✅ Zweryfikuj się` aby uzyskać dostęp do serwera.", view = view)
        await view.wait()

def setup(client):
    client.add_cog(mod_verify(client))