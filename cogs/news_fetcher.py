import discord
from discord.ext import commands, tasks
import aiohttp
from bs4 import BeautifulSoup
import asyncio

TRANSMISSION_CHANNEL_NAME = "📡︱transmission-log"

class NewsFetcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sent_articles = set()
        self.vlr_url = "https://www.vlr.gg/news"
        self.liquipedia_url = "https://liquipedia.net/valorant"
        self.esports_url = "https://esports.gg/news/valorant/"
        self.post_news.start()

    async def fetch_vlr_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.vlr_url) as resp:
                html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".wf-card")

        news = []
        for card in cards[:5]:
            title_tag = card.select_one(".wf-title")
            link_tag = card.select_one("a")
            if title_tag and link_tag:
                title = title_tag.text.strip()
                url = "https://www.vlr.gg" + link_tag["href"]
                if url not in self.sent_articles:
                    news.append((title, url))
        return news

    async def fetch_liquipedia_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.liquipedia_url) as resp:
                html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")

        news_items = []
        news_box = soup.find("div", class_="mpbox")
        if news_box:
            for li in news_box.find_all("li"):
                text = li.get_text(strip=True)
                link_tag = li.find("a", href=True)
                if text and link_tag:
                    full_link = f"https://liquipedia.net{link_tag['href']}"
                    if full_link not in self.sent_articles:
                        news_items.append((text, full_link))
        return news_items[:5]

    async def fetch_esports_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.esports_url) as resp:
                html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        news_items = []

        articles = soup.select("article.card")
        for article in articles[:5]:
            title_tag = article.select_one("h3.card-title")
            link_tag = article.find("a", href=True)
            if title_tag and link_tag:
                title = title_tag.text.strip()
                url = link_tag["href"]
                if url not in self.sent_articles:
                    news_items.append((title, url))
        return news_items

    @tasks.loop(minutes=30)  # ⏱️ Production interval (change if needed)
    async def post_news(self):
        await self.bot.wait_until_ready()
        channel = discord.utils.get(self.bot.get_all_channels(), name=TRANSMISSION_CHANNEL_NAME)
        if not channel:
            print(f"❌ Could not find channel: {TRANSMISSION_CHANNEL_NAME}")
            return

        vlr_news = await self.fetch_vlr_news()
        liqui_news = await self.fetch_liquipedia_news()
        esports_news = await self.fetch_esports_news()
        combined = vlr_news + liqui_news + esports_news

        for title, url in combined:
            if url not in self.sent_articles:
                embed = discord.Embed(
                    title="📰 Valorant Esports Update",
                    description=title,
                    url=url,
                    color=discord.Color.blue()
                )
                await channel.send(content="@everyone", embed=embed)
                self.sent_articles.add(url)
                await asyncio.sleep(3)

    @post_news.before_loop
    async def before_news(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(NewsFetcher(bot))
