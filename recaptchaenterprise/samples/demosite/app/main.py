from flask import Flask

import urls

app = Flask(__name__)

app.add_url_rule(rule="/", methods=["GET"], view_func=urls.login)
app.add_url_rule(rule="/signup", methods=["GET"], view_func=urls.signup)
app.add_url_rule(rule="/create_assessment", methods=["POST"], view_func=urls.create_assessment)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
