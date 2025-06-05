import discord
from discord.ext import commands
from discord import app_commands, Embed, Colour
from discord.ui import View, Button
from gbotCommands import web, addgbot, pierrick, papa, command_list, mycommand

command_order = {}

# Objet pour referencer un bug dans l'application 
# avec envoi de message aux developpeurs.
class BugReportModal(discord.ui.Modal):
    def __init__(self, mybot = None):
        super().__init__(title="Bug Report")
        self.bot = mybot

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
        try:
            await interaction.response.send_message(f"Thanks for your report {interaction.user}", ephemeral=True)
            user = await self.bot.fetch_user(pierrick)
            await user.send(f"🚨 **Bug report** \n By {interaction.user} \n \n  __Bug's command name__ :  \n  > *{self.name.value}* \n \n   __Bug's description__ : \n > *{self.about.value}* ")
            user = await self.bot.fetch_user(int(papa))
            await user.send(f"🚨 **Bug report** \n By {interaction.user} \n \n  __Bug's command name__ :  \n  > *{self.name.value}* \n \n   __Bug's description__ : \n  > *{self.about.value}* ")
        except Exception as e:
            print(e)


def configHelp(embedMenu, pos, title, subtitle):
    # get main commands 
    list_command = [position for position, command in command_list.items() if position.startswith(pos)]
    list_command.sort()

    embedMenu.add_field(name="📌 "+title, value="🔹"+subtitle)
    for command in list_command:
        command_name = command_list[command]['name']
        command_desc = command_list[command]['description']
        embedMenu.add_field(name=f"/{command_name}", value=f"{command_desc}", inline=False)



class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Donne l'adresse du site web de gbot
    @mycommand(name="website", description="Get website link", position='02')
    async def website(self, interaction:discord.Interaction):
        bouton = Button(label="Visit gbot website", url=web)
        view = View()
        view.add_item(bouton)

        await interaction.response.send_message("Gbot Link :", view=view )
    
    # Permet d'ajouter ce bot a un autre serveur bot
   
    @mycommand(name="add-gbot", description="Get link to add gbot to your server", position='03')
    async def addgbot(self, interaction:discord.Interaction):
        button = Button(label="Add gbot",  url=addgbot )
        view = View()
        view.add_item(button)
       
        await interaction.response.send_message( view=view )


    @mycommand(name="help",  description="Show this GBOT help", position='00')
    async def help_command(self, interaction: discord.Interaction):

        try:
            embed = Embed(title="📘 Available commands", color=Colour.blue())
            configHelp(embed,'0',"Bot commands", "Commands to interact with the bot" )
            configHelp(embed,'1',"GBOT simple commands", "Simple commands to retreive data in GBOT database" )
            configHelp(embed,'2',"GBOT aligment commands", "Blast commands on GBOT sequences" )
            configHelp(embed,'3',"GBOT PFAM commands", "Retreive PFAM information in GBOT database" )
            configHelp(embed,'4',"GBOT graph commands", "Draw sequence from database or draw your sequence" )
           
        except Exception as e:
            print(e)
        await interaction.response.send_message(embed=embed)

    
    @mycommand(name="report-a-bug", description="Report a bug", position='01')
    async def Test(self, interaction: discord.Interaction):
        
        try:
            await interaction.response.send_modal(BugReportModal(mybot=self.bot))
        except Exception as e:
            print(e)    


async def setup(bot: commands.Bot):
    await bot.add_cog(BaseCog(bot))








