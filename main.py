from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import pandas


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Cafe Location on Google Maps (URL)',
                               validators=[DataRequired(),
                                           URL(require_tld=True, message="Not a valid URL, try again")])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=["✘", "☕", "☕ ☕", "☕ ☕ ☕", "☕ ☕ ☕ ☕ ", "☕ ☕ ☕ ☕ ☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating',
                              choices=["✘", "💪", "💪 💪", "💪 💪 💪", "💪 💪 💪 💪 ", "💪 💪 💪 💪 💪"],
                              validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Socket Availability',
                                      choices=["✘", "🔌", "🔌 🔌", "🔌 🔌 🔌", "🔌 🔌 🔌 🔌 ", "🔌 🔌 🔌 🔌 🔌"],
                                      validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = request.form["cafe"]
        location_url = request.form["location_url"]
        open_time = request.form["open_time"]
        closing_time = request.form["closing_time"]
        coffee_rating = request.form["coffee_rating"]
        wifi_rating = request.form["wifi_rating"]
        power_outlet_rating = request.form["power_outlet_rating"]

        new_cafe = [cafe, location_url, open_time, closing_time, coffee_rating, wifi_rating, power_outlet_rating]

        with open('cafe-data.csv', encoding="utf8", mode='a', newline='') as csv_file:
            csv_file.write(f"\n{', '.join(new_cafe)}")
        return redirect('/cafes')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding="utf8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
