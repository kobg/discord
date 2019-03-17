import requests
import discord
from discord.ext import commands
import random
import os
import youtube_dl

TOKEN = os.environ['DISCORD_BOT_TOKEN']
client = commands.Bot(command_prefix='!')


def __parse__response(response):
    response_json = response.json()
    legends = response_json['data']['children']
    legend_dict = {}
    for legend in legends:
        legend_name = legend['metadata']['legend_name']
        stats = legend['stats']
        stat_dict = {}
        for stat in stats:
            stat_name = stat['metadata']['key']
            value = stat['value']
            stat_dict[stat_name] = value
        legend_dict[legend_name] = stat_dict
    return legend_dict


def get_stats(user_name):
    url = 'https://public-api.tracker.gg/apex/v1/standard/profile/5/{}'.format(user_name)
    headers = {'TRN-Api-Key': os.environ['TRN-Api-Key']}
    r = requests.get(url, headers=headers)

    try:
        return __parse__response(r)
    except:
        return None


@client.event
async def on_ready():
    print("Welcome to Apex Stats!")


@client.command()
async def ap_st(who='<EMPTY_USERNAME>'):
    embed = discord.Embed(title="Stats for **{}**:".format(who), color=0xb90000)
    stats = get_stats(who)
    if stats is None:
        embed.description = "Sorry, couldn't find data for {}.".format(who)
    else:
        sum_dict = {
            'Damage': 0,
            'Kills': 0,
            'Headshots': 0
        }
        for legend in stats:
            legend_stats = stats[legend]
            for key in legend_stats.keys():
                if key in sum_dict:
                    sum_dict[key] += int(legend_stats[key])
        embed.add_field(name='Stats on banners',
                        value='\n'.join(': '.join((key, str(value)))
                                        for key, value in sum_dict.items()),
                        inline=False)
    embed.set_footer(text="courtesy of apex.tracker.gg")
    await client.say(embed=embed)


@client.command()
async def ap_st_detailed(who):
    embed = discord.Embed(title="Stats for **{}**".format(who), color=0xb90000)
    stats = get_stats(who)
    if stats is None:
        embed.description = "Sorry, couldn't find data for {}.".format(who)

    for legend in stats:
        legend_stats = stats[legend]
        embed.add_field(name=legend,
                        value='\n'.join(': '.join((key, str(int(value))))
                                        for key, value in legend_stats.items()),
                        inline=False)
    embed.set_footer(text="courtesy of apex.tracker.gg")
    await client.say(embed=embed)


legend_list = ["Lifeline", "Caustic", "Bangalore", "Gibraltar", "Wraith", "Pathfinder", "Mirage", "Bloodhound"]


@client.command()
async def ap_teamcomp():
    embed = discord.Embed(title="Your random teamcomp is: ", color=0xb90000)
    random.shuffle(legend_list)
    embed.add_field(name='\n'.join(legend_list[:3]), value="\u200b", inline=True)
    embed.set_footer(text="Have fun!")
    await client.say(embed=embed)


@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say("Chat cleared!")


@client.command()
async def ap_help():
    embed = discord.Embed(color=0x0e5634)
    embed.add_field(name="!ap_st {ORIGIN_NAME}", value="Displays damage, kills, headshots (on_banner)",
                    inline=False)
    embed.add_field(name="!ap_st_detailed {ORIGIN_NAME}", value="Displays all on-banner stats", inline=False)
    embed.add_field(name="!ap_teamcomp", value="Generates a random teamcomp", inline=False)
    embed.add_field(name="!clear", value="Clears 100 messages", inline=False)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


songs_url = {
"tilt":"https://www.youtube.com/watch?v=GJDNkVDGM_s",
"rocky":"https://www.youtube.com/watch?v=xSmYAdiXb5M",
"benny":"https://www.youtube.com/watch?v=MK6TXMsvgQg",
"tiger":"https://www.youtube.com/watch?v=btPJPFnesV4",
"90s":"https://www.youtube.com/watch?v=BJ0xBCwkg3E",
"dejavu":"https://youtu.be/dv13gl0a-FA?t=60",
"freestyler":"https://www.youtube.com/watch?v=ymNFyxvIdaM",
"sandstorm":"https://www.youtube.com/watch?v=y6120QOlsfU",
"pole":"https://www.youtube.com/watch?v=UvRsDiOFdzA",
"ziemia":"https://www.youtube.com/watch?v=fwkk6mJmjkg"
}

@client.command()
async def songs():
    embed = discord.Embed(title = "Current song list: ",color=0x0e5634)
    embed.add_field(name="\n".join(songs_url),value="\u200b",inline = True)
    embed.set_footer(text="Use !play <name> ")
    await client.say(embed=embed)

players = {}



@client.command(pass_context=True)
async def play(ctx,url):
    server = ctx.message.server
    connected = client.voice_client_in(server)
    channel = ctx.message.author.voice.voice_channel
    if not connected:
        await client.join_voice_channel(channel)
    voice_client = client.voice_client_in(server)
    if url in songs_url:
        player = await voice_client.create_ytdl_player(songs_url[url])
    else:
        player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def music(ctx,cmd):
    id = ctx.message.server.id
    if cmd == "pause":
        players[id].pause()
    elif cmd == "stop":
        players[id].stop()
    elif cmd == "resume":
        players[id].resume()


client.run(TOKEN)
