from flask import Flask,render_template, request, flash
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    sequence = StringField("Podaj ciąg liczb oddzielonych przecinkiem: ", validators=[DataRequired()])
    submit = SubmitField("Wyślij")

app = Flask(__name__)
app.secret_key = "asecretkey"
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    userForm = NameForm()
    return render_template('index.html', title='Strona główna', userForm=userForm)

@app.route('/handleInput', methods=['POST'])
def handleInput():
    userForm = NameForm()
    if userForm.validate_on_submit():
        sequence = request.form['sequence']
        sequence = sequence.split(',')
        if sequence is None or len(sequence) <= 0:
            flash('Wprowadzono niepoprawne dane')
            return render_template('index.html', title='Strona główna', userForm=userForm)
        try:
            sequence = [float(num) for num in sequence ]
        except ValueError:
            flash('Wprowadzone dane nie są liczbami')
        else:
            desc = [*sequence]
            desc.sort(reverse=True)
            min_val = desc[-1]
            max_val = desc[0]
            avg = sum(sequence) / len(sequence)
            res = {
                'min_val': min_val,
                'max_val': max_val,
                'desc': desc,
                'avg': avg
            }
            return render_template('index.html', title='Strona główna', userForm=userForm, res=res)
    return render_template('index.html', title='Strona główna', userForm=userForm)


if __name__ == '__main__':
    app.run()