from flask import Flask, request, jsonify
from firehose_stream import KinesesFirehose
from model.track import TrackBody, TrackBodySchema
from model.alias import AliasBody, AliasBodySchema
from model.profile import ProfileBody, ProfileBodySchema
from marshmallow import ValidationError

app = Flask(__name__)

track_stream = KinesesFirehose(stream_name="firehose-trackevents-to-s3")
alias_stream = KinesesFirehose(stream_name="firehose-alias-to-s3")
profile_stream = KinesesFirehose(stream_name="firehose-profile-to-s3")


@app.route("/", methods=["GET"])
def index():
    return "Hello World!", 200


@app.route("/track/", methods=["POST"])
def track_handler(track):
    try:
        track = TrackBody(**request.get_json())
        track_schema = TrackBodySchema
        schema_check = track_schema.dump(track)
        result = track_stream.post(request.get_json())
        return result

    except TypeError as err:
        return jsonify(str(err)), 400

    except ValidationError as err:
        return jsonify(err.messages), 400


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
    except ValidationError as err:
        return jsonify(err.messages), 400


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
    except ValidationError as err:
        return jsonify(err.messages), 400


if __name__ == "__main__":
    app.run(debug=True)
