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

    user = User.query.filter_by(email = email).all()
    return user


def get_user_password(email):

    user = get_user_by_email(email)

    if user:
        password = user[0].password
        return password





# def get_search_result(zipcode):
#     geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
#     geocode_param = {'address': zipcode,'key': googlemap_key}
#     geocode_response = requests.get(geocode_url, params=geocode_param)

#     msg = ""

#     if geocode_response.status_code != 200:
#         result = "Invalid zipcode!"

#     try:
#         geocode_data = geocode_response.json()
#         # print(geocode_data)
#         location = geocode_data['results'][0]['geometry']['location']
#         lat, lng = location['lat'], location['lng']

#         places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
#         places_params = {'location': f'{lat},{lng}', 'radius': 16093, 'type': 'museum', 'keyword': ["museum", "gallery"], 'key': googlemap_key}

#         places_response = requests.get(places_url, params=places_params)

#         # Check the status of the places request
#         if places_response.status_code != 200:
#             return f"Places request failed with status code {places_response.status_code}"

#         places_data = places_response.json()
#         result = places_data['results']

#     except IndexError:
#         msg = "No results found"

#     return result, msg


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
