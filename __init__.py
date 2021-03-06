


import MySQLdb

from flask import Flask, render_template ,flash,request,url_for,redirect,session
from matplotlib.pyplot import waitforbuttonpress
from content_management import Content
from dbconnect import connection

from passlib.hash import sha256_crypt

# from MySQLdb import escape_string as thwart
# from pymysql import escape_string as thwart 
from wtforms import Form ,BooleanField,PasswordField,StringField,validators
# TestFiled is not, use Test StringField
import gc


TOPIC_DICT = Content()

app = Flask(__name__)
app.secret_key="keyiskey"

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    # flash("Flash Test!!")
    return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template("dashboard.html" )
    except Exception as e:
	    return render_template("500.html", error = str(e))
		
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html")



@app.route('/login/',methods=["GET","POST"])
def login_page():
    error=" "
    try:
        if request.method=="POST":
            attempted_username=request.form["username"]
            attempted_password=request.form["password"]

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username=="admin" and attempted_password=="password":
                return redirect(url_for('dashboard'))
            else:
                error="Invalid Cr    edentials. Try Again."
        return render_template("login.html",error=error)

    except Exception as e:
        flash(e)
        return render_template("login.html",error=error)
class RegistrationForm(Form):
    # pass
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        # 
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.DataRequired()])
    

		
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username=form.username.data
            email=form.email.data
            password=sha256_crypt.encrypt((str(form.password.data)))
            c,conn=connection()

            x=c.execute("SELECT * FROM WHERE username= (%s)",username)
            if int(x)>0:
                flash("That Username is already taken,")
                return render_template('register.html',form=form)

            else:
                c.execute("Insert into users (username,password,email,tracking)Values(%s,%s,%s,%s)",(username),(password),(email),("/introduction-to-python-programming/"))
                conn.commit()
                flash("Thanks for Registering")
                c.close()
                conn.close()
                gc.collect()
                #  gc Grarbage Collector 
                session['logged_in']=True
                session['username']=username

                return redirect(url_for('dashboard'))

        return render_template("register.html",form=form)

    except Exception as e:
        return (str(e))


if __name__ == "__main__":
    app.run()
		