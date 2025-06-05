import discord
from discord.ext import commands
import asyncio

from gbotCommands import key, intents





# def getSpeciesListAsJson(interaction: discord.Interaction) -> list:
#     ''' fonction de recuperation de la liste 
#         des especes pour un genre donné
#         @param interaction : objet de discord

#         @return : la liste des especes.
#     '''
#     gender = checkgender(interaction.user)
#     # Definition du genre
#     cookies = {'gender': gender}    

#     # Appel de l'url de connection a GBOT pour 
#     # avoir les species cf bot.cfg
#     jsonStr= requests.get(species, cookies=cookies).text
#     # Recuperation de la liste json et transformation 
#     # en list python
#     speciesList = json.loads(jsonStr)
#     return speciesList



# @tree.command(name="get-species", description="Get species list for current gender")
# async def getspecies(interaction: discord.Interaction):
#     '''
#     fonction de recuperation de la liste des especes
#     dans la base de donnees et l'affiche sur l'interface discord

#     @param interaction : objet de discord
#     '''
#     # Recuperation du genre
#     gender = checkgender(interaction.user)

#     # Recuperation de la liste a partir du json
#     speciesList = getSpeciesListAsJson(interaction)
    
#     if speciesList!=None and 'id' in speciesList[0] : 
#         # Creation du message de retour
#         output = f'{interaction.user} connected on {gender}\n```'
#         for d in speciesList:
#             output += d['name']+'\n'
#         output+= '```'
#         await interaction.response.send_message(output)
#     else : 
#         await interaction.response.send_message('Species invalide/inexistant !')




# async def species_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
#     ''' 
#     autocompletion de l'espece a partir de la liste dans la base de donnees
#     @param interaction : objet de discord
#     @param current : espece en cours

#     @return retourne la liste des especes selectionnables
#     '''
#     speciesList = getSpeciesListAsJson(interaction)
#     return [ app_commands.Choice(name=spe['name'], value=str(spe['id'])+'|'+str(spe['name'])) for spe in speciesList if current.lower() in spe['name'].lower() ]



# @tree.command(name="get-sequences", description="Get sequence list for a species")
# @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
# @app_commands.autocomplete(species=species_autocomplete)
# async def getsequences(interaction: discord.Interaction, species: str):
#     '''
#     Fontion de recuperation de la liste des sequences
#     pour une espece choisi en parametre, l'affichage se fait dans
#     l'interface discord
    
#     @param_discord : species (autocompletion)
#     @param interaction : objet de discord
#     @param species: species choisi par l'utilisateur
    
#     '''
#     # Recuperation du genre
#     gender = checkgender(interaction.user)
    
#     # Initialisation du cookies utilisé par GBOT
#     cookies = {'gender': gender} 

#     # Recuperation de l'espece venanat de l'autocompletion
#     (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
#     # Appel de l'url de connection a GBOT pour 
#     # avoir les Sequences cf bot.cfg : url_api/Chromosome  
#     # on passe les cookies pour avoir le genre
#     jsonStr= requests.get(api+'/Chromosome/'+speciesId, cookies=cookies).text
#     sequencesList = json.loads(jsonStr)
#     # Mise en page pour discord
#     if sequencesList!=None and 'id' in sequencesList[0] : 
#         # Creation de la sortie.
#         output = f'{interaction.user} connected on {gender}\n```'
#         for d in sequencesList:
#             output += d['name']+'\t'+str(d['length'])+"bp\n"
#         output+= '```'
#         await interaction.response.send_message(output)
#     else : 
#         await interaction.response.send_message('Species invalide/inexistant !')







