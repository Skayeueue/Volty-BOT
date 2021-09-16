import datetime
import nextcord as discord
from nextcord import client
from nextcord.ext import commands
from nextcord.ui import view
import DiscordUtils

class tests(commands.Cog):

    def __init__(self, client):
        self.client = client

music = DiscordUtils.Music()

@commands.Cog.listener()
async def on_ready():
    print("tests - ready")

    @commands.command()
    async def join(ctx):
        await ctx.author.voice.channel.connect()  # Joins author's voice channel
        embed = discord.Embed(title="\✅ Joined!", color=0xffff00)
        ctx.send(embed=embed)


    @commands.command()
    async def leave(ctx):
        await ctx.voice_client.disconnect()
        embed = discord.Embed(title="\✅ Leaved!", color=0xffff00)
        ctx.send(embed=embed)


    @commands.command(aliases=["p"])
    async def play(ctx, *, url):
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            embed = discord.Embed(title="\🎶 Now playing", description=f"{song.name}", color=0xffff00)
            await ctx.send(embed=embed)
        else:
            song = await player.queue(url, search=True)
            embed1 = discord.Embed(title="\🎶 Added to queue", description=f"{song.name}", color=0xffff00)
            await ctx.send(embed=embed1)


    @commands.command(aliases=["pa"])
    async def pause(ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
    #    embed = discord.Embed(title="\🎶 Added to queue", description=f"{song.name}", color=0xffff00)
        await ctx.send(f"Paused {song.name}")


    @commands.command(aliases=["re"])
    async def resume(ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed {song.name}")


    @commands.command(aliases=["st"])
    async def stop(ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.send("Stopped")


    @commands.command(aliases="lp")
    async def loop(ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for {song.name}")
        else:
            await ctx.send(f"Disabled loop for {song.name}")


    @commands.command(aliases=["qu"])
    async def queue(ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        await ctx.send(f'{([song.name for song in player.current_queue()])}')


    @commands.command(aliases=["now"])
    async def np(ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        await ctx.send(song.name)


    @commands.command()
    async def skip(ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
        else:
            await ctx.send(f"Skipped {data[0].name}")


    @commands.command(aliases=["vol"])
    async def volume(ctx, vol):
        player = music.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol) / 100)
        await ctx.send(f"Changed volume for {song.name} to {volume * 100}%")


    @commands.command(aliases=["rem", "rmv"])
    async def remove(ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        await ctx.send(f"Removed {song.name} from queue")

def setup(client):
    client.add_cog(tests(client))