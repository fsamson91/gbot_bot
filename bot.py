import discord
import discord.ext
import requests
import json
import configparser
import sys
import os

from discord import app_commands
from typing import List, Literal, Optional

userGender = {}

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


# Objects de discord
intents = discord.Intents.all() 
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


key = None         # Cle du serveur bot
pierrick = None
papa = None
sequence = None
specices = None
web = None
add = None
urlGender = None
gettrans = None
gbot = None # URL de gbot 
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
            gbot = config['CONFIG']['gbot']
            sequence = config['CONFIG']['sequence']
            species = config['CONFIG']['species']
            web = config['CONFIG']['web']
            add = config['CONFIG']['add']
            urlGender = config['CONFIG']['gender']
            gettrans = config['CONFIG']['gettrans']


except IOError as fnf_error:
    print(fnf_error)
    sys.exit(-1)


# Objet pour referencer un bug dans l'application 
# avec envoi de message aux developpeurs.
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
    



# Lien gbot
class Link(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Visit gbot website", style=discord.ButtonStyle.url, url = web )
        self.add_item(button)


# Add gbot ?
class Gbot(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Add gbot", style=discord.ButtonStyle.url, url = add )
        self.add_item(button)
     

# Message d'invite quand l'on se connecte au bot
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game("/gbot"))
    

################## A MODIFIER ######################""

# Affiche la liste des commandes du bot
@tree.command(name="gbot", description="Get list of commands")
async def gbot(interaction: discord.Interaction):
    await interaction.response.send_message('`/gbot`: Get list of commands \n`/set-gender` :  \n`/get-translation` : Get proteic sequence of a cds \n`/get-species` : Get sequence list\n`/website`: Get website link ')

################## A MODIFIER ######################""


# Donne l'adresse du site web de gbot
@tree.command(name="website", description="Get website link")
async def website(interaction:discord.Interaction):
    await interaction.response.send_message(view=Link())

# Permet d'ajouter ce bot a un autre serveur bot
@tree.command(name="add-gbot", description="Get link to add gbot to your server")
async def addgbot(interaction:discord.Interaction):
    await interaction.response.send_message(view=Gbot())

# Ajouter un rapport de bug
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


''' 
    Fonction de recuperation d'une proteine dans la
    base de donnees 
    parametre : cds nom de la proteine
'''
@tree.command(name="get-translation", description="Get proteic sequence of a cds")
async def getsequencetxt(interaction: discord.Interaction, cds:str):
    # Recuperation du genre
    gender = checkgender(interaction.user)
    # Initialisation du cookies utilisé par GBOT
    cookies = {'gender': gender}    

    # Creation de l'URL
    urlGetCDS = gettrans + cds
    # Recuperation de la chaine JSON 
    # Recuperation du ID du feature
    jsonStr= requests.get(urlGetCDS, cookies=cookies).text
    data = json.loads(jsonStr)
    if data!=None and 'id' in data[0] : 
        # Recuperation de la sequence a partir du ID
        urlGetTrans = sequence + str(data[0]['id'])
        seqArray= json.loads(requests.get(urlGetTrans, cookies=cookies).text)
        # Creation du message de retour
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


'''
    fonction de recuperation de la liste des especes
    dans la base de donnees
'''
@tree.command(name="get-species", description="Get species list for current gender")
async def getspecies(interaction: discord.Interaction):
    # Recuperation du genre
    gender = checkgender(interaction.user)

    # Recuperation de la liste a partir du json
    data = getSpeciesListAsJson(interaction)
    
    if data!=None and 'id' in data[0] : 
        # Creation du message de retour
        output = f'{interaction.user} connected on {gender}\n```'
        for d in data:
            output += d['name']+'\n'
        output+= '```'
        await interaction.response.send_message(output)
    else : 
        await interaction.response.send_message('Species invalide/inexistant !')



''' 
    autocompletion de l'espece a partir de la liste dans la base de donnees
'''
async def species_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    data = getSpeciesListAsJson(interaction)
    return [ app_commands.Choice(name=spe['name'], value=str(spe['id'])+'|'+str(spe['name'])) for spe in data if current.lower() in spe['name'].lower() ]


'''
    Fontion de recuperation de la liste des sequences
    pour une espece choisi en parametre
    parametre : species (autocompletion)
'''
@tree.command(name="get-sequences", description="Get sequence list for a species")
@app_commands.autocomplete(species=species_autocomplete)
async def getsequences(interaction: discord.Interaction, species: str):
    # Recuperation du genre
    gender = checkgender(interaction.user)
    
    # Initialisation du cookies utilisé par GBOT
    cookies = {'gender': gender} 

    # Recuperation de l'espece venanat de l'autocompletion
    (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
    # Requete de recuperation des informations
    jsonStr= requests.get(api+'/Chromosome/'+speciesId, cookies=cookies).text
    data = json.loads(jsonStr)
    if data!=None and 'id' in data[0] : 
        # Creation de la sortie.
        output = f'{interaction.user} connected on {gender}\n```'
        for d in data:
            output += d['name']+'\t'+str(d['length'])+"bp\n"
        output+= '```'
        await interaction.response.send_message(output)
    else : 
        await interaction.response.send_message('Species invalide/inexistant !')


'''
    Fonction d'execution de la commande blast(n,p,x,t..n) 
    sur une sequence venant d'un upload.
    sur une espece choisi en autocompletion
    parametre : fileuser fichier a blaster
                program programme a utilise choisi dans une liste
                species (autocompletion)
'''
@tree.command(name="blast")
@app_commands.autocomplete(species=species_autocomplete)
async def blast(interaction:discord.Interaction, 
                 fileuser:discord.Attachment,
                 program: Literal['blastp', 'blastn', 'blastx', 'tblastn'],
                 species:str
                 ):
    # Recuperation de l'espece venanat de l'autocompletion   
    (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
    # creation si necessaire du repertoire de sortie
    if not os.path.isdir('user'):
        os.makedirs('user')
    # Sauvegarde du fichier de l'utilisateur dans le repertoire
    await fileuser.save(os.path.join('user',fileuser.filename))
    sequence = ""
    file = open(os.path.join('user', fileuser.filename))
    file.readline()
    for line in file:
        line = line.rstrip()
        sequence+=line
    file.close()

    # Recuperation du genre
    gender = checkgender(interaction.user)
    
    # Initialisation du cookies utilisé par GBOT
    cookies = {'gender': gender} 
    # Preparation des parametres pour la commande
    # post du blast sur GBOT
    headers = {'content-type': 'application/json'}
    parameter = {'program': program, 
                 'evalue': '1e-5',
                 'wordsize': 3,
                 'txt': 1,
                 'sequence': sequence,
                 'speciesId': speciesId,
                 'speciesName' : speciesName,
                 'inter' : 'false',
                 'gender': 'Plant'
                 }
    # Mettre en attente discord
    await interaction.response.defer()
    # Requete blast
    response = requests.post(api+"/server"+"/Blast/",data=json.dumps(parameter),headers = headers, cookies=cookies)
    
    # Recuperation du fichier de resultat
    with open(os.path.join('user', fileuser.filename+"_result"), "wb") as file:
        file.write(response.content)
    file.close()

    entityFileName = fileuser.filename+"_result"

    # Send embed notifying start of the spam stream
    detailsEmbed = discord.Embed(
        colour=discord.Colour.red(),
        title=f"See `{entityFileName}` for your blast result",
        description="Due to discord character limits regarding embeds, the results have to be sent in a file"
    )
    await interaction.followup.send(embed=detailsEmbed, file=discord.File(os.path.join('user', fileuser.filename+"_result")))


''' 
    autocompletion double : species puis sequence de l'espece
'''
async def sequence_autocomplete(interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    data = getSpeciesListAsJson(interaction)
    print(interaction.namespace.species)
    species = interaction.namespace.species
    if species == "":
        return [ app_commands.Choice(name=spe['name'], value=str(spe['id'])+'|'+str(spe['name'])) for spe in data if current.lower() in spe['name'].lower() ]
    else: 
        gender = checkgender(interaction.user)
        cookies = {'gender': gender} 

        (speciesId, speciesName) = species.split('|') # regarder la value de l'autocompletion
        jsonStr= requests.get(api+'/Chromosome/'+speciesId, cookies=cookies).text
        data = json.loads(jsonStr)
        return [ app_commands.Choice(name=seq['accession'], value=str(seq['id'])+'|'+str(seq['accession'])) for seq in data if current.lower() in seq['accession'].lower() ]
        

'''
    Fonction d'affichage d'un graph a partir d'un bout de sequence 
    de la base de donnees
    parametre : species espece,
                sequence (autocompletion comme espece)
                start position de debut
                stop position de fin
'''
@tree.command(name="graph-sequence")
@app_commands.autocomplete(species=sequence_autocomplete, sequence=sequence_autocomplete)
async def graphsequence(interaction:discord.Interaction, 
                    species:str,
                    sequence:str,
                 start: int,
                 stop: int
                 ):
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

    print(gbot+"/graphsequence.html?uid="+gender+
        "&species="+speciesId+
        "&sequence="+sequenceId+
        "&start="+str(start)+
        "&stop="+str(stop))

    # Appel de l'url correspondante pour generer l'image
    driver.get(gbot+"/graphsequence.html?uid="+gender+
        "&species="+speciesId+
        "&sequence="+sequenceId+
        "&start="+str(start)+
        "&stop="+str(stop))
    html_page = driver.page_source

    
    # Creation du screenshoot
    #print(os.path.join(os.getcwd(),'user','screenshot.png'))
    driver.save_screenshot('screenshot.png')

    
    await interaction.followup.send(file=discord.File(os.path.join('user','screenshot.png')))
    




'''
    Fonction de recuperation d'un svg a partir d'un bout de sequence 
    de la base de donnees
    parametre : species espece,
                sequence (autocompletion comme espece)
                start position de debut
                stop position de fin
'''
@tree.command(name="graph-sequence-svg")
@app_commands.autocomplete(species=sequence_autocomplete, sequence=sequence_autocomplete)
async def graphsequenceassvg(interaction:discord.Interaction, 
                    species:str,
                    sequence:str,
                 start: int,
                 stop: int
                 ):
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
    from selenium.webdriver.common.by import By

    from selenium.webdriver.chrome.service import Service

    from selenium.webdriver.support.ui import WebDriverWait
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1000, 250) 

    print(gbot+"/graphsequence.html?uid="+gender+
      "&species="+speciesId+
      "&sequence="+sequenceId+
      "&start="+str(start)+
      "&stop="+str(stop))

    # Appel de l'url correspondante pour generer l'image
    driver.get(gbot+"/graphsequence.html?uid="+gender+
        "&species="+speciesId+
        "&sequence="+sequenceId+
        "&start="+str(start)+
        "&stop="+str(stop))
    html_page = driver.page_source

    import re
    exp = re.search('<svg.+?(</svg>)',html_page)
    svg = exp.group(0)
    print(svg)
    
     # backup de l'image et envoie de celle ci
    if not os.path.isdir('user'):
        os.makedirs('user')

 

    svg = svg.replace("><", ">\n"+
    """
<style>
.axis text {
  font-family: Verdana, Arial, Helvetica, sans-serif;
  font-size: 1em;
}

.axis line {
  shape-rendering: crispEdges;
  opacity: 0.2;
  stroke-width: 1px;
}

.axis .minor line {
  stroke: red;
  stroke-width: 1px;
  opacity: 0.1;
  stroke-dasharray: 6,4;
}


g.Motif g.highlight {
  stroke : red;
  stroke-width: 5px;
  fill: white;
  z-index: 10;
}


g.highlight {
  stroke : red;
  fill: red;
  stroke-width: 3px;
  z-index: 10;
}


.gap {
  stroke: #818181;
  fill: #818181;
}

.PFAM {
  stroke: #64191e;
  fill: black;
}

.est_cdna {
  stroke: #bc09bc;
  fill: #bc09bc;
}

.SeqFeature {
  stroke: #bc09bc;
  fill: hsl(63, 100%, 50%);
}

.tRNA,
.miRNA,
.otherRNA,
.npcRNA,
.ncRNA,
.snRNA,
.rRNA,
.snoRNA {
  stroke: #000000;
  fill: #ff4a2d;
}

.MIR{
  stroke: #000000;
  fill: #ffff00;
}


.CDS {
  stroke: #0000ff;
  fill: #0000ff;
}

.CDSDensity {
  stroke: #0000ff;
}


.Blast {
  stroke: #f9735a;
  fill: #eb4f0a;
}


.CDS .no{
  background-color: #0000ff;
  color: white;
  stroke: #0000ff;
  fill: #0000ff;
  font-size: 11pt;

}

.CDS .nucleus{
  background-color: #ffff00;
  color: black;
  stroke: #ffff00;
  fill: #ffff00;
  font-size: 11pt;

}

.CDS .plastid{
  background-color: #00ff00;;
  color: black;
  stroke: #00ff00;
  fill: #00ff00;
  font-size: 11pt;

}

.CDS .endo_reticulum {
  background-color: black;
  color: white;
  stroke: black;
  fill: black;
  font-size: 11pt;

}

.CDS .mitochondria {
  background-color: red;
  color: black;
  stroke: red;
  fill: red;
  font-size: 11pt;

}

.FST,
.SNP {
  stroke: black;
  fill: #ff0000;
}

.mRNA {
  stroke: #3bd1e1;
  fill: #3bd1e1;
}


.mobile_element {
  stroke: none;
  fill: #c5c5c5 ;
}

.repeat_region,
.Repeat_Element {
  stroke: white;
  fill: #949494 ;
}

.TE  {
  stroke: rgb(255, 153, 36);
  fill: #ffd6a0 ;
}


.MPSS_smallRNA {
  stroke: black;
  fill: #57f700 ;
}

.MPSS {
  stroke: black;
  fill: #00d5e4 ;
}

.AFFYMETRIX {
  stroke: #ff4851;
  fill: #ff4851 ;
}


.Repeat_TAIR {
  stroke: #949494 ;
  fill: #949494 ;
}


.CDS_Eugene {
  stroke: black;
  fill: #9800d0;
}

.CDS_Jigsaw {
  stroke: black;
  fill: #b1f0d3;
}

.LTR{
  stroke: #5f84e9;
  fill: #5f7fe9;
}


.PPR_CDS {
  stroke: black;
  fill: #e2a812;
}

.PPR_motif {
  stroke: black;
  fill: #e2a812;
}

.PPR_motif .S{
  stroke: #e9e05f;
  fill: #e9e05f;
}

.PPR_motif .P{
  stroke: #e2a812;
  fill: #e2a812;
}

.PPR_motif .L{
  stroke: #ca7f1e;
  fill: #ca7f1e;
}

.PPR_motif .E{
  stroke: #68ba2a;
  fill: #68ba2a;
}

.PPR_motif .eplus{
  stroke: #5f965e;
  fill: #5f965e;
}

.multi {
  stroke: black;
}

.SMAR{
  stroke: #b67d3e;
  fill: #b67d3e;
}

.CDS_GeneFarm {
  stroke: black;
  fill: #008300;
}

.CDS_Alternative {
  stroke: black;
  fill: #000eff;
}

.mRNA_Alternative {
  stroke: black;
  fill: #33d3e4;
}


.GST {
  stroke: #af26fb;
  fill: #af26fb;
}

.MIRSPOT {
  stroke: #df76fe;
  fill: #df76fe;
}

.ChromoChip {
  stroke: #ffa713;
  fill: #ffa713;
}


.SNP_probe {
  stroke: #ffa713;
  fill: #ffa713;
}

.CATMA_v6 {
  stroke: #c100b3;
  fill: #c100b3;
}

.TPS,
.CHS,
.RGA,
.STS {
  stroke: black;
  fill: #008300;
}

.NimbleGen,
.NimbleGen_v1, 
.Agilent_v1 {
  stroke: #ebc100;
  fill: #ebc100;
}


.RseqContig_Flowers{
  stroke: #ebc100;
  fill: rgb(97, 80, 2);
}

.RseqContig_MixOrgans{
  stroke: #524817;
  fill: rgb(215, 201, 141);
}

.notextfeat {
    stroke: none;
    fill: none;
    color: none;
    display: none;
}
.txtfeat {
  font-family: 'open sans',arial,sans-serif;
  text-anchor: middle;
  stroke: none;
  font-size: 9px;
}


rect.cadre {
  fill: rgb(252,252,242);
  stroke: lightblue;
}

path.domain {
    stroke: white;
}
.A{
  fill: green;
  stroke: green;
  stroke-linecap: round;
  stroke-width: 4;

}
.G{
  stroke: orange;
  stroke-linecap: round;
  stroke-width: 4;
  fill: white;

}
.C{
  stroke: blue;
  stroke-linecap: round;
  stroke-width: 4;
  fill: white;
}
.T{
  fill: red;
  stroke: red;
  stroke-linecap: round;
  stroke-width: 4;

}
.Aa{
  fill: none;
  stroke: green;
  stroke-linecap: round;
}

.Ga{
  stroke: #e19c18;
  stroke-linecap: round;
  fill: none;

}
.Ca{
  stroke: blue;
  stroke-linecap: round;
  fill: none;
}
.Ta{
  fill: red;
  stroke: red;
  stroke-linecap: round;
}



</style>
"""+"<",1)

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




'''
    Graph votre propre sequence uploade en parametre 
    parametre : fileuser genbank a visualiser
                start position de debut
                stop position de fin 
'''

@tree.command(name="graph-your-sequence")
async def graphit(interaction:discord.Interaction, 
                 fileuser:discord.Attachment,
                 start: Optional[int] = 0,
                 stop: Optional[int] = -1
                 ):
    # Get File on server
    if not os.path.isdir('user'):
        os.makedirs('user')
    # Sauvegarde du fichier utilisateur
    await fileuser.save(os.path.join('user',fileuser.filename))
    sequence = ""
    file = open(os.path.join('user', fileuser.filename))
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
    files = {'dataFile': open(os.path.join('user', fileuser.filename), 'rb')}

    response = requests.post("http://192.168.216.97:8088/my_pref/Api/server/uploadForBot/",
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
    driver.get("http://192.168.216.97:8088/my_pref/GBOT/graphsequence.html?uid="+uid+"&start="+str(start)+"&stop="+str(stop))
    html_page = driver.page_source
    # Sauvegarde du screenshoot
    driver.save_screenshot(os.path.join('user','screenshot.png'))
    # envoi de l'image
    await interaction.followup.send(file=discord.File(os.path.join('user','screenshot.png')))
    
    # Effacer le contenu de la base de donnee. 
    headers = {'content-type': 'application/json'}

    response = requests.post("http://192.168.216.97:8088/my_pref/Api/server/cleanBot/",
        data=json.dumps({'uid': uid }) ,headers = headers, cookies=cookies
       )


if __name__ == '__main__':
    client.run(key, root_logger=True)



