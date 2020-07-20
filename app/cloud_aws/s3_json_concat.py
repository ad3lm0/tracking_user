from s3_concat import S3Concat
import time

bucket = "firehose-tracking-raw"


def concat_alias():
    alias_path_to_concat = "success/alias/batch/"
    alias_concatenated_file = "success/alias/alias.json"
    concat_json(alias_path_to_concat, alias_concatenated_file)


def concat_trackevents():
    alias_path_to_concat = "success/track-events/batch"
    alias_concatenated_file = "success/track-events/track-events.json"
    concat_json(alias_path_to_concat, alias_concatenated_file)


def concat_profile():
    alias_path_to_concat = "success/profile/batch"
    alias_concatenated_file = "success/profile/profile.json"
    concat_json(alias_path_to_concat, alias_concatenated_file)


def concat_json(path_to_concat, concatenated_file, min_file_size=None):
    try:
        job = S3Concat(
            bucket, concatenated_file, min_file_size, content_type="application/json",
        )
        job.add_files(path_to_concat)
        job.concat(small_parts_threads=4)
    except KeyError:
        pass
