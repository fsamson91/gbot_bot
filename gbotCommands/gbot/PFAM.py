import os
import discord     # On import Discord c'est bien normal
import json        # json pour les echanges avec la base de donnees
import requests    # request pour passer des urls

from discord import app_commands
from discord.ext import commands
from typing import List
from gbotCommands import pfamlist, groupinfo, mycommand
from gbotCommands.gbot import  checkgender, species_autocomplete, getTranslation






class GBOTPFAMCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @mycommand(name="get-pfam", description="Get genes for the pfam ID choosen", position='30')
    @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
    @app_commands.describe(pfamid="the pfamid to retreive and get the genes that have this motif in the GBOT database")
    @app_commands.autocomplete(species=species_autocomplete)
    async def pfam(self, 
                    interaction:discord.Interaction, 
                    species:str,
                    pfamid:str
                    ):
        '''
        Fonction d'execution de la commande blast(n,p,x,t..n) 
        sur une sequence venant d'un upload.
        sur une espece choisi en autocompletion
        @param interaction : objet de discord
        @param species : espece a interoger
        @param pfamid : nom du pfam a interroger
        '''
        try :
            # Recuperation de l'espece venanat de l'autocompletion   
            (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion

            # Recuperation du genre
            gender = checkgender(interaction.user)
            
            # Initialisation du cookies utilisé par GBOT
            cookies = {'gender': gender} 
           
            
            # Appel de l'url de connection a GBOT pour 
            # avoir les Information concernant ce groupe pfam
            # on passe les cookies pour avoir le genre
            jsonStr= requests.get(groupinfo+pfamid+"/"+speciesId, cookies=cookies).text
            if jsonStr[0]=='<' :
                print("icic")
                await interaction.response.send_message('PFAM invalide/inexistant !')
            else :
                pfamGroup = json.loads(jsonStr)
                pfamId = pfamGroup['id']
                # Call discord to wait 
                await interaction.response.defer()

                # Appel de l'url de connection a GBOT pour 
                # avoir les Information concernant les genes du group
                # on passe les cookies pour avoir le genre
                print(pfamlist+str(pfamId)+"/"+str(speciesId))
                jsonStr = requests.get(pfamlist+str(pfamId)+"/"+str(speciesId), cookies=cookies).text
                featureList=  json.loads(jsonStr)
                # Creation de la sortie.
                try:
                    # Si le repertoire n'existe pas on cree
                    if not os.path.isdir(os.path.join('user',str(interaction.user))) :
                        print("Create "+(os.path.join('user',str(interaction.user)))+" directory")
                        try:
                            os.makedirs(os.path.join('user', str(interaction.user)))
                        except:
                            print("Can't create "+(os.path.join('user',str(interaction.user)))+" directory")
                
                    # on cree le fichier de sortie
                    file = open(os.path.join('user', str(interaction.user), "pfamlist.txt"), "w")
                    output = f'{interaction.user} connected on {gender} get pfam list for : {pfamid}\n'
                    output+= "gene"+'\t\t'+'length'+'\t'+'loc.'+'\t'+'product\n'
                    # Pour tout les genes on ajoute dans la sortie
                    for f in featureList:
                        output += str(f['idf'])+'\t'+str(f['stop']-f['start']+1)+"bp\t"+str(f['loc'][0])+'\t'
                        if 'frames' in f:
                            output += f['frames']['product']
                        output+='\n'
                    file.write(output)
                    file.close()
                    await interaction.followup.send(file=discord.File(os.path.join('user', str(interaction.user), "pfamlist.txt")))

                except Exception as e:
                    print(e)
                



        except Exception as e:
            print(e)


    @mycommand(name="get-pfam-prot", description="Get genes protein files for the pfam ID choosen", position='31')
    @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
    @app_commands.describe(pfamid="the pfamid to retreive and get the genes that have this motif in the GBOT database")
    @app_commands.autocomplete(species=species_autocomplete)
    async def pfamasprot(self, 
                    interaction:discord.Interaction, 
                    species:str,
                    pfamid:str
                    ):
        '''
        Fonction d'execution de la commande blast(n,p,x,t..n) 
        sur une sequence venant d'un upload.
        sur une espece choisi en autocompletion
        @param interaction : objet de discord
        @param species : espece a interoger
        @param pfamid : nom du pfam a interroger
        '''
        try :
            # Recuperation de l'espece venanat de l'autocompletion   
            (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion

            # Recuperation du genre
            gender = checkgender(interaction.user)
            
            # Initialisation du cookies utilisé par GBOT
            cookies = {'gender': gender} 
           
            
            # Appel de l'url de connection a GBOT pour 
            # avoir les Information concernant ce groupe pfam
            # on passe les cookies pour avoir le genre
            jsonStr= requests.get(groupinfo+pfamid+"/"+speciesId, cookies=cookies).text
            if jsonStr[0]=='<' :
                print("icic")
                await interaction.response.send_message('PFAM invalide/inexistant !')
            else :
                pfamGroup = json.loads(jsonStr)
                pfamId = pfamGroup['id']
                # Call discord to wait 
                await interaction.response.defer()

                # Appel de l'url de connection a GBOT pour 
                # avoir les Information concernant les genes du group
                # on passe les cookies pour avoir le genre
                print(pfamlist+str(pfamId)+"/"+str(speciesId))
                jsonStr = requests.get(pfamlist+str(pfamId)+"/"+str(speciesId), cookies=cookies).text
                featureList=  json.loads(jsonStr)
                # Creation de la sortie.
                try:
                    # Si le repertoire n'existe pas on cree
                    if not os.path.isdir(os.path.join('user',str(interaction.user))) :
                        print("Create "+(os.path.join('user',str(interaction.user)))+" directory")
                        try:
                            os.makedirs(os.path.join('user', str(interaction.user)))
                        except:
                            print("Can't create "+(os.path.join('user',str(interaction.user)))+" directory")
                
                    # on cree le fichier de sortie
                    file = open(os.path.join('user', str(interaction.user), "pfamlist.txt"), "w")
                    output = f'{interaction.user} connected on {gender} get pfam list for : {pfamid}\n'
                    # Pour tout les genes on ajoute dans la sortie
                    for f in featureList:
                        comment = '|'+str(f['stop']-f['start']+1)+"bp|"+str(f['loc'][0])
                        if 'frames' in f:
                            comment += '|'+f['frames']['product']
                        trans = getTranslation(gender,f['idf'],comment  )
                        output += trans
                    file.write(output)
                    file.close()
                    await interaction.followup.send(file=discord.File(os.path.join('user', str(interaction.user), "pfamlist.txt")))

                except Exception as e:
                    print(e)
                
        
                

        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(GBOTPFAMCog(bot))








