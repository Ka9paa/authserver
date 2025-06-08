import os
import discord
import aiohttp
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from pathlib import Path

# Load .env from current directory
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Use variable names, not actual values
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AUTH_HEADER = os.getenv("AUTH_HEADER")
BACKEND_URL = os.getenv("BACKEND_URL")

print(f"DEBUG: DISCORD_TOKEN is {DISCORD_TOKEN is not None}")  # Should print True

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # For slash commands

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await tree.sync()

@tree.command(name="generate", description="Generates a new license key and DMs it to you.")
async def generate(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_URL}/api/generate",
                headers={"Authorization": AUTH_HEADER}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    key = data.get("key")
                    if key:
                        await interaction.user.send(f"🔑 Your license key: `{key}`")
                        await interaction.followup.send("✅ Key sent! Check your DMs.", ephemeral=True)
                    else:
                        await interaction.followup.send("❌ No key received from backend.", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Error generating key. Try again later.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send("❌ An error occurred.", ephemeral=True)
        print(f"Error in generate command: {e}")

bot.run(DISCORD_TOKEN)
