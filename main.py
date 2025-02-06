import discord

from pathlib import Path
from ConnectBot import ConnectBot

token_path = Path(__file__).parent.joinpath("token.txt").absolute()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


def main() -> None:
    bot = ConnectBot(intents)
    bot.run(get_token())

def get_token() -> str:
    with open(token_path, 'r') as file:
        return file.read().strip()

if __name__ == "__main__":
    main()
