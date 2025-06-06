import discord
from discord.ext import commands
import asyncio

from gbotCommands import key, intents





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