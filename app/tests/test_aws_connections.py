from app.cloud_aws.firehose_stream import KinesesFirehose
from app.cloud_aws.connection_strings import AWSConnectionStrings
import boto3
import json

aws_connections = AWSConnectionStrings()
aws_client = boto3.client("firehose")


def test_trackStream():
    response = aws_client.describe_delivery_stream(
        DeliveryStreamName=aws_connections.track_stream_name
    )

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert (
        response["DeliveryStreamDescription"]["DeliveryStreamName"]
        == aws_connections.track_stream_name
    )


def test_aliasStream():
    response = aws_client.describe_delivery_stream(
        DeliveryStreamName=aws_connections.alias_stream_name
    )

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert (
        response["DeliveryStreamDescription"]["DeliveryStreamName"]
        == aws_connections.alias_stream_name
    )


def test_profileStream():
    response = aws_client.describe_delivery_stream(
        DeliveryStreamName=aws_connections.profile_stream_name
    )

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert (
        response["DeliveryStreamDescription"]["DeliveryStreamName"]
        == aws_connections.profile_stream_name
    )


def test_firehosePutConnection():
    alias_stream = KinesesFirehose(stream_name=aws_connections.alias_stream_name)
    response = json.loads(alias_stream.post(""))

    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
