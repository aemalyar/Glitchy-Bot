import discord
from discord import app_commands
from discord.ext import commands
from cogs.utils import load_teams, save_teams

class TeamSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create_team", description="Create a new team")
    @app_commands.describe(team_name="The name of your team")
    async def create_team(self, interaction: discord.Interaction, team_name: str):
        user_id = str(interaction.user.id)
        teams = load_teams()
        if any(user_id in t["members"] for t in teams.values()):
            await interaction.response.send_message("⚠️ You're already in a team.", ephemeral=True)
            return
        if team_name in teams:
            await interaction.response.send_message("🚫 Team already exists.", ephemeral=True)
            return
        teams[team_name] = {"leader": user_id, "members": [user_id]}
        save_teams(teams)
        await interaction.response.send_message(f"✅ Team `{team_name}` created. You are the leader.")

    @app_commands.command(name="join_team", description="Join an existing team")
    @app_commands.describe(team_name="Name of the team you want to join")
    async def join_team(self, interaction: discord.Interaction, team_name: str):
        user_id = str(interaction.user.id)
        teams = load_teams()
        if any(user_id in t["members"] for t in teams.values()):
            await interaction.response.send_message("⚠️ You're already in a team.", ephemeral=True)
            return
        if team_name not in teams:
            await interaction.response.send_message("🚫 Team not found.", ephemeral=True)
            return
        teams[team_name]["members"].append(user_id)
        save_teams(teams)
        await interaction.response.send_message(f"✅ You’ve joined `{team_name}`.")

    @app_commands.command(name="leave_team", description="Leave your current team")
    async def leave_team(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        teams = load_teams()
        for name, team in teams.items():
            if user_id in team["members"]:
                team["members"].remove(user_id)
                if user_id == team["leader"]:
                    del teams[name]
                    save_teams(teams)
                    await interaction.response.send_message(f"💀 You were the leader. Team `{name}` disbanded.")
                    return
                save_teams(teams)
                await interaction.response.send_message(f"📤 You’ve left the team `{name}`.")
                return
        await interaction.response.send_message("🤷 You're not in any team.", ephemeral=True)

    @app_commands.command(name="team_info", description="View team info by name")
    @app_commands.describe(team_name="Name of the team to view")
    async def team_info(self, interaction: discord.Interaction, team_name: str):
        teams = load_teams()
        team = teams.get(team_name)
        if not team:
            await interaction.response.send_message("🚫 Team not found.", ephemeral=True)
            return
        members = [f"<@{uid}>" for uid in team["members"]]
        await interaction.response.send_message(
            f"📂 **Team:** `{team_name}`\n"
            f"👑 **Leader:** <@{team['leader']}>\n"
            f"🧑‍💻 **Members** ({len(members)}): {', '.join(members)}"
        )

    # Register all slash commands for syncing
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.tree.add_command(self.create_team)
        self.bot.tree.add_command(self.join_team)
        self.bot.tree.add_command(self.leave_team)
        self.bot.tree.add_command(self.team_info)

async def setup(bot):
    await bot.add_cog(TeamSystem(bot))
