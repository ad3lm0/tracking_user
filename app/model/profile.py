class Profile:
    def __init__(self, user_id: str=None, attributes: object=None, timestamp_utc: int=None):
        self.user_id = user_id
        self.attributes = attributes
        self.timestamp_utc = timestamp_utc