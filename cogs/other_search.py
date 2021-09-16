import nextcord as discord
from nextcord import mentions
from nextcord.activity import Spotify
from nextcord.ext import commands
from urllib.parse import quote_plus
from nextcord.ui import view

class GoogleSearch(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'
        text = f'🔎 Google: "{query}"'
        self.add_item(discord.ui.Button(label = text.replace("+", " "), url = url, style = discord.ButtonStyle.success))
class YoutubeSearch(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f'https://www.youtube.com/results?search_query={query}'
        text = f'🎬 YouTube: "{query}"'
        self.add_item(discord.ui.Button(label = text.replace("+", " "), url = url, style = discord.ButtonStyle.success))
class SpotifySearch(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        final = query.replace("+", "%20")
        url = f'https://open.spotify.com/search/{final}'
        text = f'🎵 Spotify: "{query}"'
        self.add_item(discord.ui.Button(label = text.replace("+", " "), url = url, style = discord.ButtonStyle.success))
class AllSearch(discord.ui.View):
    async def google(self, query1: str):
        super().__init__()
        query1 = quote_plus(query1)
        url1 = f'https://www.google.com/search?q={query1}'
        text1 = f'🔎 Google: "{query1}"'
        self.add_item(discord.ui.Button(label = text1.replace("+", " "), url = url1, style = discord.ButtonStyle.success))
    async def youtube(self, query2: str):
        super().__init__()
        query2 = quote_plus(query2)
        url2 = f'https://www.youtube.com/results?search_query={query2}'
        text2 = f'🎬 YouTube: "{query2}"'
        self.add_item(discord.ui.Button(label = text2.replace("+", " "), url = url2, style = discord.ButtonStyle.success))
    async def spotify(self, query3: str):
        super().__init__()
        query3 = quote_plus(query3)
        final3 = query3.replace("+", "%20")
        url3 = f'https://open.spotify.com/search/{final3}'
        text3 = f'🎵 Spotify: "{query3}"'
        self.add_item(discord.ui.Button(label = text3.replace("+", " "), url = url3, style = discord.ButtonStyle.success))

class other_search(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("other(search) - ready")

    @commands.command()
    async def google(self, ctx, *, query):
        if len(query) >= 80:
            await ctx.reply("\❌ Twoje pytanie/klucz wyszukiwania nie może mieć więcej niż 80 znaków", mention_author=False)
        await ctx.reply(f"\✅ Wyniki Twojego wyszukiwania:", view=GoogleSearch(query))
    @google.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `google <pytanie/klucz wyszukiwania>`", mention_author=False)

    @commands.command()
    async def youtube(self, ctx, *, query):
        if len(query) >= 80:
            await ctx.reply("\❌ Tytuł filmu nie może mieć więcej niż 80 znaków, mention_author=False", mention_author=False)
        await ctx.reply(f"\✅ Wyniki Twojego wyszukiwania:", view=YoutubeSearch(query), mention_author=False)
    @youtube.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `youtube <tytuł filmu>`", mention_author=False)

    @commands.command()
    async def spotify(self, ctx, *, query):
        if len(query) >= 80:
            await ctx.reply("\❌ Tytuł piosenki nie może mieć więcej niż 80 znaków, mention_author=False", mention_author=False)
        await ctx.reply(f"\✅ Wyniki Twojego wyszukiwania:", view=SpotifySearch(query), mention_author=False)
    @spotify.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `spotify <tytuł piosenki>`", mention_author=False)

    @commands.command(aliases=["wyszukaj"])
    async def search(self, ctx, *, query):
        if len(query) >= 80:
            await ctx.reply("\❌ Twój klucz wyszukiwania nie może mieć więcej niż 80 znaków, mention_author=False", mention_author=False)
        await ctx.reply(f"\✅ Wyniki Twojego wyszukiwania:", view=AllSearch(query), mention_author=False)
    @spotify.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `search/wyszukaj <tytuł piosenki>`", mention_author=False)

def setup(client):
    client.add_cog(other_search(client))