from datetime import datetime, timedelta


class Event:
    def __init__(self, weekday: str, date: datetime, title: str, room: str, primary: str, secondary: str) -> None:
        self.weekday = weekday
        self.date = date
        self.title = title
        self.room = room
        self.primary = primary
        self.secondary = secondary
    
    def __str__(self) -> str:
        return f"{self.weekday:>9}   {self.date.strftime('%m/%d'):>5} {self.title:>10}   {self.room:>6}"

def create_event(weekday: str, date: str, title: str, room: str, primary: str, secondary: str) -> Event:
    d = datetime.strptime(date + "/" + str(datetime.now().year), "%d/%m/%Y")
    return Event(weekday, d, title, room, primary, secondary)

def events_in_range(events: list[Event], start: datetime, end: datetime) -> list[Event]:
    return [e for e in events if start <= e.date < end]

def next_sunday() -> datetime:
    d = datetime.today() + timedelta(days=1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return d