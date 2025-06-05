import os
import discord     # On import Discord c'est bien normal
import json        # json pour les echanges avec la base de donnees
import requests    # request pour passer des urls

from discord import app_commands
from discord.ext import commands
from typing import Literal
from gbotCommands.gbot import species_autocomplete, checkgender
from gbotCommands import blast, mycommand


class GBOTBlastCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @mycommand(name="blast", description="Blast your sequence on GBOT species", position='20')
    @app_commands.describe(fileuser="Upload your sequence file to blast")
    @app_commands.describe(program="Choose your blast tool")
    @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
    @app_commands.autocomplete(species=species_autocomplete)
    async def blast(self, 
                    interaction:discord.Interaction, 
                    fileuser:discord.Attachment,
                    program: Literal['blastp', 'blastn', 'blastx', 'tblastn'],
                    species:str
                    ):
        '''
        Fonction d'execution de la commande blast(n,p,x,t..n) 
        sur une sequence venant d'un upload.
        sur une espece choisi en autocompletion
        @param interaction : objet de discord
        @param fileuser : fichier a blaster
        @param program : programme a utilise choisi dans une liste
        @species species (autocompletion)
        '''
        try:
            # Recuperation de l'espece venanat de l'autocompletion   
            (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
            # creation si necessaire du repertoire de sortie
            if not os.path.isdir('user'):
                os.makedirs('user')
            # Mettre en attente discord
            await interaction.response.defer()
            # Si le repertoire n'existe pas pour le user on le cree
            if not os.path.isdir(os.path.join('user',str(interaction.user))) :
                print("Create "+(os.path.join('user',str(interaction.user)))+" directory")
                try:
                    os.makedirs(os.path.join('user', str(interaction.user)))
                except:
                    print("Can't create "+(os.path.join('user',str(interaction.user)))+" directory")

            # Sauvegarde du fichier de l'utilisateur dans le repertoire
            await fileuser.save(os.path.join('user',str(interaction.user),fileuser.filename))
            sequence = ""
            file = open(os.path.join('user', str(interaction.user), fileuser.filename))
            file.readline()
            for line in file:
                line = line.rstrip()
                sequence+=line
            file.close()

            # Creation de la base de donnees temporaire pour acceuillir le fichier
            # de l'utilisateur
            files = {'dataFile': open(os.path.join('user', str(interaction.user), fileuser.filename), 'rb')}

            # Recuperation du genre
            gender = checkgender(interaction.user)
            
            # Initialisation du cookies utilisé par GBOT
            cookies = {'gender': gender} 
            # Preparation des parametres pour la commande
            # post du blast sur GBOT
            parameter = {'program': program, 
                        'evalue': '1e-5',
                        'wordsize': 4,
                        'speciesId': speciesId,
                        'speciesName' : speciesName,
                        'gender': gender
                        }
            

            # Appel de l'url de connection a GBOT pour 
            # avoir les Blast cf bot.cfg : url_api/server/Blast  
            # on passe les cookies pour avoir le genre
            response = requests.post(blast,data=parameter,
                cookies=cookies,
                files=files)

            # Recuperation du fichier de resultat
            with open(os.path.join('user', str(interaction.user), fileuser.filename+"_result"), "wb") as file:
                file.write(response.content)
            file.close()

            entityFileName = fileuser.filename+"_result"

            # Send embed notifying start of the spam stream
            detailsEmbed = discord.Embed(
                colour=discord.Colour.red(),
                title=f"See `{entityFileName}` for your blast result",
                description="Due to discord character limits regarding embeds, the results have to be sent in a file"
            )
            await interaction.followup.send(embed=detailsEmbed, file=discord.File(os.path.join('user', str(interaction.user) ,fileuser.filename+"_result")))
        except Exception as e:
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(GBOTBlastCog(bot))








