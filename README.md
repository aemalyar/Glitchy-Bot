# 🤖 Glitchy Bot — A Fully Automated Valorant Esports & Scrim Management Discord Bot

**Glitchy Bot** is a custom-built Discord bot designed to manage everything for a competitive Valorant community — from esports news and scrims to teams, XP ranks, and tournament automation. Built specifically for the [Glitchy Discord server](https://discord.gg/n8J4UPRwWS), this bot creates an immersive, automated environment where players and organizers can thrive without manual hassle.

---

## 🌟 Key Features

### 📰 Automatic Valorant News
- Scrapes **VLR.gg**, **Liquipedia**, and **Esports.gg**
- Auto-posts breaking Valorant esports headlines in a dedicated `📡︱transmission-log` channel
- Tags `@everyone` with every important update
- Runs every 30 minutes (customizable)

### 🎮 Scrim System
- Scrim queuing logic with **XP-based team balancing**
- Auto-assigns esports-style team names (e.g. `Team Fnatic`, `Team Sentinels`)
- Creates **temporary voice channels** for each team
- Scrim roles are assigned & cleaned up automatically after 15 minutes

### 🧠 AI Assistant
- In-chat conversational assistant
- Switchable AI chat mode
- Can answer questions, moderate, or act as a support bot for your server

### 📊 XP & Rank Progression
- Tracks player participation & experience points
- Automatically assigns server ranks based on XP
- Includes persistent data storage for player stats

### 🏆 Tournament & League System
- Complete support for signups, team registration, bracket generation
- Fully automated tournament flow management
- Match history tracking (ongoing development)

### 🛠️ Server Utilities
- Role management tools
- Event coordination logic
- Smooth onboarding for new players and teams

---

## 📦 Project Structure

```bash
📁 cogs/                # All bot features modularized as Cogs
📁 data/                # JSON files storing XP, team info, scrim logs etc.
📝 main.py              # Bot entry point
📝 .env                 # Environment variables (add manually on Railway)
📝 requirements.txt     # Python dependencies
````

---

## 🚀 Deployment

We recommend **[Railway](https://railway.app)** for free cloud hosting.
Steps:

1. Clone the repo
2. Upload to Railway
3. Add environment variables (`DISCORD_TOKEN` and others)
4. Set your bot’s entry point to `main.py`

Done ✅ Your bot now stays online 24/7.

---

## 🌐 Where It's Being Used

This bot was originally developed for the [Glitchy Discord Server](https://discord.gg/n8J4UPRwWS), where it’s actively tested and maintained.
Join the server to:

* See it in action
* Request new features
* Collaborate or contribute!

---

## 📌 Requirements

* Python 3.11+
* Discord Bot Token
* Railway / Replit / VPS for hosting
* Add the following to `.env`:

  ```env
  DISCORD_TOKEN=your_token_here
  ```

---

## 🤝 Contribute

Feel free to fork, improve, or submit pull requests.
This project is in active development and we welcome community contributions 💡

---

## 📜 License

MIT License

---

## 💬 Contact

Made with ❤️ by [@aemalyar](https://github.com/aemalyar)
For collabs or support, reach out via [Glitchy Server](https://discord.gg/n8J4UPRwWS)

```

