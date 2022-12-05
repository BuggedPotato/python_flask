import json

from flask import Flask, render_template, session, redirect, flash, request
from flask_bs4 import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired
from datetime import date


class LoginForm(FlaskForm):
    loginName = StringField("Nazwa użytkownika: ", validators=[DataRequired()])
    userPass = StringField("Hasło:", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")

class AddSubject(FlaskForm):
    subject = StringField("Nazwa przedmiotu", validators=[DataRequired()])
    submit = SubmitField("Dodaj")

class AddGrade(FlaskForm):
    subject = SelectField('Wybierz przedmiot', choices=str, validators=[DataRequired()])
    term = RadioField('Wybierz semestr', choices=[('term1', 'Semestr 1'), ('term2', 'Semestr 2')], validators=[DataRequired()])
    category = SelectField('Wybierz kategorię', choices=[('answer', 'Odpowiedź'), ('quiz', 'Kartkówka'), ('test', 'Sprawdzian')], validators=[DataRequired()])
    grade = SelectField('Wybierz ocenę', choices=[
        ('6', 'Celujący'),
        ('5', 'Bardzo dobry'),
        ('4', 'Dobry'),
        ('3', 'Dostateczny'),
        ('2', 'Dopuszczający'),
        ('1', 'Niedostateczny')
    ], validators=[DataRequired()])
    submit = SubmitField('Dodaj')

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
    return render_template('dashboard.html', title='Dashboard', loginName=session.get('loginName'), date=date.today(), grades=grades, countAverage=countAverage, getBestAverage=getBestAverage, getDangerAverage=getDangerAverage)


@app.route("/addSubject", methods=['POST', 'GET'])
def addSubject():
    addSubject = AddSubject()
    if addSubject.validate_on_submit():
        with open("data/grades.json", encoding='utf-8') as gradesFile:
            grades = json.load(gradesFile)
            subject = addSubject.subject.data
            grades[subject] = {
                'term1': {'answer': [], 'quiz': [], 'test': [], 'interim': 0},
                'term2': {'answer': [], 'quiz': [], 'test': [], 'interim': 0, 'yearly': 0},
            }
        with open("data/grades.json", mode='w', encoding='utf-8') as gradesFile:
            json.dump(grades, gradesFile)
            gradesFile.close()
            flash('Dane zapisane poprawnie')
            return redirect('addSubject')
    return render_template("add_subject.html", title="Dodaj przedmiot", loginName=session.get('loginName'), date=date.today(), addSubject=addSubject)


@app.route("/addGrade", methods=['POST', 'GET'])
def addGrade():
    addGradeForm = AddGrade()
    with open('data/grades.json', encoding='utf-8') as gradesFile:
        grades = json.load(gradesFile)

    print(addGradeForm.validate_on_submit())
    if request.method == 'POST':
        print("opachki")
        with open("data/grades.json", mode='w', encoding='utf-8') as gradesFile:
            subject = addGradeForm.subject.data
            term = addGradeForm.term.data
            category = addGradeForm.category.data
            grade = int(addGradeForm.grade.data)
            print(grades[subject][term][category])
            grades[subject][term][category].append(grade)
            print(grades[subject][term][category])
            json.dump(grades, gradesFile)
            flash('Dane zapisane poprawnie')
            return redirect('addGrade')
    addGradeForm.subject.choices = [subject for subject in grades]
    return render_template('add-grade.html', title='Dodaj ocenę', loginName=session.get('loginName'), date=date,
                           addGradeForm=addGradeForm)

def countAverage(subjectValue, termValue, data=None):
    if data is None:
        with open('data/grades.json') as gradesFile:
            grades = json.load(gradesFile)
            gradesFile.close()
    else:
        grades = data
    sumGrades = 0
    length = 0

    if subjectValue != "" and termValue == "year":
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                    for category, grades in categories.items():
                        if category == 'answer' or category == 'quiz' or category == 'test':
                            for grade in grades:
                                sumGrades += grade
                                length += 1

    elif subjectValue == "" and termValue == "":
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
    if length != 0:
        return round(sumGrades/length, 2)
    return 0

def getBestAverage(count):
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        values = {subject: countAverage(subject, "year", grades) for subject, terms in grades.items()}
        gradesFile.close()
    return dict(sorted(values.items(), key=lambda x : x[1], reverse=True)[0:count])

def getDangerAverage():
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        values = {subject: countAverage(subject, "year", grades) for subject, terms in grades.items()}
        gradesFile.close()
    out = {}
    for key, value in values.items():
        if value < 2:
            out[key] = value
    return out

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404

@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500

if __name__ == '__main__':
    app.run(debug=True)
