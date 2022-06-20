from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired
from pogoda import check_weather, check_city, check_celcius
from datetime import date
from calendar import month_name

app = Flask(__name__)
app.config['SECRET_KEY'] = "jakis randomowy tekst"
boot = Bootstrap(app)
today = date.today()
fdate = date.today().strftime('%d/%m/%Y')
DMY = fdate.split("/")
globals()["DMY"] = DMY

## Format dzisiejszej daty DD-MM-YYYY jako global uzyty ponizej


class CurrentWeather(FlaskForm):
    month = SelectField("Select month: ", choices=[(f"{DMY[1]}", f"{month_name[int(DMY[1])]}")])
    day = SelectField("Select day: ", choices=[elem for elem in range(int(DMY[0]), int(DMY[0])+5)])
    city_name = StringField("Input city: ", validators=[InputRequired()])
    submit_btn = SubmitField("Check weather!")


@app.route("/", methods=["POST", "GET"])
def index():
    form_flask = CurrentWeather()
    if form_flask.validate_on_submit():
        month = form_flask.month.data
        day = form_flask.day.data
        city = form_flask.city_name.data
        lat, long = check_city(city)
        weather_now = check_weather(lat, long, f"2022-{month}-{day}")
        celcius_dict = check_celcius(lat, long, f"2022-{month}-{day}")
        max_celcius = celcius_dict["max"]
        min_celcius = celcius_dict["min"]
        avg_celcius = celcius_dict["day"]
        return render_template("result.html", result=weather_now, top=max_celcius, min=min_celcius,
                               avg=avg_celcius, city= city, day=day, month=month_name[int(DMY[1])])

    return render_template("index.html", form=form_flask)


if __name__ == '__main__':
    app.run()