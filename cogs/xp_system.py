import discord
from discord.ext import commands
import random
from cogs.utils import load_xp, save_xp, calculate_level

LEVEL_ROLES = {
    5: "📂︱Data Drifter",
    10: "🔍︱Code Tracer",
    15: "🕶︱Kernel Crasher",
    20: "⚡︱Glitch Manifest",
    30: "💀︱System Ghost"
}

last_xp = {}

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        xp_data = load_xp()
        user_xp = xp_data.get(user_id, {"xp": 0, "level": 0})
        old_level = user_xp["level"]

        # Cooldown: 60 seconds
        if user_id in last_xp and (discord.utils.utcnow() - last_xp[user_id]).total_seconds() < 60:
            return
        last_xp[user_id] = discord.utils.utcnow()

        earned = random.randint(5, 15)
        user_xp["xp"] += earned
        new_level = calculate_level(user_xp["xp"])

        if new_level > old_level:
            user_xp["level"] = new_level
            await message.channel.send(f"✨ <@{user_id}> leveled up to **Level {new_level}**!")
            role_name = LEVEL_ROLES.get(new_level)
            if role_name:
                role = discord.utils.get(message.guild.roles, name=role_name)
                if role:
                    await message.author.add_roles(role)
                    await message.channel.send(f"🎖️ <@{user_id}> unlocked the `{role_name}` role!")

        xp_data[user_id] = user_xp
        save_xp(xp_data)

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))
