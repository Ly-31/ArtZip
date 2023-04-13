"""CRUD operations."""

from model import db, User, Museum, User_muse, connect_to_db
import requests


googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8'


def create_user(fname, lname, email, password, phone, zipcode):
    """Create and return a new user"""

    if phone == '':
        phone = None

    if zipcode == '':
        zipcode = None

    user = User(fname=fname,
                lname=lname,
                email=email,
                password=password,
                phone=phone,
                zipcode=zipcode)
    return user


def create_museum(name, place_id, website, phone):
    """Create and return the museum"""
    if phone == '':
        phone = None

    if website == '':
        website = None

    museum = Museum(name=name,
                    phone=phone,
                    website=website,
                    googlemap_id=place_id)

    return museum


def get_user_by_email(email):
    """return a user object"""

    user = User.query.filter_by(email = email).first()

    return user


def get_user_password(email):

    user = get_user_by_email(email)

    if user:
        password = user[0].password
        return password


def get_all_muse_name():

    museums = Museum.query.all()
    muse_list = []

    for muse in museums:
        muse_list.append(muse.name)

    return muse_list


def get_muse_id_by_name(muse_name):

    museum = Museum.query.filter_by(name=muse_name).one()

    return museum.id


def get_muse_details(place_id):
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    details_params = {'place_id': place_id, 'key': googlemap_key}

    details_response = requests.get(details_url, params=details_params)

    museum_details = []

    if details_response.status_code == 200:
        data = details_response.json()
        museum_details = data['result']

    return museum_details


def get_user_by_id(user_id):

    user = User.query.filter_by(id = user_id).one()
    return user


def get_muse_by_id(user_id):

    user = get_user_by_id(user_id)
    museums = user.museums

    return museums


def set_user_muse(user_id, muse_id):
    user_muse = User_muse(user_id=user_id, museum_id=muse_id)

    return user_muse


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
