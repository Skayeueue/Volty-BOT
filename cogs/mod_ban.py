import typing
import nextcord as discord
from nextcord import mentions
from nextcord.embeds import Embed
from nextcord.ext import commands
from nextcord.ext.commands.core import has_permissions
from nextcord.member import Member

class mod_ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderacyjne(ban) - ready")

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: typing.Optional[str] = "Nie podano"):
        if member == ctx.message.author:
            await ctx.reply("\❌ Nie możesz zbanować samego siebie ;)", mention_author=False)
        else:
            zapro = discord.abc.GuildChannel.create_invite(ctx.message.channel, max_uses=3,max_age=2678400)
            embed = discord.Embed(description = f"Zostałeś zbanowany na `{ctx.guild.name}` za `{reason}`\nZaproszenie do serwera: [Kliknij!]({zapro})", color = 0xffff00)
            await member.send(embed = embed)
            await ctx.guild.ban(member, reason=reason)
            await ctx.reply(f"\✅ Zbanowano `{member.name}` za `{reason}`", mention_author=False)
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("\❌ Nie posiadasz permisji do tego! `(ban_members)`", mention_author=False)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `ban <@member> [powód]`", mention_author=False)

    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        ban_list = await ctx.guild.bans()
        member_name, member_tag = member.split("#")

        for ban_entry in ban_list:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_tag):
                await ctx.guild.unban(user)
                await ctx.reply(f"\✅ Odbanowano `{member_name}#{member_tag}`", mention_author=False)
            elif member == ctx.message.author:
                await ctx.reply(f"\❌ Nie możesz odbanować samego siebie ;)")
            else:
                await ctx.reply(f"\❌ Nie znaleziono takiego użytkownika")
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"\❌ Nie posiadasz permisji do tego! `(ban_members)`", mention_author=False)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `ban <nick#tag>`", mention_author=False)
    
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: typing.Optional[str] = "Nie podano"):
        if member == ctx.message.author:
            await ctx.reply("\❌ Nie możesz zbanować samego siebie ;)", mention_author=False)
        else:
            zapro = await discord.abc.GuildChannel.create_invite(ctx.message.channel, max_uses=3,max_age=2678400)
            embed = discord.Embed(description = f"Zostałeś wyrzucony z `{ctx.guild.name}` za `{reason}`\nDołącz ponownie: [Kliknij!]({zapro[0]})", color = 0xffff00)
            await member.send(embed = embed)
            await ctx.guild.kick(member, reason=reason)
            await ctx.reply(f"\✅ Wyrzucono `{member.name}` za `{reason}`", mention_author=False)
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("\❌ Nie posiadasz permisji do tego! `(kick_members)`", mention_author=False)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("\❌ Użyj: `kick <@member> [powód]`", mention_author=False)


def setup(client):
    client.add_cog(mod_ban(client))