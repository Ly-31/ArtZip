"""CRUD operations."""

from model import db, User, Museum, User_muse, connect_to_db
import requests


googlemap_key = 'AIzaSyB_18v8UhFjo18Pe6IsiJ8h1kwHyVnxVB8'


def create_user(fname, lname, email, password, phone, zipcode):
    """
        Create and return a new user.
        Phone number & zipcode are optinal input.
    """

    # if the passed in value for phone or zipcode is '', set their value to none
    if phone == '':
        phone = None

    if zipcode == '':
        zipcode = None

    # create new user
    user = User(fname=fname,
                lname=lname,
                email=email,
                password=password,
                phone=phone,
                zipcode=zipcode)
    return user


def create_museum(name, place_id, website, phone):
    """
        Create and return the museum.
        Some museum doesn't have website or phone number.
    """

    # if the passed in value for phone or website is '', set it to None.
    if phone == '':
        phone = None

    if website == '':
        website = None

    # create new museum
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
    """return a user's password"""

    # get the user object with the email
    user = get_user_by_email(email)

    if user:
        password = user[0].password
        return password


def get_all_muse_name():
    """return a list of museums' name"""

    # gets all the museum object
    museums = Museum.query.all()
    muse_list = []

    # add the name of all museums to the muse_list
    for muse in museums:
        muse_list.append(muse.name)

    return muse_list


def get_muse_id_by_name(muse_name):
    """return a museum's database id."""

    # get the museum object with the inputted museum name(unique)
    museum = Museum.query.filter_by(name=muse_name).one()

    return museum.id


def get_muse_details(place_id):
    """
        return a museum object.
        make a place API request to retrieve json object of the museum.
    """

    # pass the place_id as the param for the API request
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    details_params = {'place_id': place_id, 'key': googlemap_key}
    details_response = requests.get(details_url, params=details_params)

    museum_details = []

    if details_response.status_code == 200:
        data = details_response.json()
        museum_details = data['result']

    return museum_details


def get_user_by_id(user_id):
    """return the user object"""

    user = User.query.filter_by(id = user_id).one()

    return user


def get_user_muses_by_user_id(user_id):
    """return a list of the museum object user liked"""

    # get the user object using user_id
    user = get_user_by_id(user_id)
    # retrieve a list of museums object user liked
    museums = user.museums

    return museums


def set_user_muse(user_id, muse_id):
    """create the user_muse, which sets relationship b/t user and mueseum"""

    user_muse = User_muse(user_id=user_id, museum_id=muse_id)

    return user_muse

def check_like(user_id, muse_name):
    museums = get_user_muses_by_user_id(user_id)
    muse_id = get_muse_id_by_name(muse_name)

    for museum in museums:
        if museum.id == muse_id:
            return True


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
