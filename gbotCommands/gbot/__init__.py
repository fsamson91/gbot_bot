import discord     # On import Discord c'est bien normal
import json        # json pour les echanges avec la base de donnees
import requests    # request pour passer des urls

from discord import app_commands
from discord.ext import commands
from typing import List
from gbotCommands import urlGender, species, api, chromosome, gettrans, sequence, mycommand

userGender = {}


#  TODO:
#  graph-your-sequence a remettre en ligne egalement... 

def getSpeciesListAsJson(interaction: discord.Interaction) -> list:
    ''' fonction de recuperation de la liste 
        des especes pour un genre donné
        @param interaction : objet de discord

        @return : la liste des especes.
    '''
    gender = checkgender(interaction.user)
    # Definition du genre
    cookies = {'gender': gender}    

    # Appel de l'url de connection a GBOT pour 
    # avoir les species cf bot.cfg
    jsonStr= requests.get(species, cookies=cookies).text
    # Recuperation de la liste json et transformation 
    # en list python
    speciesList = json.loads(jsonStr)
    return speciesList

def getTranslation(gender, cds, comment=None):
    '''
        fonction de recuperation de la protein pour un CDS
        @param gender : le genre pour chercher dans le bon schema
        @cds : le nom du cds a chercher avec le numero de version xxx.y
        @comment : commentaire a ajouter dans le fasta

        @return : None ou la protein en question
        '''
    try:
       
        # Initialisation du cookies utilisé par GBOT
        cookies = {'gender': gender}    

        # Creation de l'URL
        urlGetCDS = gettrans + cds
        # Recuperation de la chaine JSON 
        # Recuperation du ID du feature
        jsonStr= requests.get(urlGetCDS, cookies=cookies).text
        featureId = json.loads(jsonStr)
        # Si on a un ID alors 
        if featureId!=None and 'id' in featureId[0] : 
            # Recuperation de la sequence a partir du ID
            urlGetTrans = sequence + str(featureId[0]['id'])
            # la sequence est sous la forme d'un tableau de chaine du 80car
            seqArray= json.loads(requests.get(urlGetTrans, cookies=cookies).text)
            # Creation du message de retour
            output = f'>{cds}'
            # Si un commentaire est passe a la fonction on l'ajoute 
            # a la ligne de description du fasta
            if comment != None : 
                output+=f' {comment}'
            output+='\n'

            # Pour toutes les sous chaines on concatene!
            for line in seqArray:
                output+=f'{line}\n'
            
            return output
        return None
    except Exception as e:
        print(e)


def checkgender(user):
  """ Fonction de verification du genre pour un utilisateur
      cela permet d'acceder aux plantes et aux mouches
      @param user : nom du user connecté. 
      @return : par defaut Plant sinon le genre de l'utilisateur
  """
  if user in userGender:
    return userGender[user]
  else:
    return 'Plant'

async def gender_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    ''' fonction d'autocompletion pour le nom des genres
        dans la base de données
    '''
    # on requete la base de donnees avec l'url associé 
    #print(urlGender)
    genders = json.loads(requests.get(urlGender).text)
    #print(genders)
    # On cree la liste de genre a partir de notre json
    genderList = [ d['gendername'] for d in genders['list'] ]
    # on cree le tableau des objets discord pour l'affichage de la liste
    discordList = [ app_commands.Choice(name=gender, value=gender) for gender in genderList if current.lower() in gender.lower() ]
    return discordList


async def species_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    ''' 
    autocompletion de l'espece a partir de la liste dans la base de donnees
    @param interaction : objet de discord
    @param current : espece en cours

    @return retourne la liste des especes selectionnables
    '''
    speciesList = getSpeciesListAsJson(interaction)
    return [ app_commands.Choice(name=spe['name'], value=str(spe['id'])+'|'+str(spe['name'])) for spe in speciesList if current.lower() in spe['name'].lower() ]



