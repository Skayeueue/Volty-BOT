import nextcord as discord
from nextcord import mentions
from nextcord import channel
from nextcord import message
from nextcord.ext import commands
from nextcord.ext.commands.core import has_permissions
import time

class mod_chat(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderacyjne(chat) - ready")

    @commands.command(aliases=["sm"])
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int):
        await ctx.channel.edit(slowmode_delay=time)
        await ctx.send(f"\✅ Ustawiono slowmode kanału na `{time}` sekund")
    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("\❌ Nie posiadasz permisji do tego! `(manage_channels)`", mention_author=False)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `slowmode <czas w sekundach>`", mention_author=False)
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("\❌ Użyj: `slowmode <czas w sekundach>`", mention_author=False)
        elif isinstance(error, ValueError):
            await ctx.reply("\❌ Użyj: `slowmode <czas w sekundach>`", mention_author=False)
    
    @commands.command(aliases=["purge"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, ile: int):
        totalile = int(ile) + int(1)
        await ctx.channel.purge(limit=totalile)
        if ile == 1:
            msg = await ctx.send(f"\✅ Usunięto `{ile}` wiadomość!")
        else:
            msg = await ctx.send(f"\✅ Usunięto `{ile}` wiadomości!")
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("\❌ Nie posiadasz permisji do tego! `(manage_channels)`", mention_author=False)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `clear <liczba (max 99)>`", mention_author=False)
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("\❌ Użyj: `clear <liczba (max 99)>`", mention_author=False)
        elif isinstance(error, ValueError):
            await ctx.reply("\❌ Użyj: `clear <liczba (max 99)>`", mention_author=False)


def setup(client):
    client.add_cog(mod_chat(client))