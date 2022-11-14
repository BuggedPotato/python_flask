import json

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import date


class LoginForm(FlaskForm):
    loginName = StringField("Nazwa użytkownika: ", validators=[DataRequired()])
    userPass = StringField("Hasło:", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")


app = Flask(__name__)
app.secret_key = "asecretkey"
bootstrap = Bootstrap(app)
moment = Moment(app)

users = {1: {'loginName': 'dpikon', 'userPass': 'Qwerty123!', 'fname': 'Dominik', 'lname': 'Pikoń'}}


@app.route('/')
def index():
    return render_template('index.html', title='Strona główna')


@app.route('/logIn', methods=['POST', 'GET'])
def logIn():
    login = LoginForm()
    if login.validate_on_submit():
        loginName = login.loginName.data
        userPass = login.userPass.data
        if userPass == users[1]['userPass'] and loginName == users[1]['loginName']:
            session['loginName'] = loginName
            return redirect('dashboard')
    return render_template('login.html', title="Logowanie", login=login, loginName=session.get('loginName'))


@app.route('/logOut')
def logOut():
    session.pop('loginName')
    return redirect('logIn')


@app.route('/dashboard')
def dashboard():
    with open( "data/grades.json" ) as gradesFile:
        grades = json.load( gradesFile )
        gradesFile.close()
    return render_template('dashboard.html', title='Dashboard', loginName=session.get('loginName'), date=date.today(), grades=grades, countAverage=countAverage)


def countAverage(subjectValue, termValue):
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    sumGrades = 0
    length = 0
    if subjectValue == "" and termValue == "":
        for subject, terms in grades.items():
            for term, categories in terms.items():
                for category, grades in categories.items():
                    if category == 'answer' or category == 'quiz' or category == 'test':
                        for grade in grades:
                            sumGrades += grade
                            length += 1
    else:
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                    if term == termValue:
                        for category, grades in categories.items():
                            if category == 'answer' or category == 'quiz' or category == 'test':
                                for grade in grades:
                                    sumGrades += grade
                                    length += 1
    return round(sumGrades/length, 2)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500

if __name__ == '__main__':
    app.run(debug=True)
