from flask import flash, Flask, Markup, redirect, render_template, request
from sparkpost import SparkPost
from sparkpost.exceptions import SparkPostAPIException

app = Flask(__name__)
app.secret_key = 'Sshhh. This is a secret!'

sp = SparkPost()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    recipient = request.form.get('email')
    try:
        sp.transmissions.send(
            use_sandbox=True,
            from_email='python-appengine@sparkpostbox.com',
            recipients=[recipient],
            subject='Hello From Google App Engine!',
            html='<h1>Google App Engine + Python + SparkPost = Epic!</h1>'
        )
    except SparkPostAPIException as e:
        errors = e.response.json()['errors']
        for err in errors:
            msg = err.get('message')
            desc = err.get('description')
            flash(Markup('<strong>{}</strong>: {}'.format(msg, desc)))
            return render_template('index.html', err=True)
    flash('Email sent!')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
