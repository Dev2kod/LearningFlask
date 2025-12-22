from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired, Email, Length
import os 
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-secret-change-me')

class RegisterationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    submit = SubmitField('Register')

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        return f"Registration successful for {username} ({email})"
    return render_template("register.html", form = form)

@app.route("/")
def home():
    return '<a href="/register">Go to register</a>"'

if __name__ == "__main__":
    app.run(debug=True)