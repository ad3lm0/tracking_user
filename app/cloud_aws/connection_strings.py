class AWSConnectionStrings(object):
    def __init__(self):
        self.track_stream_name = "firehose-track-stream"
        self.track_path_to_concat = "success/track/batch/"
        self.track_concatenated_file = "success/track/track-events.json"

        self.alias_stream_name = "firehose-alias-stream"
        self.alias_path_to_concat = "success/alias/batch/"
        self.alias_concatenated_file = "success/alias/alias.json"

        self.profile_stream_name = "firehose-profile-stream"
        self.profile_path_to_concat = "success/profile/batch/"
        self.profile_concatenated_file = "success/profile/profile.json"

        self.bucket = "behavior-tracking-user-bucket"
