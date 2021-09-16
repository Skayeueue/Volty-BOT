from os import curdir
import nextcord as discord
from nextcord import embeds
from nextcord import client
from nextcord.ext import commands
from nextcord.ext.commands.core import command
from nextcord.role import RoleTags
from nextcord.ui import view
import sqlite3
from main import set_guild_role

def get_role(client, message):
    db = sqlite3.connect("verify.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT role_id FROM role WHERE guild_id = {message.guild.id}")
    wynik = cursor.fetchone()
    if wynik is None:
        message.channel.send("\❌ Ustaw role!")
    else:
        rola = wynik
    cursor.close()
    db.close()
    return rola

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
        db = sqlite3.connect("verify.db")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS role(guild_id INT, role_id STR)")
        cursor.close()
        db.close()

    @commands.command()
    async def weryfikacja(self, ctx):
        view = verifyButtons()
        await ctx.send("Kliknij przycisk `✅ Zweryfikuj się` aby uzyskać dostęp do serwera.", view = view)
        await view.wait()

    @commands.command()
    async def setverifyrole(self, ctx, role):
        set_guild_role(ctx.author)
        db = sqlite3.connect("verify.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT role_id FROM role WHERE guild_id = {ctx.author.guild.id}")
        rola = cursor.fetchone()
        if rola:
            await ctx.send("\❌ Rola jest już ustawiona!")
        else:
            cursor.execute("UPDATE role SET role_id = ? WHERE guild_id = ?", (role, ctx.author.guild.id))
        cursor.close()
        db.commit()
        db.close()

def setup(client):
    client.add_cog(mod_verify(client))