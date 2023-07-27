# bot.py
import os
import urllib.parse
import discord
import requests
from urllib.parse import urlencode
from urllib.parse import urljoin
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.command(name='random_info')
async def generate_info(ctx):
    response = requests.get("https://randomuser.me/api/")
    await ctx.send(response.text)


@bot.command(name='card_info')
async def get_card_info(ctx, card_names):
    query_params = {"name": card_names}
    info_endpoint = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    art_endpoint = "https://storage.googleapis.com/ygoprodeck.com/pics/"
    database_endpoint = "https://db.ygoprodeck.com/card/?{}"
    response = requests.get(info_endpoint, params=query_params).json()
    card_information = response["data"]
    for x in range(0, len(card_information)):
        card_name = card_information[len(card_information)-x-1]["name"]
        #card_type = card_information[len(card_information)-x-1]["type"]
        #card_race = card_information[len(card_information)-x-1]["race"]
        search_args = {"search":  card_name}
        card_link = database_endpoint.format(urllib.parse.urlencode(search_args))
        embed = discord.Embed(title=card_name, url=card_link,
                              description=card_information[len(card_information)-x-1]["desc"], color=0xFF5733)
        card_id = card_information[len(card_information)-x-1]["id"]
        embed.set_thumbnail(url=urljoin(art_endpoint, str(card_id) + '.jpg'))
        await ctx.send(embed=embed)


@bot.command(name='random_card')
async def get_random_card(ctx):
    random_card_endpoint = "https://db.ygoprodeck.com/api/v7/randomcard.php"
    response = requests.get(random_card_endpoint).json()
    card_information = response
    card_name = card_information["name"]
    database_endpoint = "https://db.ygoprodeck.com/card/?{}"
    art_endpoint = "https://storage.googleapis.com/ygoprodeck.com/pics/"
    search_args = {"search": card_name}
    card_link = database_endpoint.format(urllib.parse.urlencode(search_args))
    embed = discord.Embed(title=card_name, url=card_link,
                          description=card_information["desc"], color=0xFF5733)
    card_id = card_information["id"]
    embed.set_thumbnail(url=urljoin(art_endpoint, str(card_id) + '.jpg'))
    await ctx.send(embed=embed)

#@bot.command(name='card_picture')
#async def get_card_picture(ctx):
    #response = requests.get("https://storage.googleapis.com/ygoprodeck.com/pics/22398665.jpg")
    #file = open("22398665.jpg", "wb")
    #file.write(response.content)
    #file.close()


bot.run(TOKEN)
