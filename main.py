import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Sync slash commands when bot is ready
@bot.event
async def on_ready():
    print(f"✅ glitchy.bot is ONLINE as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Synced {len(synced)} global slash commands.")
        for guild in bot.guilds:
            await bot.tree.sync(guild=discord.Object(id=guild.id))
            print(f"🔁 Synced slash commands for: {guild.name}")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

# Dynamically load all cogs from cogs/
async def load_cogs():
    loaded = 0
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_") and filename != "utils.py":
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
                loaded += 1
            except Exception as e:
                print(f"❌ Failed to load cog {filename}: {e}")
    print(f"📦 Total cogs loaded: {loaded}")

# Run everything
async def main():
    await load_cogs()
    await bot.start(TOKEN)

# Graceful shutdown
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Bot shutdown manually.")
