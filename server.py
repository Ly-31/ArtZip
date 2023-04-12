from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud
# from flask import Flask
from jinja2 import StrictUndefined
import os
import json
import requests
from time import sleep


app = Flask(__name__)
app.secret_key = "art"
app.jinja_env.undefined = StrictUndefined

GOOGLEMAP_KEY = os.environ['GOOGLEMAP_KEY']

googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8'

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
    print(f'form-password: {password}')

    db_user = crud.get_user_by_email(email)
    print(f'*****user: {db_user}')
    print(db_user.id)


    if db_user:
        db_password = db_user.password

        if password == db_password:
            session['user_id'] = db_user.id
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
        return redirect('/login')


@app.route('/user-home')
def user_homepage():
    logged_user = session.get("user_id")

    #function to retrive user info by id
    user = crud.get_user_by_id(logged_user)
    museums = crud.get_muse_by_id(logged_user)

    return render_template('user_homepage.html', user=user, museums=museums)


# @app.route('/search-result')
# def result():
    """Returns search result for museums on Google Map"""

    zipcode = request.args.get("search-bar-zipcode")
    # print(f"********** zipcode:{zipcode}")
    # print(type(zipcode))


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
            token = places_data['next_page_token']
            places_params['pagetoken'] = places_data['next_page_token']
            places_response = requests.get(places_url, params=places_params)
            places_data = places_response.json()
            result.extend(places_data['results'])



        return render_template('search_result.html', places_data=result, key=googlemap_key, token=token)

    except IndexError:
        return "No results found"


# @app.route('/muse-details')
# def show_muse_details():
    place_id = request.args.get('place_id')

    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    details_params = {'place_id': place_id, 'key': googlemap_key}

    details_response = requests.get(details_url, params=details_params)


    if details_response.status_code == 200:
        data = details_response.json()
        museum_details = data['result']

        return render_template('muse_details.html', museum_details=museum_details, key=googlemap_key)

    else:
        return f"Details request failed with status code {details_response.status_code}"


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


    # if geocode_response.status_code != 200:
    #     msg = "invalid zipcode"
    #     return f"Geocode request failed with status code {geocode_response.status_code}"

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
            msg = "valid zipcode"
            return f"Places request failed with status code {places_response.status_code}"

        places_data = places_response.json()
        print(f'place_data: {places_data}')

        if 'next_page_token' in places_data:
            token = places_data['next_page_token']
            print(f'**********result token: {token}')


        return render_template('search_result.html', places_data=places_data['results'], key=googlemap_key, token=token)
    except IndexError:
        return "No results found"

@app.route('/load-more-results.json')
def load_more_results():
    token = request.args.get("token")
    print(f'*************load more: {token}')

    places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    places_params = {'key': googlemap_key}
    places_params['pagetoken'] = token
    places_response = requests.get(places_url, params=places_params)
    places_data = places_response.json()

    return jsonify(places_data)


@app.route('/muse-details')
def show_muse_details():
    place_id = request.args.get('place_id')
    museum_details = crud.get_muse_details(place_id)

    return render_template('muse_details.html', museum_details=museum_details, key=googlemap_key)


@app.route('/add-to-list', methods=['POST'])
def add_muse_to_list():

    # if session['user_id']:
    logged_user = session.get("user_id")

    if logged_user is None:
        return redirect('/login')
    else:
        place_id = request.form.get("place-id")
        name = request.form.get("muse-name")
        website = request.form.get("muse-website")
        phone = request.form.get("muse-phone" )

        # check if museum already in muse db
        muse_list = crud.get_all_muse_name()

        if name in muse_list:
            muse_id = crud.get_muse_id_by_name(name)
            user_muse = crud.set_user_muse(logged_user,muse_id)
            db.session.add(user_muse)
            db.session.commit()
        else:
            #add museum to database
            new_muse = crud.create_museum(name, place_id, website, phone)
            db.session.add(new_muse)
            db.session.commit()

            muse_id = new_muse.id
            user_muse = crud.set_user_muse(logged_user,muse_id)
            db.session.add(user_muse)
            db.session.commit()

        return redirect('/user-home')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
