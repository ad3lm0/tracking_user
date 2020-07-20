from s3_concat import S3Concat
import time


def concat_json(bucket, path_to_concat, concatenated_file, min_file_size=None):
    try:
        job = S3Concat(
            bucket, concatenated_file, min_file_size, content_type="application/json",
        )
        job.add_files(path_to_concat)
        job.concat(small_parts_threads=4)
    except KeyError:
        pass
