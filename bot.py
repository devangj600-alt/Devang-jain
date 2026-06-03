import asyncio
import os
import aiohttp
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

class OwoBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv("BOT_TOKEN")
        self.get_owos.start()
    
    @tasks.loop(minutes=10)
    async def get_owos(self):
        """Get Owos every 10 minutes"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://owo-bot-api.vercel.app/owo",
                    params={"token": self.token}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"Got {data['owos']} Owos!")
                    else:
                        print(f"Failed to get Owos: {response.status}")
        except Exception as e:
            print(f"Error fetching Owos: {e}")
    
    @get_owos.before_loop
    async def before_get_owos(self):
        await self.bot.wait_until_ready()

async def main():
    bot = commands.Bot(command_prefix="!")
    
    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready!")
    
    await bot.add_cog(OwoBot(bot))
    await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
