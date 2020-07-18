class Event:
    def __init__(self, event_name: str=None, metadata: object=None, timestamp_utc: int=None):
        self.event_name = event_name
        self.metadata = metadata
        self.timestamp_utc = timestamp_utc