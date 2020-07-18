import boto3
import json

class KinesesFirehose(object):

    def __init__(self, stream_name=None):
        self.stream_name = stream_name
        self.client = boto3.client('firehose')
        self.description = self.client.describe_delivery_stream(DeliveryStreamName=self.stream_name)

    def post(self, payload=None):
        json_payload =  json.dumps(payload)
        json_payload += "\n"

        json_payload_encode = json_payload.encode("utf-8")

        response = self.client.put_record(DeliveryStreamName=self.stream_name, Record={"Data": json_payload_encode})

        response_aws = json.dumps(response, indent=3)
        return response_aws