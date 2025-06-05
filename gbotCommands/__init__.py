import configparser
import sys
import discord
from discord import app_commands
import functools



key = None         # Cle du serveur bot
pierrick = None
papa = None
sequence = None
species = None
pfamlist = None
groupinfo = None
web = None
addgbot = None
urlGender = None
gettrans = None
gbot_url = None # URL de gbot 
api = None  # URL de L'API de gbot


# Lecture des variables du fichier de configuration
try:
  
    config = configparser.ConfigParser()
    with open("bot.cfg") as f:
        config.read_file(f)

        if 'CONFIG' in config:
            key = config['CONFIG']['key']
            pierrick = config['CONFIG']['pierrick']
            papa = config['CONFIG']['papa']
            api = config['CONFIG']['api']
            gbot_url = config['CONFIG']['gbot']
            sequence = config['CONFIG']['sequence']
            species = config['CONFIG']['species']
            chromosome = config['CONFIG']['chromosome']
            blast = config['CONFIG']['blast']
            pfamlist = config['CONFIG']['pfamlist']
            groupinfo = config['CONFIG']['groupinfo']
            web = config['CONFIG']['web']
            addgbot = config['CONFIG']['add']
            urlGender = config['CONFIG']['gender']
            gettrans = config['CONFIG']['gettrans']


except IOError as fnf_error:
    print(fnf_error)
    sys.exit(-1)


intents = discord.Intents.all() 

command_list = {}
# Surcharge du decorateur @app_command pour permetre l'ajout d'un parametre 
# pour gerer la priorite des fonctions discord
def mycommand(name, description, position):
    def decorator(func):
        command_list[position] = { 'name': name, 'description': description }
        @app_commands.command(name=name, description=description)
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try : 
                print(*args)
                print("Ajout du nouveau décorateur")
                result = await func(*args, **kwargs)
            except Exception as e :
                print(e)
            return result
        return wrapper
    return decorator






