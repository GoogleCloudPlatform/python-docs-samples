from receive import receive_authorized_get_request


from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def main():
    return receive_authorized_get_request(request)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
