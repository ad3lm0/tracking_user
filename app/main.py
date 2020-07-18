from flask import Flask, request, jsonify
from firehose_stream import KinesesFirehose
from model.track import Track
from model.alias import Alias
from model.profile import Profile

app = Flask(__name__)

track_stream = KinesesFirehose(stream_name="firehose-trackevents-to-s3")
alias_stream = KinesesFirehose(stream_name="firehose-alias-to-s3")
profile_stream = KinesesFirehose(stream_name="firehose-profile-to-s3")


@app.route('/', methods=['GET'])
def index():
    return "Hello World!", 200


@app.route('/track/', methods=['POST'])
def track_handler(track): 
    result = track_stream.post(request.get_json())
    return result


@app.route('/alias/', methods=['POST'])
def alias_handler():
    result = alias_stream.post(request.get_json())    
    return result


@app.route('/profile/', methods=['POST'])
def profile_handler():
    result = profile_stream.post(request.get_json())
    return result
    

if __name__ == '__main__':
    app.run(debug=True)