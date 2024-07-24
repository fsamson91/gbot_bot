import discord
import discord.ext
import requests
import json
import configparser
import sys

from discord import app_commands
from typing import Literal
from typing import List

userGender = {}

def checkgender(user):
    if user in userGender:
        return userGender[user]
    else:
        return 'Plant'


intents = discord.Intents.all() 
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


key = None
pierrick = None
papa = None
sequence = None
specices = None
web = None
add = None
urlGender = None
gettrans = None

try:
    config = configparser.ConfigParser()
    with open("bot.cfg") as f:
        config.read_file(f)

        if 'CONFIG' in config:
            key = config['CONFIG']['key']
            pierrick = config['CONFIG']['pierrick']
            papa = config['CONFIG']['papa']
            api = config['CONFIG']['api']
            sequence = config['CONFIG']['sequence']
            species = config['CONFIG']['species']
            web = config['CONFIG']['web']
            add = config['CONFIG']['add']
            urlGender = config['CONFIG']['gender']
            gettrans = config['CONFIG']['gettrans']


except IOError as fnf_error:
    print(fnf_error)
    sys.exit(-1)



class BugReportModal(discord.ui.Modal):
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
        user = await client.fetch_user(pierrick)
        await user.send(f"🚨 **Bug report** \n By {interaction.user} \n \n  __Bug's command name__ :  \n  > *{self.name.value}* \n \n   __Bug's description__ : \n > *{self.about.value}* ")
        user = await client.fetch_user(papa)
        await user.send(f"🚨 **Bug report** \n By {interaction.user} \n \n  __Bug's command name__ :  \n  > *{self.name.value}* \n \n   __Bug's description__ : \n  > *{self.about.value}* ")
    


class Link(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Visit gbot website", style=discord.ButtonStyle.url, url = web )
        self.add_item(button)

class Gbot(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Add gbot", style=discord.ButtonStyle.url, url = add )
        self.add_item(button)
     

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game("/gbot"))
    
@tree.command(name="gbot", description="Get list of commands")
async def gbot(interaction: discord.Interaction):
    await interaction.response.send_message('`/gbot`: Get list of commands \n`/set-gender` :  \n`/get-translation` : Get proteic sequence of a cds \n`/get-species` : Get sequence list\n`/website`: Get website link ')
 
@tree.command(name="website", description="Get website link")
async def website(interaction:discord.Interaction):
    await interaction.response.send_message(view=Link())

@tree.command(name="add-gbot", description="Get link to add gbot to your server")
async def addgbot(interaction:discord.Interaction):
    await interaction.response.send_message(view=Gbot())

@tree.command(name="report-a-bug", description="Report a bug")
async def Test(interaction: discord.Interaction):
    await interaction.response.send_modal(BugReportModal())


async def gender_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    data = json.loads(requests.get(urlGender).text)
    genderList = [ d['gendername'] for d in data['list'] ]
    return [ app_commands.Choice(name=gender, value=gender) for gender in genderList if current.lower() in gender.lower() ]

@tree.command(name="set-gender", description="set the gender for your futur queries")
@app_commands.autocomplete(gender=gender_autocomplete)
async def setGender(interaction:discord.Interaction, gender: str):
    userGender[interaction.user] = gender
    await interaction.response.send_message(f'{interaction.user} set gender to {gender}')

@tree.command(name="get-translation", description="Get proteic sequence of a cds")
async def getsequencetxt(interaction: discord.Interaction, cds:str):
    gender = checkgender(interaction.user)
   
    cookies = {'gender': gender}    

    urlGetCDS = gettrans + cds
    jsonStr= requests.get(urlGetCDS, cookies=cookies).text
    data = json.loads(jsonStr)
    if data!=None and 'id' in data[0] : 
        urlGetTrans = sequence + str(data[0]['id'])
        seqArray= json.loads(requests.get(urlGetTrans, cookies=cookies).text)
        output = f'{interaction.user} connected on {gender}\n```>{cds}\n'
        for line in seqArray:
            output+=f'{line}\n'
        output+='```'
        await interaction.response.send_message(output)
    else : 
        await interaction.response.send_message('CDS invalide/inexistant !')


def getSpeciesListAsJson(interaction: discord.Interaction) -> str:
    gender = checkgender(interaction.user)
   
    cookies = {'gender': gender}    

    jsonStr= requests.get(species, cookies=cookies).text
    data = json.loads(jsonStr)
    return data


@tree.command(name="get-species", description="Get species list for current gender")
async def getspecies(interaction: discord.Interaction):
    data = getSpeciesListAsJson()
    if data!=None and 'id' in data[0] : 
        output = f'{interaction.user} connected on {gender}\n```'
        for d in data:
            output += d['name']+'\n'
        output+= '```'
        await interaction.response.send_message(output)
    else : 
        await interaction.response.send_message('Species invalide/inexistant !')


async def species_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    data = getSpeciesListAsJson(interaction)
    return [ app_commands.Choice(name=spe['name'], value=str(spe['id'])+'|'+str(spe['name'])) for spe in data if current.lower() in spe['name'].lower() ]

@tree.command(name="get-sequences", description="Get sequence list for a species")
@app_commands.autocomplete(species=species_autocomplete)
async def getsequences(interaction: discord.Interaction, species: str):
    gender = checkgender(interaction.user)
   
    cookies = {'gender': gender} 

    (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
    jsonStr= requests.get(api+'/Chromosome/'+speciesId, cookies=cookies).text
    data = json.loads(jsonStr)
    if data!=None and 'id' in data[0] : 
        output = f'{interaction.user} connected on {gender}\n```'
        for d in data:
            output += d['name']+'\t'+str(d['length'])+"bp\n"
        output+= '```'
        await interaction.response.send_message(output)
    else : 
        await interaction.response.send_message('Species invalide/inexistant !')

   # await interaction.response.send_message(f'{speciesName} probleme !')


'''
@tree.command(name="upload-test")
async def upload(interaction:discord.Interaction, fileuser:discord.Attachment):
    await interaction.response.send_message(file=discord.File(r'/home/pierrick/Bureau/test.png'))
'''

if __name__ == '__main__':
    client.run(key, root_logger=True)
