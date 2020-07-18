import util

class Alias:
    def __init__(self, new_user_id: str=None, original_user_id: str=None, timestamp_utc: int=None):
        self.new_user_id = new_user_id
        self.original_user_id = original_user_id
        self.timestamp_utc = timestamp_utc

    @classmethod
    def from_dict(cls, dikt) -> 'Alias':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The alias of this Alias.
        :rtype: Alias
        """
        return util.deserialize_model(dikt, cls)