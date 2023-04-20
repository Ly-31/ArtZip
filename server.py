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


googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8'

@app.route('/')
def hompage():
    """Show homepage"""

    return render_template('homepage.html')

@app.route('/user-session', methods=['POST'])
def check_user_in_session():
    """Check if there is a user in session"""

    # get the user id from session
    logged_user = session.get("user_id")

    if logged_user is not None:
        return {"user_id": True}
    else:
        return {"user_id": False}


@app.route('/login')
def login():
    """Show login page"""

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        flash("You've logout.")
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/login', methods=['POST'])
def verify_login():
    """Verify if user exist in the database"""

    # get user info from the log-in from
    email = request.form.get("login-form-email")
    password = request.form.get("login-form-password")

    # get user from db using the inputted email using the get_user_by_email function
    # get_user_by_email function returns the user object
    db_user = crud.get_user_by_email(email)

    # check if user exist in the db
    if db_user:
        # retrieve user's password
        db_password = db_user.password

        # check if the inputted password matches password in the db
        # if the password matches, log the user id in session
        # and redirect user to their homepage
        if password == db_password:
            session['user_id'] = db_user.id
            return redirect('/user-home')
        # if the passowrd don't match, flash error msg and redirect user to log in page
        else:
            flash("Incorrect password, please try again.")
            return redirect('/login')
    # if user doesn't exit in the db, flash error message, redirect user to create account page
    else:
        flash("There is no account assoicated with this email. Please create an account.")
        return redirect('/create-account')


@app.route('/create-account')
def create_account():
    """Show create account page"""

    return render_template('create_account.html')


@app.route('/create-account', methods=['POST'])
def verify_account():
    """Add a new user to our database."""

    # get user's input from the create account form
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    zipcode = request.form.get("zipcode")

    # get user from db using the inputted email using the get_user_by_email function
    # get_user_by_email function returns the user object
    user = crud.get_user_by_email(email)

    # if user exist in the db, flask error msg and redirect to login page
    if user:
        flash("There is account associate with this email, please log in")
        return redirect('/login')
    # if user doesn't exit in the db
    # use the create_user function to create a new user with the form infos
    # add the new user to db then flash success msg and redirect user to log in
    else:
        new_user = crud.create_user(fname, lname, email, password, phone, zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully")
        return redirect('/login')


@app.route('/user-home')
def user_homepage():
    """Show user homepage"""

    # get the user id from session
    logged_user = session.get("user_id")

    # retrieve user object by id using get_user_by_id function
    # get a list of museums object user liked use user id
    user = crud.get_user_by_id(logged_user)
    museums = crud.get_muses_by_id(logged_user)

    return render_template('user_homepage.html', user=user, museums=museums)


@app.route('/search-result')
def result():
    """
        Returns search result for museums using google places API.
        It will return the first 20th result.
    """

    googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8'

    # get the zipcode user searched from the search bar
    zipcode = request.args.get("search-bar-zipcode")
    print(f'*****{zipcode}')

    # check if user entered a zipcode
    if zipcode == "":
        flash('Please enter a zipcode.')
        return redirect('/')

    # use google geocode API to retrieve lng and lat from Zipcode
    # send request to geocode API with the zipcode as param
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    geocode_param = {'address': zipcode,'key': googlemap_key}
    geocode_response = requests.get(geocode_url, params=geocode_param)

    # check if the the API request was successful
    # if the request failed, show error code
    if geocode_response.status_code != 200:
        return f"Geocode request failed with status code {geocode_response.status_code}"

    # try to covert the geocode api response to json object
    # gets the lat & lng from the json object using the lat & lng key
    try:
        geocode_data = geocode_response.json()
        location = geocode_data['results'][0]['geometry']['location']
        lat, lng = location['lat'], location['lng']

        # make request to google places API to perform a nearby search of the inputted zipcode and retrieve establishments that are museum or gallery
        places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        places_params = {'location': f'{lat},{lng}', 'radius': 16093, 'type': 'museum', 'keyword': ["museum", "gallery"], 'key': googlemap_key}
        places_response = requests.get(places_url, params=places_params)

        # Check the status of the places request
        if places_response.status_code != 200:
            return f"Places request failed with status code {places_response.status_code}"

        # convert the place response to json object
        places_data = places_response.json()
        print(places_data['results'],)

        # check if there is next-page(more results) that we can request
        if 'next_page_token' in places_data:
            token = places_data['next_page_token']

        return render_template('search_result.html', places_data=places_data['results'], key=googlemap_key, token=token)
    except IndexError:
        return "No results found"


@app.route('/load-more-results.json')
def load_more_results():
    """Return json object of museums"""

    # gets the next page token from fetch post request
    token = request.args.get("token")

    # make API request to get the next batch results(20 result)
    places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    places_params = {'key': googlemap_key}
    places_params['pagetoken'] = token
    places_response = requests.get(places_url, params=places_params)
    places_data = places_response.json()

    return jsonify(places_data)


@app.route('/muse-details')
def show_muse_details():
    """Show museum detail page"""

    # get the place_ id of that specific museum use click on
    place_id = request.args.get('place_id')

    # get the museum dict using the place_id
    # get_muse_details() takes the place_id as input
    # and make a place API request to retrieve json object of the place
    museum_details = crud.get_muse_details(place_id)

    return render_template('muse_details.html', museum_details=museum_details, key=googlemap_key)


@app.route('/add-to-list', methods=['POST'])
def add_muse_to_list():
    """Add museum to user's liked list"""

    # get current user from the session
    logged_user = session.get("user_id")

    # if user is not logged in, redirect user to log in page
    if logged_user is None:
        return redirect('/login')
    # if user is logged in, get museum info from the form
    else:
        name = request.json.get("name")
        place_id = request.json.get("placeID")
        website = request.json.get("website")
        phone = request.json.get("phone")
        print(f'*****{phone}')

        # get a list of museums' name
        muse_list = crud.get_all_muse_name()

        # check if current museum is already in db
        # if the current museum is in db, add this museum to user-muse list
        if name in muse_list:
            muse_id = crud.get_muse_id_by_name(name)
            user_muse = crud.set_user_muse(logged_user,muse_id)
            db.session.add(user_muse)
            db.session.commit()
        else:
            #if the museum is not in db, add museum to db, then add this museum to user-muse list
            new_muse = crud.create_museum(name, place_id, website, phone)
            db.session.add(new_muse)
            db.session.commit()

            muse_id = new_muse.id
            user_muse = crud.set_user_muse(logged_user,muse_id)
            db.session.add(user_muse)
            db.session.commit()

        return { "success": True,
                "status": f"{name} has been added to your liked list."
        }


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
