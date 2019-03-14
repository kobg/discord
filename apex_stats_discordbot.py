#Mostly Thuleq's work

import requests
import json
import discord
import asyncio
from discord.ext import commands
import random

TOKEN = 'GET YOUR OWN BOT TOKEN'
client = commands.Bot(command_prefix = '!')

def get_stats(user_name):
    url = 'https://public-api.tracker.gg/apex/v1/standard/profile/5/{}'.format(user_name)
    headers = {'GET YOUR OWN API KEY FROM apex.tracker.gg'}
    r = requests.get(url, headers=headers)

    response = r.json()
    if 'errors' in response:
        return None
    legends = response['data']['children']
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
@client.event
async def on_ready():
    print("rd")
@client.command()
async def ap_st(who):
    embed=discord.Embed(title="Stats for {}".format(who),color=0xb90000)
    stats = get_stats(who)
    DamageValue = 0
    KillsValue = 0
    HeadshotsValue = 0
    if stats is None:
        print("error msg")
    for legend in stats:
        legend_stats = stats[legend]
        for stat, value in legend_stats.items():
            if stat == "Damage":
                DamageValue += value
            if stat == "Kills":
                KillsValue += value
            if stat == "Headshots":
                HeadshotsValue += value
            print(legend,stat,value)
    embed.add_field(name="Damage (on banners)", value=int(DamageValue), inline=False)
    embed.add_field(name="Kills (on banners)", value=int(KillsValue), inline=False)
    embed.add_field(name="Headshots (on banners)", value=int(HeadshotsValue), inline=False)
    embed.set_footer(text="courtesy of apex.tracker.gg")
    await client.say(embed=embed)

@client.command()
async def ap_st_detailed(who):
    embed=discord.Embed(title="Stats for {}".format(who),color=0xb90000)
    stats = get_stats(who)
    helpvalue = 0
    if stats is None:
        print("error msg")
    for legend in stats:
        legend_stats = stats[legend]
        embed.add_field(name=legend, value=legend_stats, inline=False)
        #await client.say("{} {}".format(legend,legend_stats))
    embed.set_footer(text="courtesy of apex.tracker.gg")
    await client.say(embed=embed)

@client.command()
async def ap_teamcomp():
    embed=discord.Embed(title="Your random teamcomp is: ",color=0xb90000)
    tab = ["Lifeline","Caustic","Bangalore","Gibraltar","Wraith","Pathfinder","Mirage","Bloodhound"]
    for x in range(0,3):
        d = random.randint(0,len(tab)-1)
        embed.add_field(name=tab[d], value="\u200b", inline=True)
        del(tab[d])
    embed.set_footer(text="Have fun!")
    await client.say(embed=embed)
    tab = ["Lifeline","Caustic","Bangalore","Gibraltar","Wraith","Pathfinder","Mirage","Bloodhound"]

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
    embed=discord.Embed(color=0x0e5634)
    embed.add_field(name="!ap_st {ORIGIN_NAME}", value="Displays damage, kills, headshots (on_banner)", inline=False)
    embed.add_field(name="!ap_st_detailed {ORIGIN_NAME}", value="Displays all on-banner stats", inline=False)
    embed.add_field(name="!ap_teamcomp", value="Generates a random teamcomp", inline=False)
    embed.add_field(name="!clear", value="Clears 100 messages", inline=False)
    await client.say(embed=embed)

@client.command()
async def music(what):
    if what == "tilt":
        await client.say("-play https://www.youtube.com/watch?v=GJDNkVDGM_s")
    if what == "motivation":
        await client.say("-play https://www.youtube.com/watch?v=xSmYAdiXb5M")

client.run(TOKEN)
