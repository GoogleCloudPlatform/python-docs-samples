import os
import json
import base64

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return 'GET Success!\n', 200

@app.route('/', methods=['POST'])
def event_handler():
	body = json.loads(request.json)

	if 'message' not in body or 'data' not in body['message']:
		msg = 'invalid Pub/Sub message format'
		return {'err': msg}, 400

	if 'ce-id' not in request.headers:
		msg = 'missing ce-id field in Pub/Sub headers'
		return {'err': msg}, 400

	base64_message = body['message']['data']
	name = base64.b64decode(base64_message).decode()
	return {'message': 'Hello {0}! ID: {1}'.format(name, request.headers['ce-id'])}, 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
