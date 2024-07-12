import os
import random 
import json
import requests

import discord
from discord.ext import commands
from discord import app_commands

import configparser
import sys
import settings

logger = settings.logging.getLogger("bot")

intents = discord.Intents.default()
intents.message_content = True
    
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/',intents=intents)

userGender = {}
# todo a mettre dans le fichier de config
#   
pierrick = '773562699102814228'
papa = '789041302556901427' 


class BugReport(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Bug Report")

    name = discord.ui.TextInput(
        label="Bug's command name",
        placeholder="/gbot for example"
    )

    about = discord.ui.TextInput(
        label="Bug's description",
        placeholder="The bug is ...",
        style=discord.TextStyle.long,
        max_length=300,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thanks for your report {interaction.user}", ephemeral=True)
        user = await bot.fetch_user(pierrick)
        await user.send(f"🚨 **Bug report** \n By {interaction.user} \n \n  __Bug's command name__ :  \n  > *{self.name.value}* \n \n   __Bug's description__ : \n > *{self.about.value}* ")
        user = await bot.fetch_user(papa)
        await user.send(f"🚨 **Bug report** \n By {interaction.user} \n \n  __Bug's command name__ :  \n  > *{self.name.value}* \n \n   __Bug's description__ : \n  > *{self.about.value}* ") 


@bot.tree.command(name="report-a-bug", description="Report a bug")
async def Test(interaction: discord.Interaction):
    await interaction.response.send_modal(BugReport()) 




@bot.event
async def on_ready():
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()
    


@bot.tree.command(name="set-gender", description="set the gender for your futur queries")
async def setGender(interaction: discord.Interaction, gender:str):
    userGender[interaction.user] = gender
    await interaction.response.send_message(f'{interaction.user} set gender to {gender}')


@bot.tree.command(name="get_translation", description="Get proteic sequence of a cds in text")
async def getsequencetxt(interaction: discord.Interaction, cds:str):
    "Get proteic sequence of a cds in text"

    if interaction.user in userGender:
        gender = userGender[interaction.user]
    else:
        gender = 'Plant'

    # set the cookie genger
    cookies = {'gender': gender}    

    urlGetCDS = APIURL+'/Feature/feat/CDS/'+ cds
    jsonStr= requests.get(urlGetCDS, cookies=cookies).text
    data = json.loads(jsonStr)
    if data!=None and 'id' in data[0] : 
        urlGetTrans = APIURL+'/Feature/product/'+ str(data[0]['id'])
        seqArray= json.loads(requests.get(urlGetTrans, cookies=cookies).text)
        output = '```>'+cds+'\n'
        for line in seqArray:
            output+=f'{line}\n'
        output+='```'
        await interaction.response.send_message(output)
    else : 
        await interaction.response.send_message('CDS invalide/inexistant !')


if __name__ == '__main__':
    TOKEN = None
    APIURL= None
    try:
        config = configparser.ConfigParser()

        with open("bot.cfg") as f:
            config.read_file(f)

            if 'SERVER' in config:
                TOKEN = config['SERVER']['key']
                APIURL = config['SERVER']['apiURL']
    except IOError as fnf_error:
        print(fnf_error)
        sys.exit(-1)

    # Recuperation des gender pour la suite des requetes
    urlGender = APIURL+'/Gender'
    try:
        genderList = json.loads(requests.get(urlGender).text)
        print(genderList['list'])
    except Exception as e:
        print("Erreur sur les genres")
        print(e)
        sys.exit(-1)


    bot.run(TOKEN, root_logger=True)






# import discord
# from discord.ext import commands
# import requests
# import json
# import configparser
# import sys

# intents = discord.Intents.all() 
# client = discord.Client(intents=intents)
# tree = discord.app_commands.CommandTree(client)

# genderList = None

# @client.event
# async def on_ready():
#     print(f'{client.user} is connected to the following server:\n')
#     for server in client.guilds:
#         print(f'{server.name}(id: {server.id})')
    
#     await tree.sync()
#     await client.change_presence(activity=discord.Game("/gbot"))

# class Link(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#         button = discord.ui.Button(label="Visit gbot website", style=discord.ButtonStyle.url, url = 'http://stat.genopole.cnrs.fr/server/GBOT/index.html')
#         self.add_item(button)

# class Gbot(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#         button = discord.ui.Button(label="Add gbot", style=discord.ButtonStyle.url, url = 'https://discord.com/oauth2/authorize?client_id=1251220532737871883')
#         self.add_item(button)
 




# @tree.command(name="get-sequence-in-json", description="Get proteic sequence of a cds in json")
# async def getsequencejson(interaction: discord.Interaction, cds:str):
#     link = requests.get('http://stat.genopole.cnrs.fr/server/Api/Feature/product/' + cds).text
#     if not str(link) == 'null':
#         data = '```' + link + '```'
#         await interaction.response.send_message(data)
#     else:
#         await interaction.response.send_message('CDS invalide/inexistant !')




# @tree.command(name="gbot", description="Get list of commands")
# async def gbot(interaction: discord.Interaction):
#     await interaction.response.send_message('`/gbot`: Get list of commands \n`/get-sequence-in-txt` : Get proteic sequence of a cds in text \n`/get-sequence-in-json` : Get proteic sequence of a cds in json \n`/get-species` : Get sequence list\n`/website`: Get website link ')
    
# @tree.command(name="get-species", description="Get sequence list")
# async def getspecies(interaction:discord.Interaction):
#     await interaction.response.send_message(requests.get('http://stat.genopole.cnrs.fr/server/Api/Species/').text)

# @tree.command(name="upload-test")
# async def upload(interaction:discord.Interaction, fileuser:discord.Attachment):
#     await interaction.response.send_message(file=discord.File(r'/home/pierrick/Bureau/test.png'))





# @tree.command(name="website", description="Get website link")
# async def website(interaction:discord.Interaction):
#     await interaction.response.send_message(view=Link())

# @tree.command(name="add-gbot", description="Get link to add gbot to your server")
# async def addgbot(interaction:discord.Interaction):
#     await interaction.response.send_message(view=Gbot())





# if __name__ == '__main__':
#     key = None
#     try:
#         config = configparser.ConfigParser()

#         with open("bot.cfg") as f:
#             config.read_file(f)

#             if 'SERVER' in config:
#                 key = config['SERVER']['key']
            
#     except IOError as fnf_error:
#         print(fnf_error)
#         sys.exit(-1)

#     # Recuperation des gender pour la suite des requetes
#     url = 'http://stat.genopole.cnrs.fr/server/Api/Gender'
#     try:
#         genderList = json.loads(requests.get(url).text)
#         print(genderList['list'])
#     except :
#         print("Erreur sur les genres")
#         sys.exit(-1)


#     client.run(key)
