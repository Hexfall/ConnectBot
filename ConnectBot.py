import asyncio
from datetime import timedelta, datetime
from functools import lru_cache
from typing import Optional

import discord

from Models.ChannelModel import ChannelModel
from Models.EventModel import EventModel
from Models.IntroModel import IntroModel
from Event import events_in_range, next_sunday, Event

PREFIX = "!connect"
MINUTE = 60
HOUR = MINUTE * 60
DAY = 24 * HOUR

class ConnectBot(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.shift_channel: discord.TextChannel | None = None
        self.event_manager_channel: discord.TextChannel | None = None
    
    def __find_channels(self) -> None:
        with ChannelModel() as model:
            for channel in self.get_all_channels():
                if channel.id == model.shift_channel:
                    self.shift_channel = channel
                    print("Found shift channel")
                if channel.id == model.event_manager_channel:
                    self.event_manager_channel = channel
                    print("Found event manager channel")

    def set_event_manager_channel(self, channel: discord.TextChannel):
        self.event_manager_channel = channel
        with ChannelModel() as model:
            model.event_manager_channel = channel.id
        print(f"Set event manager channel as {channel.name} in {channel.guild}")

    def set_shift_channel(self, channel: discord.TextChannel):
        self.shift_channel = channel
        with ChannelModel() as model:
            model.shift_channel = channel.id
        print(f"Set shift channel as {channel.name} in {channel.guild}")
    
    async def on_ready(self):
        print(f'Logged in as: {self.user.name} {self.user.id}')
        self.__find_channels()
    
    async def on_message(self, message: discord.message.Message):
        if message.author == self.user:
            return
        
        if message.content.startswith(PREFIX):
            text = message.content[len(PREFIX):].strip()
            await self.parse_message(message, text)

    async def parse_message(self, message: discord.message.Message, text: str):
        print(f'Parsing message: {message.content}')
        if text.startswith("help"):
            pass
        elif text.startswith("bind"):
            role = None
            for r in message.guild.roles:
                if r.name == "President":
                    role = r
            if role is None or not role in message.author.roles:
                await message.reply("Only the president can use this command.")
                return
            if text.endswith("shift_channel"):
                self.set_shift_channel(message.channel)
                await message.add_reaction("👍")
            elif text.endswith("event_manager_channel"):
                self.set_event_manager_channel(message.channel)
                await message.add_reaction("👍")

    async def event_manager_cycle(self) -> None:
        sleep_until = next_sunday()
        sleep_until = sleep_until.replace(hour=16, minute=0, second=0, microsecond=0)
        sleep_until += timedelta(days=1)
        #sleep_until = datetime.strptime("2025-02-07 00:35", "%Y-%m-%d %H:%M") # For debugging
        while True:
            await asyncio.sleep((sleep_until - datetime.now()).total_seconds())
            sleep_until += timedelta(days=7)
            print(f"Firing Event Manager cycle.")

            if not self.is_ready() or self.event_manager_channel is None:
                return
            
            em_role = await self.get_role_by_name("Event Manager")
            if em_role is None:
                continue

            with EventModel() as model:
                events = events_in_range(
                    model.events,
                    next_sunday(),
                    next_sunday() + timedelta(days=7)
                )
            
            if len(events) == 0:
                continue
            
            await self.event_manager_channel.send(
                f"{em_role.mention} there are {len(events)} event(s) next week:" +
                "\n```" +
                "\n".join([str(e) for e in events]) +
                "```"
            )


    async def shift_cycle(self) -> None:
        sleep_until = datetime.now()
        sleep_until = sleep_until.replace(hour=16, minute=0, second=0, microsecond=0)
        if sleep_until < datetime.now():
            sleep_until += timedelta(days=1)
        #sleep_until = datetime.strptime("2025-02-07 01:19", "%Y-%m-%d %H:%M") # For debugging
        while True:
            await asyncio.sleep((sleep_until - datetime.now()).total_seconds())
            sleep_until += timedelta(days=1)
            print(f"Firing Shift cycle.")
            
            with EventModel() as model:
                events = events_in_range(model.events, datetime.now(), datetime.now() + timedelta(days=1))
            if self.is_ready() and self.shift_channel is not None:
                for e in events:
                    with IntroModel() as model:
                        intro = model.get_event_intro(e.title)
                        primary = model.get_primary_intro(await self.get_crew_member(e.primary))
                        secondary = model.get_secondary_intro(await self.get_crew_member(e.secondary))
                    await self.shift_channel.send(f"{intro} {primary} {secondary}")
    
    async def get_crew_member(self, name: str) -> str:
        crew_role = self.get_role_by_name("Crew")
        if crew_role is None:
            return name
        
        for u in self.shift_channel.guild.members:
            if not crew_role in u.roles:
                continue
            alias = u.nick.lower() if u.nick is not None else u.name.lower()
            for n in name.lower().split():
                if not n in alias:
                    break
            else:
                return u.mention
        
        return name
    
    @lru_cache(maxsize=3)
    async def get_role_by_name(self, name: str) -> Optional[discord.Role]:
        for r in self.shift_channel.guild.roles:
            if r.name == name:
                return r
        return None
    