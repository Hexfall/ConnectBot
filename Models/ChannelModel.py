import json
from pathlib import Path


channel_file = Path(__file__).parent.parent.joinpath('Data/channels.json')

class ChannelModel:
    def __init__(self):
        self.shift_channel: int|None = None
        self.event_manager_channel: int|None = None
    
    def __enter__(self):
        self.__load()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__save()

    def __load(self):
        if not channel_file.exists():
            return
        with open(channel_file) as f:
            channels: dict[str, str] = json.load(f)
        self.shift_channel = channels.get('shift_channel', None)
        self.event_manager_channel = channels.get('event_manager_channel', None)
    
    def __save(self):
        d = {
            'shift_channel': self.shift_channel,
            'event_manager_channel': self.event_manager_channel,
        }
        with open(channel_file, 'w') as f:
            json.dump(d, f)