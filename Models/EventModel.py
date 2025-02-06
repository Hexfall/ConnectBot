from pathlib import Path
import csv

from Event import create_event

schedule_path = Path(__file__).parent.parent.joinpath('Data/schedule.csv').absolute()

class EventModel:
    def __init__(self):
        self.events = []
    
    def __enter__(self):
        self.__load()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def __load(self):
        if Path(schedule_path).exists():
            with open(schedule_path, 'r') as csvfile:
                self.events = [create_event(*data.split(',')) for data in csvfile.read().strip().split('\n')]
                