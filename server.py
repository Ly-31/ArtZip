from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from flask import Flask
from jinja2 import StrictUndefined
import os
import json
import requests

app = Flask(__name__)
app.secret_key = "art"
app.jinja_env.undefined = StrictUndefined


# API_KEY = os.environ['GOOGLEMAP_KEY']

@app.route('/')
def hompage():
    """Show homepage"""

    return render_template('homepage.html')


@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def verify_login():

    return redirect('/user-home')


@app.route('/create-account')
def create_account():
    """Add a new user to our database."""

    return render_template('create_account.html')


@app.route('/create-account', methods=['POST'])
def verify_account():
    """Add a new user to our database."""

    fname = request.form.get("acct-fname")
    lname = request.form.get("acct-lname")
    email = request.form.get("acct-email")
    password = request.form.get("acctpassowrd")
    phone = request.form.get("acct_phone")
    zipcode = request.form.get("acct-zipcode")

    user = crud.get_users_by_email(email)

    if user:
        flash("There is account associate with this email, please log in")
    else:
        crud.create_user(fname, lname, email, password, phone, zipcode)

    return redirect('/login.html')


@app.route('/user-home')
def user_homepage():

    return render_template('user_homepage.html')



@app.route('/search-result', methods=['POST'])
def result():
    """Search for museums on Google Map"""

    return render_template('search_result.html')


if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
