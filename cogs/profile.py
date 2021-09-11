import sqlite3
import discord as discord
from discord.ext import commands

def jakniemaxp(user: discord.User):
    db = sqlite3.connect("profile.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT xp FROM levels WHERE user_id = {user.id}")
    xp = cursor.fetchone()
    if xp:
        return
    if xp == None:
        sql = "INSERT INTO levels(user_id, xp) VALUES(?,?)"
        val = (user.id, 0)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

class profile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("profile - ready")
        db = sqlite3.connect("profile.db")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS levels(user_id STR, user_name STR, xp INT, level INT)")
        cursor.close()
        db.close()

#    @commands.command()
    async def profile(self, ctx, member):
        if not member:
            member = ctx.message.author
        db = sqlite3.connect("profile.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT xp FROM level WHERE user_name = {member.name} AND user_id = {member.id}")
        xp = cursor.fetchone()
        await ctx.send(xp)
        cursor.close()
        db.close()

#    @commands.command()
    async def givexp(self, ctx, member: discord.Member, ile):
        if not member:
            member = ctx.message.author
#        jakniemaxp(member.id)
        db = sqlite3.connect("profile.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT xp FROM levels WHERE user_id = {member.id}")
        expp= cursor.fetchone()
        if expp is None:
            await ctx.send('Error')
        exp, = expp
        x = exp+int(ile)
        cursor.execute(f"UPDATE levels SET xp = ? WHERE user_id = ?", (x, {member.id}))

def setup(client):
    client.add_cog(profile(client))