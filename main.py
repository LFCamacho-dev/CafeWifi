from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL(require_tld=True,
                                                                       message='Not a valid URL')])
    opened = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    coffe = SelectField('Coffe',
                        validators=[DataRequired()],
                        choices=['','☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'])
    wifi = SelectField('Wifi',
                       validators=[DataRequired()],
                       choices=['','💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'])
    power = SelectField('Power',
                        validators=[DataRequired()],
                        choices=['','🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = request.form['cafe']
        location = request.form['location']
        opened = request.form['oppend']
        close = request.form['close']
        coffe = request.form['coffe']
        wifi = request.form['wifi']
        power = request.form['power']
        add_cafe_form = [cafe, location, opened, close, coffe, wifi, power]
        print(add_cafe_form)
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
