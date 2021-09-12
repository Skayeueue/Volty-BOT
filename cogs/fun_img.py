import nextcord as discord
from nextcord.ext import commands

class fun_img(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("fun(img) - ready")

    @commands.command()
    async def rip(self, ctx, member: discord.Member):
        if not member:
            member = ctx.message.author
        

def setup(client):
    client.add_cog(fun_img(client))