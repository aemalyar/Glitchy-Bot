import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from cogs.utils import load_scrims, save_scrims, load_xp

PRO_TEAMS = [
    "Fnatic", "Sentinels", "Gen.G", "Paper Rex", "Team Liquid",
    "LOUD", "DRX", "NAVI", "T1", "100 Thieves", "ZETA DIVISION", "NRG"
]

class ScrimSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="scrim_create", description="Create a new scrim")
    @app_commands.describe(required_players="Total players required (e.g., 10)")
    async def scrim_create(self, interaction: discord.Interaction, required_players: int):
        user_id = str(interaction.user.id)
        scrims = load_scrims()
        if scrims.get("active"):
            await interaction.response.send_message("⚠️ A scrim is already active.", ephemeral=True)
            return
        scrims["active"] = {
            "leader": user_id,
            "players_needed": required_players,
            "joined": [user_id]
        }
        save_scrims(scrims)
        await interaction.response.send_message(
            f"📡 Scrim created by <@{user_id}>. Needed: `{required_players}` players. Use `/scrim_join` to enter."
        )

    @app_commands.command(name="scrim_join", description="Join the active scrim")
    async def scrim_join(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        scrims = load_scrims()
        active = scrims.get("active")
        if not active:
            await interaction.response.send_message("❌ No scrim is currently active.", ephemeral=True)
            return
        if user_id in active["joined"]:
            await interaction.response.send_message("⚠️ You've already joined the scrim.", ephemeral=True)
            return
        active["joined"].append(user_id)

        if len(active["joined"]) >= active["players_needed"]:
            scrims["completed"] = scrims.pop("active")
            save_scrims(scrims)

            # Balance teams by XP
            xp_data = load_xp()
            players = scrims["completed"]["joined"]
            players_with_xp = [(p, xp_data.get(str(p), {}).get("xp", 0)) for p in players]
            players_with_xp.sort(key=lambda x: x[1], reverse=True)

            team1, team2 = [], []
            team1_xp = team2_xp = 0

            for p, xp in players_with_xp:
                if team1_xp <= team2_xp:
                    team1.append(p)
                    team1_xp += xp
                else:
                    team2.append(p)
                    team2_xp += xp

            team_names = random.sample(PRO_TEAMS, 2)
            team1_name, team2_name = team_names

            # Create temporary VCs
            category = discord.utils.get(interaction.guild.categories, name="Scrims")
            if not category:
                category = await interaction.guild.create_category("Scrims")

            vc1 = await category.create_voice_channel(f"{team1_name} VC")
            vc2 = await category.create_voice_channel(f"{team2_name} VC")

            # Move members into their team VCs
            for uid in team1:
                member = interaction.guild.get_member(int(uid))
                if member and member.voice:
                    await member.move_to(vc1)

            for uid in team2:
                member = interaction.guild.get_member(int(uid))
                if member and member.voice:
                    await member.move_to(vc2)

            # Schedule deletion after 15 minutes
            async def delete_vcs():
                await asyncio.sleep(900)  # 15 minutes
                await vc1.delete()
                await vc2.delete()

            self.bot.loop.create_task(delete_vcs())

            # Send embed result
            embed = discord.Embed(title="🔥 Scrim Teams Ready!", color=0x00ffcc)
            embed.add_field(name=f"🏷️ Team {team1_name}", value="\n".join([f"<@{uid}>" for uid in team1]), inline=True)
            embed.add_field(name=f"🏷️ Team {team2_name}", value="\n".join([f"<@{uid}>" for uid in team2]), inline=True)
            embed.set_footer(text="Balanced based on XP ⚖️ | Temp VCs auto-delete in 15 min ⏱️")

            await interaction.response.send_message(embed=embed)

        else:
            save_scrims(scrims)
            needed = active["players_needed"] - len(active["joined"])
            await interaction.response.send_message(f"✅ You've joined. `{needed}` more needed.")

    @app_commands.command(name="scrim_status", description="Check scrim join status")
    async def scrim_status(self, interaction: discord.Interaction):
        scrims = load_scrims()
        active = scrims.get("active")
        if not active:
            await interaction.response.send_message("📭 No active scrim.")
            return
        players = [f"<@{uid}>" for uid in active["joined"]]
        needed = active["players_needed"] - len(active["joined"])
        await interaction.response.send_message(
            f"🎮 **Active Scrim**\n"
            f"👑 Leader: <@{active['leader']}>\n"
            f"👥 Players ({len(players)}/{active['players_needed']}): {', '.join(players)}\n"
            f"🔄 Waiting for `{needed}` more..."
        )

    @app_commands.command(name="scrim_cancel", description="Cancel current scrim (Leader only)")
    async def scrim_cancel(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        scrims = load_scrims()
        active = scrims.get("active")
        if not active:
            await interaction.response.send_message("🚫 No scrim to cancel.", ephemeral=True)
            return
        if active["leader"] != user_id:
            await interaction.response.send_message("❌ Only the scrim leader can cancel.", ephemeral=True)
            return
        scrims.pop("active")
        save_scrims(scrims)
        await interaction.response.send_message("🗑️ Scrim canceled by leader.")

async def setup(bot):
    await bot.add_cog(ScrimSystem(bot))
