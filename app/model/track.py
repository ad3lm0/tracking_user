from typing import List
from model.event import Event

class Track:
    def __init__(self, user_id: str=None, events: List[Event]=None):
        self.user_id = user_id
        self.events = events