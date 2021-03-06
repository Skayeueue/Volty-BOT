import typing
import nextcord
from nextcord import mentions
from nextcord.ext import commands
import sqlite3
from nextcord.ext.commands.core import has_permissions
from nextcord.ext.commands.errors import MissingPermissions
import time
import os

def get_prefix(client, message):
    db = sqlite3.connect("prefix.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT prefix FROM info WHERE guild_id = {message.guild.id}")
    wynik = cursor.fetchone()
    if wynik is None:
        prefix = ">"
    else:
        prefix = wynik
    cursor.close()
    db.close()
    return prefix

def set_guild_role(user : nextcord.User):
    db = sqlite3.connect("verify.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT guild_id FROM role")
    wynik = cursor.fetchone()
    if wynik is None:
        cursor.execute(f"UPDATE role SET guild_id = {user.guild.id}", (user.guild.id,))
    cursor.close()
    db.commit()
    db.close()

intents = nextcord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix=get_prefix)
client.remove_command("help")

@client.event
async def on_ready():
    db = sqlite3.connect("prefix.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS info(guild_id INT, prefix STR)")
    cursor.close()
    db.close()
    set_guild_role
    print("main - ready")
    await client.change_presence(activity=nextcord.Activity(type = nextcord.ActivityType.playing, name="Ładowanie..."))
    time.sleep(3)
    await client.change_presence(activity=nextcord.Activity(type = nextcord.ActivityType.playing, name=f"⚡ Jestem na {len(client.guilds)} serwerach"))

#@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction("❌")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You are missing the required permissions to run this command!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send("Something about your input was wrong, please check your input and try again!")
    else:
        await ctx.send("Oh no! Something went wrong while running the command!")


@client.event
async def on_message(message):
    prfx = get_prefix(client, message)
    embed = nextcord.Embed(title="", description=f"\⚡ Mój prefix na tym serwerze to: `{prfx[0]}`\n\🔗 Lista komend: `{prfx[0]}help`", color=0xfffa00)
    if client.user.mentioned_in(message):
        await message.reply(embed=embed, mention_author=False)
    await client.process_commands(message)

@client.command()
@has_permissions(administrator=True)
async def prefix(ctx, prefix):
    db = sqlite3.connect("prefix.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT guild_id FROM info WHERE guild_id = {ctx.author.guild.id}")
    wynik = cursor.fetchone()
    if wynik is None:
        cursor.execute("INSERT INTO info(guild_id, prefix) VALUES(?, ?)", (ctx.author.guild.id, prefix))
    else:
        cursor.execute("UPDATE info SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id))
    await ctx.reply(f"\✅ Ustawiono prefix na `{prefix}`", mention_author=False)
    db.commit()
    cursor.close()
    db.close()
@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("\❌ Nie posiadasz permisji do tego! `(administrator)`", mention_author=False)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("\❌ Użyj: `prefix <prefix>`", mention_author=False)

@client.command()
async def help(ctx, cat: typing.Optional[str]):
    embed = nextcord.Embed(
        color = 0xffff00
    )
    embed.add_field(
        name = "\💡 Informacje",
        value = "Właścicel/Developer: `Skayee#2115`\nArgumenty: `<arg> - potrzebne`, `[arg] - opcjonalne`\nJęzyk: Python, Strona: [Kliknij!](https://volty.xyz/)"
    )
    embed.add_field(
        name = "\📚 Kategorie",
        value = "`moderacyjne/mod, soon`"
    )
    mod = nextcord.Embed(
        color = 0x0377fc
    )
    mod.add_field(
        name = "\📘 Moderacyjne - Ban, Unban, Kick",
        value = "`ban <@member> [powód]`\n`unban <nick#tag>`\n`kick <@member> <powód>`"
    )
    if cat == None:
        await ctx.reply(embed = embed, mention_author=False)
    elif cat == "moderacyjne" or "Moderacyjne" or "mod" or "Mod":
        await ctx.reply(embed = mod, mention_author=False)

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

import config
client.run(config.token)