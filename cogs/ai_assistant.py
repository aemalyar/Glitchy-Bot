import discord
from discord.ext import commands
from discord import app_commands
import os
import cohere
from cogs.utils import load_json, save_json

# Load Cohere API key from environment
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

CHAT_SETTINGS_FILE = "data/chat_mode.json"

# Ensure the chat mode file exists
if not os.path.exists(CHAT_SETTINGS_FILE):
    save_json(CHAT_SETTINGS_FILE, {"chat_mode": True})


class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_chat_mode_enabled(self):
        settings = load_json(CHAT_SETTINGS_FILE)
        return settings.get("chat_mode", True)

    def toggle_chat_mode(self):
        settings = load_json(CHAT_SETTINGS_FILE)
        current = settings.get("chat_mode", True)
        settings["chat_mode"] = not current
        save_json(CHAT_SETTINGS_FILE, settings)
        return not current

    async def get_ai_response(self, prompt):
        try:
            response = cohere_client.generate(
                model="command-light",
                prompt=f"You are Glitchy, a helpful and chill Discord assistant with a gamer/tech nerd personality.\nUser: {prompt}\nGlitchy:",
                max_tokens=150,
                temperature=0.7
            )
            return response.generations[0].text.strip()
        except Exception as e:
            print(f"❌ AI error: {e}")
            return f"⚠️ Error: {e}"

    @app_commands.command(name="toggle_chat", description="Enable or disable Glitchy's AI chat responses.")
    async def toggle_chat(self, interaction: discord.Interaction):
        new_status = self.toggle_chat_mode()
        status_text = "🟢 Enabled" if new_status else "🔴 Disabled"
        await interaction.response.send_message(f"💬 Chat mode is now: **{status_text}**")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not self.is_chat_mode_enabled():
            return

        if isinstance(message.channel, discord.TextChannel):
            mention = self.bot.user.mention
            if mention in message.content or message.channel.name in ["ai", "chat", "general"]:
                user_msg = message.content.lower()

                # Command suggestions
                suggestions = {
                    "join a team": "/join_team",
                    "create a team": "/create_team",
                    "make a team": "/create_team",
                    "start a scrim": "/scrim_create",
                    "join a scrim": "/scrim_join",
                    "check scrim": "/scrim_status",
                    "cancel scrim": "/scrim_cancel",
                    "see rank": "/rank",
                    "my level": "/rank",
                    "team info": "/team_info"
                }

                for trigger, command in suggestions.items():
                    if trigger in user_msg:
                        await message.channel.send(f"💡 You can use the `{command}` command to do that!")
                        return

                # Fall back to AI response
                prompt = message.content.replace(mention, "").strip()
                if prompt:
                    async with message.channel.typing():
                        reply = await self.get_ai_response(prompt)
                    await message.reply(reply)


async def setup(bot):
    await bot.add_cog(AIAssistant(bot))
