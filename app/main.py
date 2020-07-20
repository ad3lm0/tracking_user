from flask import Flask, request, jsonify
from marshmallow import ValidationError

from cloud_aws.firehose_stream import KinesesFirehose
from cloud_aws.connection_strings import AWSConnectionStrings
from cloud_aws.s3_json_concat import concat_json

from model.track import TrackBody, TrackBodySchema
from model.alias import AliasBody, AliasBodySchema
from model.profile import ProfileBody, ProfileBodySchema
from model.event import EventBody, EventSchema

from multiprocessing import Process, Value
import time

app = Flask(__name__)

aws_connections = AWSConnectionStrings()

track_stream = KinesesFirehose(stream_name=aws_connections.track_stream_name)
alias_stream = KinesesFirehose(stream_name=aws_connections.alias_stream_name)
profile_stream = KinesesFirehose(stream_name=aws_connections.profile_stream_name)


def s3_concat():
    starttime = time.time()
    while True:
        # alias
        time.sleep(61.0 - ((time.time() - starttime) % 61.0))
        concat_json(
            aws_connections.bucket,
            aws_connections.alias_path_to_concat,
            aws_connections.alias_concatenated_file,
        )
        # track
        concat_json(
            aws_connections.bucket,
            aws_connections.track_path_to_concat,
            aws_connections.track_concatenated_file,
        )
        # profile
        concat_json(
            aws_connections.bucket,
            aws_connections.profile_path_to_concat,
            aws_connections.profile_concatenated_file,
        )


@app.route("/", methods=["GET"])
def index():
    return "Hello World!", 200


@app.route("/track/", methods=["POST"])
def track_handler():
    json_request = request.get_json()
    if "userId" not in json_request:
        raise TypeError("'userId' is a required field for this method")

    if "events" not in json_request:
        raise TypeError("'events' is a required field for this method")
    try:
        tracked_user = json_request["userId"]
        tracked_events = []
        for events in json_request["events"]:
            event = EventBody(**events)
            tracked_events.append(event)

        track = TrackBody(userId=tracked_user, events=tracked_events)
        track_schema = TrackBodySchema()
        schema_check = track_schema.dump(track)
        result = track_stream.post(request.get_json())
        return result

    except TypeError as err:
        return jsonify(str(err))


@app.route("/alias/", methods=["POST"])
def alias_handler():
    try:
        alias = AliasBody(**request.get_json())
        alias_schema = AliasBodySchema()
        schema_check = alias_schema.dump(alias)

        result = alias_stream.post(request.get_json())
        return result

    except TypeError as err:
        return jsonify(str(err)), 400


@app.route("/profile/", methods=["POST"])
def profile_handler():
    try:
        profile = ProfileBody(**request.get_json())
        profile_schema = ProfileBodySchema()
        schema_check = profile_schema.dump(profile)

        result = profile_stream.post(request.get_json())
        return result

    except TypeError as err:
        return jsonify(str(err)), 400


if __name__ == "__main__":
    recording_on = Value("b", True)
    p = Process(target=s3_concat)
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()
