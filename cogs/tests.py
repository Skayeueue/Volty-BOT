import nextcord
from nextcord import client
from nextcord.ext import commands
from nextcord.ui import view

class tests(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("tests - ready")

def setup(client):
    client.add_cog(tests(client))