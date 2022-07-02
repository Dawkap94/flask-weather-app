from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired
from datetime import date
from calendar import month_name
from new_pogoda import CheckWeather, GetLatLong, Temperature

app = Flask(__name__)
app.config['SECRET_KEY'] = "NiceToKnowTheWeather"
boot = Bootstrap(app)
today = date.today()
fdate = date.today().strftime('%d/%m/%Y')
DMY = fdate.split("/")
globals()["DMY"] = DMY


## Todays date format DD-MM-YYY as global used below

class CurrentWeather(FlaskForm):
    month = SelectField("Select month: ", choices=[(f"{DMY[1]}", f"{month_name[int(DMY[1])]}")])
    day = SelectField("Select day: ", choices=[elem for elem in range(int(DMY[0]), int(DMY[0]) + 5)])
    city_name = StringField("Input city: ", validators=[InputRequired()])
    temp_value = SelectField("Select temperature unit: ", choices=["Celcius", "Fahrenheit"])
    submit_btn = SubmitField("Check weather!")


@app.route("/", methods=["POST", "GET"])
def index():
    form_flask = CurrentWeather()
    if form_flask.validate_on_submit():
        month = form_flask.month.data
        day = form_flask.day.data
        if len(day) == 1:
            day = "0" + day
        city = form_flask.city_name.data
        temp_value = form_flask.temp_value.data
        selected_date = f"2022-{month}-{day}"
        cityobj = GetLatLong(city)
        try:
            lat, lon = cityobj.get_lat_long_from_city(city)
            weatherobj = CheckWeather(lat, lon, selected_date)
            weather_now = weatherobj.get_weather_dict(selected_date)
            tempobj = Temperature(lat, lon, selected_date)
            if temp_value == "Celcius":
                celcius_dict = tempobj.get_celcius_temp(selected_date)
                max_celcius = celcius_dict["max"]
                min_celcius = celcius_dict["min"]
                avg_celcius = celcius_dict["day"]
                return render_template("result.html", result=weather_now, top=max_celcius, min=min_celcius,
                                       avg=avg_celcius, city=city, day=day, month=month_name[int(DMY[1])])
            if temp_value == "Fahrenheit":
                fahrenheit_dict = tempobj.get_fahrenheit_temp(selected_date)
                max_fahr = fahrenheit_dict["max"]
                min_fahr = fahrenheit_dict["min"]
                avg_fahr = fahrenheit_dict["day"]
                return render_template("result.html", result=weather_now, top=max_fahr, min=min_fahr,
                                       avg=avg_fahr, city=city, day=day, month=month_name[int(DMY[1])])
        except ValueError:
            return render_template("404.html")

    return render_template("index.html", form=form_flask)


if __name__ == '__main__':
    app.run()
