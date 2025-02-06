import discord
import asyncio

from pathlib import Path
from ConnectBot import ConnectBot

token_path = Path(__file__).parent.joinpath("token.txt").absolute()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def main() -> None:
    bot = ConnectBot(intents=intents)
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            bot.start(get_token())
        )
        tg.create_task(
            bot.event_manager_cycle()
        )
        tg.create_task(
            bot.shift_cycle()
        )
        

def get_token() -> str:
    with open(token_path, 'r') as file:
        return file.read().strip()
        

if __name__ == "__main__":
    asyncio.run(main())
