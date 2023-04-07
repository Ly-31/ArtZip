from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from flask import Flask
from jinja2 import StrictUndefined
import os
import json
import requests
from time import sleep

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

    email = request.form.get("login-form-email")
    password = request.form.get("login-form-password")

    db_user = crud.get_user_by_email(email)
    db_password = crud.get_user_password(email)

    if db_user:
        if password == db_password:
            return redirect('/user-home')
        else:
            flash("Incorrect password, please try again.")
            return redirect('/login')
    else:
        flash("There is no account assoicated with this email. Please create an account.")
        return redirect('/create-account')


@app.route('/create-account')
def create_account():
    """Add a new user to our database."""

    return render_template('create_account.html')


@app.route('/create-account', methods=['POST'])
def verify_account():
    """Add a new user to our database."""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    zipcode = request.form.get("zipcode")

    user = crud.get_user_by_email(email)

    if user:
        flash("There is account associate with this email, please log in")
        return redirect('/login')
    else:
        new_user = crud.create_user(fname, lname, email, password, phone, zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully")
        return redirect('user-home')


@app.route('/user-home')
def user_homepage():

    return render_template('user_homepage.html')


# @app.route('/search-result')
# def result():
    """Returns search result for museums on Google Map"""

    zipcode = request.form.get("search-bar-zipcode")
    print(f"********** zipcode:{zipcode}")
    print(type(zipcode))

    if zipcode == "":
        print("No zipcode")
        return redirect('/')
    else:
        print("Zipcode exist")
        return render_template('search_result.html')

    if len(zipcode) != 5:
        flash("Invalid zipcode")
        return redirect('/')
    else:
        try:
            zipcode = int(zipcode)
            #use api to get the result
            return render_template('search_result.html')
        except:
            flash("Invalid zipcode")
            return redirect('/')


@app.route('/search-result')
def result():
    """Returns search result for museums on Google Map"""

    googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8'
    zipcode = request.args.get("search-bar-zipcode")
    print(f"********** zipcode:{zipcode}")
    print(type(zipcode))


    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    geocode_param = {'address': zipcode,'key': googlemap_key}
    geocode_response = requests.get(geocode_url, params=geocode_param)


    if geocode_response.status_code != 200:
        msg = "invalid zipcode"
        return f"Geocode request failed with status code {geocode_response.status_code}"

    try:
        geocode_data = geocode_response.json()
        # print(geocode_data)
        location = geocode_data['results'][0]['geometry']['location']
        lat, lng = location['lat'], location['lng']

        places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        places_params = {'location': f'{lat},{lng}', 'radius': 16093, 'type': 'museum', 'keyword': ["museum", "gallery"], 'key': googlemap_key}

        places_response = requests.get(places_url, params=places_params)

        # Check the status of the places request
        if places_response.status_code != 200:
            return f"Places request failed with status code {places_response.status_code}"

        places_data = places_response.json()
        result = places_data['results']

        while 'next_page_token' in places_data:
            sleep(2)
            places_params['pagetoken'] = places_data['next_page_token']
            places_response = requests.get(places_url, params=places_params)
            places_data = places_response.json()
            result.extend(places_data['results'])


        return render_template('search_result.html', places_data=result, key=googlemap_key)

    except IndexError:
        return "No results found"



@app.route('/muse-details')
def show_muse_details():

    return render_template('muse_details.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
