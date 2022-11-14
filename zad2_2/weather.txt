import json

from flask import Flask,render_template, request, session, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CityForm(FlaskForm):
    city = StringField("Podaj miasto: ", validators=[DataRequired()])
    submit = SubmitField("Sprawdź")


app = Flask(__name__)
app.secret_key = "asecretkey"
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    form = CityForm()
    return render_template('weather.html', title='Sprawdź pogodę', cityForm=form)

@app.route('/city', methods=['POST', 'GET'])
def city():
    city = request.form['city']
    form = CityForm()
    keys = { "stacja": "stacja", "data_pomiaru": "data pomiaru", "godzina_pomiaru": "godzina pomiaru",
             "temperatura": "temperatura", "predkosc_wiatru": "predkość wiatru", "kierunek_wiatru": "kierunek wiatru",
            "wilgotnosc_wzgledna": "wilgotność względna", "suma_opadu": "suma opadu", "cisnienie": "ciśnienie" }
    with open("weather.json", "r") as file:
        data = json.loads(file.read())
        for city_data in data:
            if city_data['stacja'].lower() == city.lower():
                return render_template('weather.html', title='Sprawdź pogodę', cityForm=form, weatherData=city_data, keys=keys)
    flash("Nie znaleziono danych dla miasta " + city)
    return render_template('weather.html', title='Sprawdź pogodę', cityForm=form)

if __name__ == '__main__':
    app.run(debug=True)