# @tree.command(name="blast", description="Blast your sequence on GBOT species")
# @app_commands.describe(fileuser="Upload your sequence file to blast")
# @app_commands.describe(program="Choose your blast tool")
# @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
# @app_commands.autocomplete(species=species_autocomplete)
# async def blast(interaction:discord.Interaction, 
#                  fileuser:discord.Attachment,
#                  program: Literal['blastp', 'blastn', 'blastx', 'tblastn'],
#                  species:str
#                  ):
#     '''
#     Fonction d'execution de la commande blast(n,p,x,t..n) 
#     sur une sequence venant d'un upload.
#     sur une espece choisi en autocompletion
#     @param interaction : objet de discord
#     @param fileuser : fichier a blaster
#     @param program : programme a utilise choisi dans une liste
#     @species species (autocompletion)
#     '''
#     # Recuperation de l'espece venanat de l'autocompletion   
#     (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
#     # creation si necessaire du repertoire de sortie
#     if not os.path.isdir('user'):
#         os.makedirs('user')
#     # Sauvegarde du fichier de l'utilisateur dans le repertoire
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
#     # Preparation des parametres pour la commande
#     # post du blast sur GBOT
#     headers = {'content-type': 'application/json'}
#     parameter = {'program': program, 
#                  'evalue': '1e-5',
#                  'wordsize': 4,
#                  'txt': 1,
#                  'sequence': sequence,
#                  'speciesId': speciesId,
#                  'speciesName' : speciesName,
#                  'inter' : 'false',
#                  'gender': 'Plant'
#                  }
#     print(parameter)
#     # Mettre en attente discord
#     await interaction.response.defer()
#     # Appel de l'url de connection a GBOT pour 
#     # avoir les Blast cf bot.cfg : url_api/server/Blast  
#     # on passe les cookies pour avoir le genre
#     # on passe les parametres sous forme de str json en mode post
#     response = requests.post(api+"/server"+"/Blast/",data=json.dumps(parameter),headers = headers, cookies=cookies)
    
#     # Recuperation du fichier de resultat
#     with open(os.path.join('user', fileuser.filename+"_result"), "wb") as file:
#         file.write(response.content)
#     file.close()

#     entityFileName = fileuser.filename+"_result"

#     # Send embed notifying start of the spam stream
#     detailsEmbed = discord.Embed(
#         colour=discord.Colour.red(),
#         title=f"See `{entityFileName}` for your blast result",
#         description="Due to discord character limits regarding embeds, the results have to be sent in a file"
#     )
#     await interaction.followup.send(embed=detailsEmbed, file=discord.File(os.path.join('user', fileuser.filename+"_result")))



# async def sequence_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
#     ''' 
#         autocompletion double : species puis sequence de l'espece
#         @param interaction : objet de discord
#         @param current : sequence en cours

#         @return retourne la liste des sequences selectionnables
#     '''
#     # recuperation du parametre necessaire pour fonctionner ici
#     # l'espece! qui est passe dans l'objet discord
#     species = interaction.namespace.species
#     # On recupere le Id
#     (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion

#     # recuperation du genre
#     gender = checkgender(interaction.user)
#     cookies = {'gender': gender} 

#     # Appel de l'url de connection a GBOT pour 
#     # avoir les Sequences cf bot.cfg : url_api/Chromosome/speciesId  
#     # on passe les cookies pour avoir le genre
#     jsonStr= requests.get(api+'/Chromosome/'+speciesId, cookies=cookies).text
#     data = json.loads(jsonStr)
#     return [ app_commands.Choice(name=seq['accession'], value=str(seq['id'])+'|'+str(seq['accession'])) for seq in data if current.lower() in seq['accession'].lower() ]




# # ''' 
# #      autocompletion triple : species puis sequence de l'espece, puis feature a afficher
# # '''
# # async def featureList_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
# #     speciesList = getSpeciesListAsJson(interaction)
# #     print(interaction.namespace.species)
# #     species = interaction.namespace.species
# #     if species == "":
# #         return [ app_commands.Choice(name=spe['name'], value=str(spe['id'])+'|'+str(spe['name'])) for spe in speciesList if current.lower() in spe['name'].lower() ]
# #     else: 
# #         gender = checkgender(interaction.user)
# #         cookies = {'gender': gender} 

