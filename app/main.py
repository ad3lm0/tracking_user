from flask import Flask, request, jsonify
from marshmallow import ValidationError

from cloud_aws.firehose_stream import KinesesFirehose
import cloud_aws.s3_json_concat as s3_conc

from model.track import TrackBody, TrackBodySchema
from model.alias import AliasBody, AliasBodySchema
from model.profile import ProfileBody, ProfileBodySchema
from model.event import EventBody, EventSchema

from multiprocessing import Process, Value
import time

app = Flask(__name__)

track_stream = KinesesFirehose(stream_name="firehose-trackevents-to-s3")
alias_stream = KinesesFirehose(stream_name="firehose-alias-to-s3")
profile_stream = KinesesFirehose(stream_name="firehose-profile-to-s3")


def s3_concat():
    starttime = time.time()
    while True:
        time.sleep(61.0 - ((time.time() - starttime) % 61.0))
        s3_conc.concat_trackevents()
        s3_conc.concat_alias()
        s3_conc.concat_profile()


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
    # p = Process(target=s3_concat)
    # p.start()
    app.run(debug=True, use_reloader=False)
    # p.join()
