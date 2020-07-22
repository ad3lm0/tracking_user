from s3_concat import S3Concat
import time
import boto3

s3client = boto3.client("s3")


def data_exists(bucket, check_path):
    response = s3client.list_objects_v2(bucket, check_path)
    return response["KeyCount"] > 0


def concat_json(bucket, path_to_concat, concatenated_file, min_file_size=None):

    if data_exists(bucket, path_to_concat):
        job = S3Concat(
            bucket, concatenated_file, min_file_size, content_type="application/json",
        )
        job.add_files(path_to_concat)
        job.concat(small_parts_threads=4)