# #         (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
# #         jsonStr= requests.get(api+'/Chromosome/'+speciesId, cookies=cookies).text
# #         data = json.loads(jsonStr)
# #         return [ app_commands.Choice(name=seq['accession'], value=str(seq['id'])+'|'+str(seq['accession'])) for seq in data if current.lower() in seq['accession'].lower() ]
        

# class FeatureSelect(discord.ui.Select):
#     def __init__(self, interaction, species, sequence, start, stop, shownames):
       

#         self.species = species
#         self.sequence = sequence
#         self.start = start
#         self.stop = stop
#         self.shownames = shownames

#         # Recuperation du genre
#         gender = checkgender(interaction.user)

#         # Initialisation du cookies utilisé par GBOT
#         cookies = {'gender': gender} 

#         (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
#         jsonStr= requests.get(api+'/Species/FeatureTypesFor/'+speciesId, cookies=cookies).text
#         featureTypes =  json.loads(jsonStr)
#         featureTypeList = featureTypes ['type']
#         featureViewList = featureTypes ['view']


#         options = []
#         for idx in range(len(featureTypeList)):
#             d = discord.SelectOption(label=featureViewList[idx], value=featureTypeList[idx])
#             options.append(d)

      

#         super().__init__(
#             placeholder="Features to show",
#             min_values=1,
#             max_values=len(options),
#             options=options
#         )

#     async def callback(self, interaction: discord.Interaction):
#         feature_selected = self.values
        

#         species =self.species  
#         sequence =self.sequence  
#         start =self.start  
#         stop =self.stop  


#         # Recuperation du genre
#         gender = checkgender(interaction.user)

#         # Initialisation du cookies utilisé par GBOT
#         cookies = {'gender': gender} 

    
#         # Call discord to wait 
#         await interaction.response.defer()


#         # Recuperation des parametres venant de l'autocompletion    
#         (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
#         (sequenceId, sequenceName) = sequence.split('|') # regarder la value de l'autocompletion

#         # Utilisation de la librairie permettant de simuler un navigateur web
#         from selenium import webdriver
#         from selenium.webdriver.chrome.service import Service

#         from selenium.webdriver.support.ui import WebDriverWait

#         # backup de l'image et envoie de celle ci
#         if not os.path.isdir('user'):
#             os.makedirs('user')

        
#         service = Service()
#         options = webdriver.ChromeOptions()
#         options.add_argument("--headless=new")
#         #options.add_argument('user-data-dir='+os.path.join(os.getcwd(),'user'))

#         driver = webdriver.Chrome(service=service, options=options)
#         driver.set_window_size(1000, 250) 

#         # Appel de l'url correspondante pour generer l'image
#         driver.get(gbot_url+"/graphsequence.html?uid="+gender+
#             "&species="+speciesId+
#             "&sequence="+sequenceId+
#             "&start="+str(start)+
#             "&stop="+str(stop)+
#             "&features="+','.join(feature_selected)+
#             "&names="+str(self.shownames))
#         print(gbot_url+"/graphsequence.html?uid="+gender+
#             "&species="+speciesId+
#             "&sequence="+sequenceId+
#             "&start="+str(start)+
#             "&stop="+str(stop)+
#             "&features="+','.join(feature_selected)+
#             "&names="+str(self.shownames))
#         html_page = driver.page_source
        
#         # Creation du screenshoot
#         #print(os.path.join(os.getcwd(),'user','screenshot.png'))
#         driver.save_screenshot(os.path.join('user','screenshot.png'))

#         await interaction.followup.send(file=discord.File(os.path.join('user','screenshot.png')))


# class FeatureView(discord.ui.View):
#     def __init__(self,  interaction, species, sequence, start, stop, shownames):
#         super().__init__(timeout=60)

#         self.add_item(FeatureSelect(interaction, species, sequence, start, stop, shownames))

