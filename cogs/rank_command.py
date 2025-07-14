import discord
from discord import app_commands
from discord.ext import commands
from cogs.utils import load_xp

class RankCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rank", description="View your level and XP")
    async def rank(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        xp_data = load_xp()
        user = xp_data.get(user_id)

        if not user:
            await interaction.response.send_message("🚫 No XP found. Start chatting to gain XP!", ephemeral=True)
            return

        await interaction.response.send_message(
            f"🔎 <@{user_id}> is **Level {user['level']}** with **{user['xp']} XP**"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(RankCommand(bot))
