import discord
import discord.ext
import requests
import json
import configparser
import sys

intents = discord.Intents.all() 
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

class Link(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Visit gbot website", style=discord.ButtonStyle.url, url = 'http://stat.genopole.cnrs.fr/server/GBOT/index.html')
        self.add_item(button)

class Gbot(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Add gbot", style=discord.ButtonStyle.url, url = 'https://discord.com/oauth2/authorize?client_id=1251220532737871883')
        self.add_item(button)
     

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Game("/gbot"))

@tree.command(name="get-sequence-in-txt", description="Get proteic sequence of a cds in text")
async def getsequencetxt(interaction: discord.Interaction, cds:str):
    data = ""
    try:
        for i in json.loads(requests.get('http://stat.genopole.cnrs.fr/server/Api/Feature/product/' + cds).text):
            data = data + i + '\n'
        await interaction.response.send_message(data)
    except:
        await interaction.response.send_message('CDS invalide/inexistant !')

@tree.command(name="get-sequence-in-json", description="Get proteic sequence of a cds in json")
async def getsequencejson(interaction: discord.Interaction, cds:str):
    link = requests.get('http://stat.genopole.cnrs.fr/server/Api/Feature/product/' + cds).text
    if not str(link) == 'null':
        data = '```' + link + '```'
        await interaction.response.send_message(data)
    else:
        await interaction.response.send_message('CDS invalide/inexistant !')
    
@tree.command(name="gbot", description="Get list of commands")
async def gbot(interaction: discord.Interaction):
    await interaction.response.send_message('`/gbot`: Get list of commands \n`/get-sequence-in-txt` : Get proteic sequence of a cds in text \n`/get-sequence-in-json` : Get proteic sequence of a cds in json \n`/get-species` : Get sequence list\n`/website`: Get website link ')
    
@tree.command(name="get-species", description="Get sequence list")
async def getspecies(interaction:discord.Interaction):
    await interaction.response.send_message(requests.get('http://stat.genopole.cnrs.fr/server/Api/Species/').text)

@tree.command(name="upload-test")
async def upload(interaction:discord.Interaction, fileuser:discord.Attachment):
    await interaction.response.send_message(file=discord.File(r'/home/pierrick/Bureau/test.png'))

@tree.command(name="website", description="Get website link")
async def website(interaction:discord.Interaction):
    await interaction.response.send_message(view=Link())

@tree.command(name="add-gbot", description="Get link to add gbot to your server")
async def addgbot(interaction:discord.Interaction):
    await interaction.response.send_message(view=Gbot())

if __name__ == '__main__':
    key = None
    try:
        config = configparser.ConfigParser()

        with open("bot.cfg") as f:
            config.read_file(f)

            if 'SERVER' in config:
                key = config['SERVER']['key']
            
    except IOError as fnf_error:
        print(fnf_error)
        sys.exit(-1)

    client.run(key)