# '''
#     Fonction d'affichage d'un graph a partir d'un bout de sequence 
#     de la base de donnees
#     parametre : species espece,
#                 sequence (autocompletion comme espece)
#                 start position de debut
#                 stop position de fin
# '''
# @tree.command(name="graph-sequence", description="Get a picture of a region of sequence in GBOT")
# @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
# @app_commands.describe(sequence="select a sequence from the list available for your species")
# @app_commands.describe(start="the start position")
# @app_commands.describe(stop="the stop position")
# @app_commands.describe(shownames="True pour activer, False pour désactiver")
# @app_commands.autocomplete(species=species_autocomplete, sequence=sequence_autocomplete)
# async def graphsequence(interaction:discord.Interaction, 
#                     species:str,
#                     sequence:str,
#                     start: int,
#                     stop: int,
#                     shownames: bool
#                  ):

                
#     await interaction.response.send_message(
#         content="Select feature to draw in the list below :",
#         view=FeatureView(interaction, species, sequence, start, stop, shownames),
#         ephemeral=True
#     )

    




# '''
#     Fonction de recuperation d'un svg a partir d'un bout de sequence 
#     de la base de donnees
#     parametre : species espece,
#                 sequence (autocompletion comme espece)
#                 start position de debut
#                 stop position de fin
# '''
# @tree.command(name="graph-sequence-svg",  description="Get a picture in SVG format of a region of sequence in GBOT")
# @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
# @app_commands.describe(sequence="select a sequence from the list available for your species")
# @app_commands.describe(start="the start position")
# @app_commands.describe(stop="the stop position")
# @app_commands.autocomplete(species=species_autocomplete, sequence=sequence_autocomplete)
# async def graphsequenceassvg(interaction:discord.Interaction, 
#                     species:str,
#                     sequence:str,
#                     start: int,
#                     stop: int
#                  ):

    
#     # Recuperation du genre
#     gender = checkgender(interaction.user)

#     # Initialisation du cookies utilisé par GBOT
#     cookies = {'gender': gender} 

    

#     # Call discord to wait 
#     await interaction.response.defer()

#     # Recuperation des parametres venant de l'autocompletion    
#     (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
#     (sequenceId, sequenceName) = sequence.split('|') # regarder la value de l'autocompletion

#     # Utilisation de la librairie permettant de simuler un navigateur web
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By

#     from selenium.webdriver.chrome.service import Service

#     from selenium.webdriver.support.ui import WebDriverWait
#     service = Service()
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless=new")
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.set_window_size(1000, 250) 

    
#     # Appel de l'url correspondante pour generer l'image
#     url = gbot_url+"/graphsequence.html?uid="+gender+\
#         "&species="+speciesId+\
#         "&sequence="+sequenceId+\
#         "&start="+str(start)+\
#         "&stop="+str(stop)
#     driver.get(url)
#     html_page = driver.page_source
#     import re
#     exp = re.search('<svg.+?(</svg>)',html_page)
#     svg = exp.group(0)
    
#      # backup de l'image et envoie de celle ci
#     if not os.path.isdir('user'):
#         os.makedirs('user')

#     with open('html_style_for_svg_graph.html', 'r') as style:
#         style = style.read()

#     svg = svg.replace("><", ">\n"+style+"<",1)

#     svg = svg.replace("currentColor", "black")

#      # Recuperation du fichier de resultat
#     with open(os.path.join('user', "result.svg"), "w") as file:
#         file.write(str(svg))
#     file.close()
#     # et les include dans le svg apres la balise svg.
#     entityFileName = "result.svg"

#     # Send embed notifying start of the spam stream
#     detailsEmbed = discord.Embed(
#         colour=discord.Colour.red(),
#         title=f"See `{entityFileName}` for your svg result",
#         description="Due to discord character limits regarding embeds, the results have to be sent in a file"
#     )
#     await interaction.followup.send(embed=detailsEmbed, file=discord.File(os.path.join('user', "result.svg")))




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