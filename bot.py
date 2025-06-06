import discord
from discord.ext import commands
import asyncio

from gbotCommands import key, intents








# '''
#     Graph votre propre sequence uploade en parametre 
#     parametre : fileuser genbank a visualiser
#                 start position de debut
#                 stop position de fin 
# '''

# @tree.command(name="graph-your-sequence", description="Get a picture your sequence in genbank file format")
# @app_commands.describe(fileuser="Upload your sequence to draw")
# @app_commands.describe(start="the start position")
# @app_commands.describe(stop="the stop position")
# async def graphit(interaction:discord.Interaction, 
#                  fileuser:discord.Attachment,
#                  start: Optional[int] = 0,
#                  stop: Optional[int] = -1
#                  ):
#     # Get File on server
#     if not os.path.isdir('user'):
#         os.makedirs('user')
#     # Sauvegarde du fichier utilisateur
#     await fileuser.save(os.path.join('user',fileuser.filename))
#     sequence = ""
#     file = open(os.path.join('user', fileuser.filename))
#     file.readline()
#     for line in file:
#         line = line.rstrip()
#         sequence+=line
#     file.close()

#     # Recuperation du genre
#     gender = checkgender(interaction.user)
        
#     # Initialisation du cookies utilisé par GBOT
#     cookies = {'gender': gender} 
#     # uid a 0 pour dire que c'est un nouvel update
#     parameter = { 'uid' : 0 }
#     # Call discord to wait 
#     await interaction.response.defer()

#     # Creation de la base de donnees temporaire pour acceuillir le fichier
#     # de l'utilisateur
#     files = {'dataFile': open(os.path.join('user', fileuser.filename), 'rb')}

#     response = requests.post(gbot_url+"/Api/server/uploadForBot/",
#         cookies=cookies,
#         files=files)
    
#     retour = json.loads(response.text)


#     if retour['status'] != 1 :
#         await interaction.followup.send("Problem with your sequence")

#     uid = retour['uid']

#     # Utilisation de la librairie permettant de simuler un navigateur web
#     from selenium import webdriver
#     from selenium.webdriver.chrome.service import Service

#     from selenium.webdriver.support.ui import WebDriverWait
#     service = Service()
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless=new")
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.set_window_size(1000, 250) 

#     # Demande de visualisation de la nouvelle sequence
#     driver.get(gbot_url+"/graphsequence.html?uid="+uid+"&start="+str(start)+"&stop="+str(stop))
#     html_page = driver.page_source
#     # Sauvegarde du screenshoot
#     driver.save_screenshot(os.path.join('user','screenshot.png'))
#     # envoi de l'image
#     await interaction.followup.send(file=discord.File(os.path.join('user','screenshot.png')))
    
#     # Effacer le contenu de la base de donnee. 
#     headers = {'content-type': 'application/json'}

#     response = requests.post(gbot_url+"/Api/server/cleanBot/",
#         data=json.dumps({'uid': uid }) ,headers = headers, cookies=cookies
#        )






# @tree.command(name="help",  description="Show the list of gbot-bot command")
# async def help_command(interaction: discord.Interaction):
#     embed = discord.Embed(title="📘 Available commands", color=discord.Color.blue())
#     for command in tree.walk_commands():
#         embed.add_field(name=f"/{command.name}", value=command.description or "no description", inline=False)

#     await interaction.response.send_message(embed=embed)

# if __name__ == '__main__':
#     bot.load_extension("commandes.test")
#     client.run(key, root_logger=True)

#intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_command_error(ctx, error):
    print(f"Erreur dans la commande {ctx.command}: {error}")@bot.event

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} ({bot.user.id})")
    await bot.tree.sync()  # Important : synchronise les slash commands
    print("Commandes slash synchronisées")

async def main():
    async with bot:
        await bot.load_extension("gbotCommands.gbot")
        await bot.load_extension("gbotCommands.gbot.blast")
        await bot.load_extension("gbotCommands.gbot.graph")
        await bot.load_extension("gbotCommands.gbot.PFAM")

        await bot.load_extension("gbotCommands.base")
        await bot.start(key)

asyncio.run(main())