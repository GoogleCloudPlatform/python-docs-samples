CLOUD_PROJECT_ID = 'YOUR_PROJECT_ID'
BACKEND_SERVICE_ID = 'YOUR_BACKEND_SERVICE_ID'

from flask import Flask
from flask import request

import validate_jwt

app = Flask(__name__)

@app.route('/')
def root():
    jwt = request.headers.get('x-goog-iap-jwt-assertion')
    if jwt is None:
        return 'Unauthorized request.', 401
    user_id, user_email, error_str = validate_jwt.validate_iap_jwt_from_compute_engine(
            jwt, CLOUD_PROJECT_ID, BACKEND_SERVICE_ID)
    if error_str:
        return "Error: %s" % error_str
    else:
        return "Hi, %s" % user_email

@app.route('/healthz')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
