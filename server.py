import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_member_join(member):
    
    channel = discord.utils.get(member.guild.channels, name="👋-introductions")
    
    if channel:
        welcome_1_liner = f"Welcome to the community, {member.mention}! Glad to have you here. "
        
        await channel.send(welcome_1_liner)


@bot.command()
async def ping(ctx):
    await ctx.send(f"| Pong! {round(bot.latency * 500)}ms")

@bot.command()
async def testjoin(ctx):
    
    await on_member_join(ctx.author)


if TOKEN:
    # Start the background web server
    keep_alive()
    # Start the Discord bot
    bot.run(TOKEN)
else:
    print("Error: No token found. Check .env file!")