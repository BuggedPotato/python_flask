from flask import Flask,render_template, request, session, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    userName = StringField("Podaj swoje imię: ", validators=[DataRequired()])
    submit = SubmitField("Wyślij")


app = Flask(__name__)
app.secret_key = "asecretkey"
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    userForm = NameForm()
    return render_template('index.html', title='Strona główna', userForm=userForm)


@app.route('/user', methods=['POST'])
def user():
    userName = request.form['userName']
    return render_template('user.html', title='Strona główna', userName=userName)


@app.route('/setSession', methods=['POST', 'GET'])
def setSession():
    userForm = NameForm()
    if userForm.validate_on_submit():
        oldName = session.get('userName')
        if oldName is not None and oldName != userForm.userName.data:
            flash('Wygląda na to, że nazywasz się inaczej!')
        session['userName'] = userForm.userName.data
        return redirect(url_for('setSession'))
    return render_template('session.html', title='Zastosowanie sesji', userForm=userForm, userName=session.get('userName'))

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500

if __name__ == '__main__':
    app.run()
