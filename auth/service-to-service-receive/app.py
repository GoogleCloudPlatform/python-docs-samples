from flask import Flask, request

from receive import receive_authorized_get_request

app = Flask(__name__)


@app.route("/")
def main():
    return receive_authorized_get_request(request)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
