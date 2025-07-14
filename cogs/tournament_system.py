from discord.ext import commands

class TournamentSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add tournament-related commands here later

async def setup(bot: commands.Bot):
    await bot.add_cog(TournamentSystem(bot))