async def sequence_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    ''' 
    autocompletion double : species puis sequence de l'espece
    @param interaction : objet de discord
    @param current : sequence en cours

    @return retourne la liste des sequences selectionnables
    '''
    # recuperation du parametre necessaire pour fonctionner ici
    # l'espece! qui est passe dans l'objet discord
    species = interaction.namespace.species
    # On recupere le Id
    (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion

    # recuperation du genre
    gender = checkgender(interaction.user)
    cookies = {'gender': gender} 

    # Appel de l'url de connection a GBOT pour 
    # avoir les Sequences cf bot.cfg : url_api/Chromosome/speciesId  
    # on passe les cookies pour avoir le genre
    jsonStr= requests.get(chromosome+speciesId, cookies=cookies).text
    data = json.loads(jsonStr)
    return [ app_commands.Choice(name=seq['accession'], value=str(seq['id'])+'|'+str(seq['accession'])) for seq in data if current.lower() in seq['accession'].lower() ]





class GBOTCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @mycommand(name="set-gender", description="Set the gender for your futur queries", position='10')
    @app_commands.describe(gender="Gender name to use for query the database")
    @app_commands.autocomplete(gender=gender_autocomplete)
    async def setGender(self, interaction:discord.Interaction, gender: str):
        ''' fonction qui permet de definir le genre sur lequel les requetes suivantes 
            vont se faire 
        '''
        try:
            userGender[interaction.user] = gender
            await interaction.response.send_message(f'{interaction.user} set gender to {gender}')
        except Exception as e:
            print(e)

    @mycommand(name="get-species", description="Get species list for current gender", position='11')
    async def getspecies(self, interaction: discord.Interaction):
        '''
        fonction de recuperation de la liste des especes
        dans la base de donnees et l'affiche sur l'interface discord

        @param interaction : objet de discord
        '''
        # Recuperation du genre
        gender = checkgender(interaction.user)

        # Recuperation de la liste a partir du json
        speciesList = getSpeciesListAsJson(interaction)
        
        if speciesList!=None and 'id' in speciesList[0] : 
            # Creation du message de retour
            output = f'{interaction.user} connected on {gender}\n```'
            for d in speciesList:
                output += d['name']+'\n'
            output+= '```'
            await interaction.response.send_message(output)
        else : 
            await interaction.response.send_message('Species invalide/inexistant !')


    @mycommand(name="get-sequences", description="Get sequence list for a species", position='12')
    @app_commands.describe(species="select a species from the list avalaible in the GBOT database")
    @app_commands.autocomplete(species=species_autocomplete)
    async def getsequences(self, interaction: discord.Interaction, species: str):
        '''
        Fontion de recuperation de la liste des sequences
        pour une espece choisi en parametre, l'affichage se fait dans
        l'interface discord
        
        @param_discord : species (autocompletion)
        @param interaction : objet de discord
        @param species: species choisi par l'utilisateur
        
        '''
    
        # Recuperation du genre
        gender = checkgender(interaction.user)
        
        # Initialisation du cookies utilisé par GBOT
        cookies = {'gender': gender} 

        # Recuperation de l'espece venanat de l'autocompletion
        (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
        # Appel de l'url de connection a GBOT pour 
        # avoir les Sequences cf bot.cfg : url_api/Chromosome  
        # on passe les cookies pour avoir le genre
        jsonStr= requests.get(chromosome+speciesId, cookies=cookies).text
        sequencesList = json.loads(jsonStr)
        # Mise en page pour discord
        if sequencesList!=None and 'id' in sequencesList[0] : 
            # Creation de la sortie.
            output = f'{interaction.user} connected on {gender}\n```'
            for d in sequencesList:
                output += d['name']+'\t'+str(d['length'])+"bp\n"
            output+= '```'
            await interaction.response.send_message(output)
        else : 
            await interaction.response.send_message('Species invalide/inexistant !')
    

    
    @mycommand(name="get-translation", description="Get proteic sequence of a cds", position='13')
    @app_commands.describe(cds="get the gene ID with the version number like xxx.y  ")
    async def gettranslation(self, interaction: discord.Interaction, cds:str):
        ''' 
        Fonction de recuperation d'une proteine dans la
        base de donnees 

        @param interaction : objet de discord
        @param : cds nom de la proteine
        '''
         # Recuperation du genre
        gender = checkgender(interaction.user)

        try:
            # Recuperation de la protein avec le ID : cds
            trans = getTranslation(gender,cds)
            # si on a pas de retour => message d'erreur
            if trans == None :
                await interaction.response.send_message('CDS invalide/inexistant !')
            # Sinon on affiche la sequence.
            else : 
                output = f'{interaction.user} connected on {gender}\n```\n'
                output+=trans+"\n"
           
                output+='```'
                await interaction.response.send_message(output)
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(GBOTCog(bot))








