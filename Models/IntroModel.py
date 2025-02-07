import json
from pathlib import Path
from random import choice, seed


intro_file = Path(__file__).parent.parent.joinpath("Data/intros.json")

class IntroModel:
    def __init__(self):
        self.event_intros = ["Tomorrow is {0} and"]
        self.primary_intros = ["{0} is on games and"]
        self.secondary_intros = ["{0} is on snack duty."]
    
    def __enter__(self):
        self.__load()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __load(self):
        if not intro_file.exists():
            return
        
        with open(intro_file) as f:
            d = json.load(f)
        self.event_intros = d.get("event_intros", self.event_intros)
        self.primary_intros = d.get("primary_intros", self.primary_intros)
        self.secondary_intros = d.get("secondary_intros", self.secondary_intros)
    
    def get_event_intro(self, event_name):
        return choice(self.event_intros).format(event_name)
    
    def get_primary_intro(self, name):
        return choice(self.primary_intros).format(name)
    
    def get_secondary_intro(self, name):
        return choice(self.secondary_intros).format(name)
        
