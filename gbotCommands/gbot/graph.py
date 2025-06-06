import os
import discord     # On import Discord c'est bien normal
import json        # json pour les echanges avec la base de donnees
import requests    # request pour passer des urls

from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional
from gbotCommands.gbot import sequence_autocomplete, species_autocomplete, checkgender
from gbotCommands import api, gbot_url, mycommand


class FeatureSelect(discord.ui.Select):
    def __init__(self, interaction, species, sequence, start, stop, shownames, svg):
        self.species = species
        self.sequence = sequence
        self.start = start
        self.stop = stop
        self.shownames = shownames
        self.svg = svg

        # Recuperation du genre
        gender = checkgender(interaction.user)

        # Initialisation du cookies utilisé par GBOT
        cookies = {'gender': gender} 

        (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
        jsonStr= requests.get(api+'/Species/FeatureTypesFor/'+speciesId, cookies=cookies).text
        featureTypes =  json.loads(jsonStr)
        featureTypeList = featureTypes ['type']
        featureViewList = featureTypes ['view']


        options = []
        for idx in range(len(featureTypeList)):
            d = discord.SelectOption(label=featureViewList[idx], value=featureTypeList[idx])
            options.append(d)

      

        super().__init__(
            placeholder="Features to show",
            min_values=1,
            max_values=len(options),
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        feature_selected = self.values
        species =self.species  
        sequence =self.sequence  
        start =self.start  
        stop =self.stop  

        # Recuperation du genre
        gender = checkgender(interaction.user)

        # Initialisation du cookies utilisé par GBOT
        cookies = {'gender': gender} 

        # Call discord to wait 
        await interaction.response.defer()

        # Recuperation des parametres venant de l'autocompletion    
        (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
        (sequenceId, sequenceName) = sequence.split('|') # regarder la value de l'autocompletion

        # Utilisation de la librairie permettant de simuler un navigateur web
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service

        from selenium.webdriver.support.ui import WebDriverWait

        # backup de l'image et envoie de celle ci
        if not os.path.isdir('user'):
            os.makedirs('user')

        
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        #options.add_argument('user-data-dir='+os.path.join(os.getcwd(),'user'))

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1000, 250) 

        # Appel de l'url correspondante pour generer l'image
        driver.get(gbot_url+"/graphsequence.html?uid="+gender+
            "&species="+speciesId+
            "&sequence="+sequenceId+
            "&start="+str(start)+
            "&stop="+str(stop)+
            "&features="+','.join(feature_selected)+
            "&names="+str(self.shownames))
        print(gbot_url+"/graphsequence.html?uid="+gender+
            "&species="+speciesId+
            "&sequence="+sequenceId+
            "&start="+str(start)+
            "&stop="+str(stop)+
            "&features="+','.join(feature_selected)+
            "&names="+str(self.shownames))
        html_page = driver.page_source
        

        if self.svg:
            import re
            exp = re.search(r'<svg.+?(</svg>)',html_page)
            svg = exp.group(0)
        
            # backup de l'image et envoie de celle ci
            if not os.path.isdir('user'):
                os.makedirs('user')

            with open(os.path.join(os.path.dirname(__file__),'html_style_for_svg_graph.html'), 'r') as style:
                style = style.read()
            

            svg = svg.replace("><", ">\n"+style+"<",1)

            svg = svg.replace("currentColor", "black")

            # Recuperation du fichier de resultat
            with open(os.path.join('user', "result.svg"), "w") as file:
                file.write(str(svg))
            file.close()
            # et les include dans le svg apres la balise svg.
            entityFileName = "result.svg"

            # Send embed notifying start of the spam stream
            detailsEmbed = discord.Embed(
                colour=discord.Colour.red(),
                title=f"See `{entityFileName}` for your svg result",
                description="Due to discord character limits regarding embeds, the results have to be sent in a file"
            )
            await interaction.followup.send(embed=detailsEmbed, file=discord.File(os.path.join('user', "result.svg")))

        else :
            # Creation du screenshoot
            #print(os.path.join(os.getcwd(),'user','screenshot.png'))
            driver.save_screenshot(os.path.join('user','screenshot.png'))

            await interaction.followup.send(file=discord.File(os.path.join('user','screenshot.png')))


class FeatureView(discord.ui.View):
    def __init__(self,  interaction, species, sequence, start, stop, shownames, svg=False):
        super().__init__(timeout=60)

        self.add_item(FeatureSelect(interaction, species, sequence, start, stop, shownames, svg))




class GBOTGraphCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @mycommand(name="graph-sequence", description="Get a picture of a region of sequence in GBOT", position='40')
    @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
    @app_commands.describe(sequence="select a sequence from the list available for your species")
    @app_commands.describe(start="the start position")
    @app_commands.describe(stop="the stop position")
    @app_commands.describe(shownames="True pour activer, False pour désactiver")
    @app_commands.autocomplete(species=species_autocomplete, sequence=sequence_autocomplete)
    async def graphsequence(self, interaction:discord.Interaction, 
                        species:str,
                        sequence:str,
                        start: int,
                        stop: int,
                        shownames: bool
                    ):
        '''
            Fonction d'affichage d'un graph a partir d'un bout de sequence 
            de la base de donnees
            @param species : autocompletion espece,
            @param sequence : autocompletion comme espece
            @param start position de debut
            @param stop position de fin
        '''
                    
        await interaction.response.send_message(
            content="Select feature to draw in the list below :",
            view=FeatureView(interaction, species, sequence, start, stop, shownames),
            ephemeral=True
        )

    @mycommand(name="graph-sequence-svg", description="Get a svg file of a region of sequence in GBOT", position='41')
    @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
    @app_commands.describe(sequence="select a sequence from the list available for your species")
    @app_commands.describe(start="the start position")
    @app_commands.describe(stop="the stop position")
    @app_commands.describe(shownames="True pour activer, False pour désactiver")
    @app_commands.autocomplete(species=species_autocomplete, sequence=sequence_autocomplete)
    async def graphsequenceassvg(self, interaction:discord.Interaction, 
                        species:str,
                        sequence:str,
                        start: int,
                        stop: int,
                        shownames: bool
                    ):
        '''
            Fonction d'affichage d'un graph a partir d'un bout de sequence 
            de la base de donnees
            @param species : autocompletion espece,
            @param sequence : autocompletion comme espece
            @param start position de debut
            @param stop position de fin
        '''
                    
        await interaction.response.send_message(
            content="Select feature to draw in the list below :",
            view=FeatureView(interaction, species, sequence, start, stop, shownames, True),
            ephemeral=True
        )

    '''
        Graph votre propre sequence uploade en parametre 
        parametre : fileuser genbank a visualiser
                    start position de debut
                    stop position de fin 
    '''
    @mycommand(name="graph-your-sequence", description="Get a picture of your sequence uploaded", position='42')
    @app_commands.describe(fileuser="Upload your sequence to draw")
    @app_commands.describe(start="the start position")
    @app_commands.describe(stop="the stop position")
    async def graphit(self,
                    interaction:discord.Interaction, 
                    fileuser:discord.Attachment,
                    start: Optional[int] = 0,
                    stop: Optional[int] = -1
                    ):
        # Get File on server
        if not os.path.isdir('user'):
            os.makedirs('user')
        # Sauvegarde du fichier utilisateur
        await fileuser.save(os.path.join('user',str(interaction.user), fileuser.filename))
        sequence = ""
        file = open(os.path.join('user',str(interaction.user), fileuser.filename))
        file.readline()
        for line in file:
            line = line.rstrip()
            sequence+=line
        file.close()

        # Recuperation du genre
        gender = checkgender(interaction.user)
            
        # Initialisation du cookies utilisé par GBOT
        cookies = {'gender': gender} 
        # uid a 0 pour dire que c'est un nouvel update
        parameter = { 'uid' : 0 }
        # Call discord to wait 
        await interaction.response.defer()

        # Creation de la base de donnees temporaire pour acceuillir le fichier
        # de l'utilisateur
        files = {'dataFile': open(os.path.join('user', str(interaction.user), fileuser.filename), 'rb')}

        response = requests.post(gbot_url+"/Api/server/uploadForBot/",
            cookies=cookies,
            files=files)
        
        retour = json.loads(response.text)


        if retour['status'] != 1 :
            await interaction.followup.send("Problem with your sequence")

        uid = retour['uid']

        # Utilisation de la librairie permettant de simuler un navigateur web
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service

        from selenium.webdriver.support.ui import WebDriverWait
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1000, 250) 

        # Demande de visualisation de la nouvelle sequence
        driver.get(gbot_url+"/graphsequence.html?uid="+uid+"&start="+str(start)+"&stop="+str(stop))
        html_page = driver.page_source
        # Sauvegarde du screenshoot
        driver.save_screenshot(os.path.join('user','screenshot.png'))
        # envoi de l'image
        await interaction.followup.send(file=discord.File(os.path.join('user','screenshot.png')))
        
        # Effacer le contenu de la base de donnee. 
        headers = {'content-type': 'application/json'}

        response = requests.post(gbot_url+"/Api/server/cleanBot/",
            data=json.dumps({'uid': uid }) ,headers = headers, cookies=cookies
        )




async def setup(bot: commands.Bot):
    await bot.add_cog(GBOTGraphCog(bot))








