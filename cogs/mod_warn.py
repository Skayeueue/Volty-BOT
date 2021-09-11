import typing
import nextcord as discord
from nextcord import mentions
from nextcord.ext import commands
from nextcord.ext.commands.cog import Cog
import random
import sqlite3
import time
from datetime import datetime, timezone
from nextcord.ext.commands.core import command, has_permissions
from pytz import timezone

class mod_warn(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderacyjne(warn) - ready")
        db = sqlite3.connect("warns.db")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS warns(guild_id INT, user_id INT, reason STR, author_id INT, author_name STR, warn_time INT)")
        cursor.close()
        db.close()

    @commands.command()
    @has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        db = sqlite3.connect("warns.db")
        cursor = db.cursor()
        rok = time.strftime("%d-%m-%Y", time.gmtime())
        godzina = time.strftime("%H", time.gmtime())
        minuta = time.strftime("%M", time.gmtime())
        sekunda = time.strftime("%S", time.gmtime())
        nmrb = 2
        g_cest = int(godzina) + int(nmrb)
        czas = (f"{g_cest}:{minuta}:{sekunda} {rok}")
        cursor.execute("INSERT INTO warns(guild_id, user_id, reason, author_id, author_name, warn_time) VALUES(?, ?, ?, ?, ?, ?)", (ctx.author.guild.id, member.id, reason, ctx.author.id, ctx.message.author.name, czas))
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(f"\✅ Zwarnowałeś `{member}` za `{reason}`", mention_author=False)
    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("\❌ Nie posiadasz permisji do tego! `(kick_members)`", mention_author=False)

    @commands.command(aliases=["warns"])
    async def warnlist(self, ctx, member: typing.Optional[discord.Member]):
        if member is None:
            member = ctx.message.author
        db = sqlite3.connect("warns.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM warns WHERE guild_id = {ctx.author.guild.id} AND user_id = {member.id}")
        wynik = cursor.fetchall()
        embed = discord.Embed(
            description = "",
            color = 0xffff00
        )
        embed.set_author(name=f"Warny użytkownika {member.display_name}", icon_url=f"{member.avatar}")
        cursor.execute(f"SELECT author_name FROM warns WHERE guild_id = {ctx.author.guild.id} AND user_id = {member.id}")
        warnauthor_name = cursor.fetchone()
        cursor.execute(f"SELECT warn_time FROM warns WHERE guild_id = {ctx.author.guild.id} AND user_id = {member.id}")
        warntime = cursor.fetchone()
        nmr = 1
        if not wynik:
            await ctx.reply(f"\❌ `{member.name}` nie posiada warnów!", mention_author=False)
        else:
            for warn in wynik: 
                embed.add_field(
                    name=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬(`ID: {nmr}`)",
                    value=f"`-` Powód: `{warn[2]}`\n`-` Administrator: `{warnauthor_name[0]}`\n`-` Data: `{warntime[0]}`",
                    inline=False
                    )
                nmr += 1
            await ctx.reply(embed=embed, mention_author=False)
        cursor.close()
        db.close()

    @commands.command()
    @has_permissions(kick_members=True)
    async def delwarn(self, ctx, member: typing.Optional[discord.Member], id: int):
        if member is None:
            member = ctx.message.author
        db = sqlite3.connect("warns.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM warns WHERE guild_id = {ctx.author.guild.id} AND user_id = {member.id}")
        wynik = cursor.fetchall()
        nm = 1
        if wynik:
            for warn in wynik:
                if nm == id:
                    cursor.execute(f"DELETE FROM warns WHERE guild_id = ? AND user_id = ? AND reason = ? AND author_id = ? AND author_name = ? AND warn_time = ?", (warn[0],warn[1],warn[2],warn[3],warn[4],warn[5]))
                    await ctx.reply(f"\✅ Usunięto warn o id `{nm}` użytkownikowi `{member.name}`", mention_author=False)
                nm += 1
        else:
            await ctx.reply(f"\❌ `{member.name}` nie posiada warnów!", mention_author=False)
        db.commit()
        cursor.close()
        db.close()
    @delwarn.error
    async def delwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("\❌ Nie posiadasz permisji do tego! `(kick_members)`", mention_author=False)




def setup(client):
    client.add_cog(mod_warn(client))