from flask import Flask, render_template, session, g, url_for, request, redirect, json
from flask_sqlalchemy import SQLAlchemy
import os
from json_files import day1, day2

app = Flask(__name__, static_folder='assets')
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

message = ''


class users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    pin = db.Column(db.Unicode)
    token = db.Column(db.Unicode)

    def __init__(self, name, email, pin, token):
        self.name = name
        self.email = email
        self.pin = pin
        self.token = token

    def __repr__(self):
        return 'User' + str(self.id)


@app.route("/")
def main():
    if g.user:
        return redirect(url_for('live'))
    return redirect(url_for('login'))


@app.route("/games")
def games():
    if g.user:
        return render_template('games/index.html')
    return redirect(url_for('login'))


@app.route("/events")
def events():
    if g.user:
        return render_template('events.html')
    return redirect(url_for('login'))


@app.route("/tutorials/<string:item>")
def tutorials(item):
    if g.user:
        if item == 'Photoshop':
            return render_template('essentials.htm')
        if item == 'XD':
            return render_template('XD.html')
        if item == 'Shell':
            return redirect('../../assets/wslbash.html')
        if item == 'chatbots':
            return render_template('chatbot.html')
        if item == 'Ai':
            return render_template('more.html')
        if item == 'imagine':
            return render_template('more.html')
        if item == 'solidworks':
            return render_template('more.html')
        if item == 'hacking':
            return render_template('cyberrange.htm')
    return redirect(url_for("login"))

@app.route("/tutorials")
def tutorial():
    if g.user:
        return render_template('tutorials.html')
    return render_template('login.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('live'))
    global message
    if request.method == 'POST':
        session.pop('user', None)
        _uname = request.form['username']
        _pass = request.form['password']
        # Not found
        if users.query.filter_by(email=_uname).first() == None and users.query.filter_by(name=_uname).first() == None:
            message = 'No'
            return render_template('login.html', message=message)
        # Matches
        if users.query.filter_by(name=_uname).first() != None:
            if users.query.filter_by(name=_uname).first().pin == _pass:
                session['user'] = users.query.filter_by(
                    name=_uname).first().name
                message = ''
                return redirect(url_for('schedule'))
        elif users.query.filter_by(email=_uname).first().pin == _pass:
            session['user'] = users.query.filter_by(email=_uname).first().name
            message = ''
            return redirect(url_for('schedule'))
        else:
            message = 'No'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/webinar")
@app.route("/live")
def live():
    if g.user:
        return render_template('live.html', User=session['user'])
    return redirect(url_for('login'))


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
        session.permanent = True


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/home')
@app.route('/schedule')
def schedule():
    if g.user:
        return render_template('schedule.html', User=session['user'], day1=day1, day2=day2)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
