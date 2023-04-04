"""CRUD operations."""

from model import db, User, Museum, User_muse, connect_to_db

def create_user(fname, lname, email, passoword, phone=None, zipcode=None):
    """Create and return a new user"""

    user = User(fname=fname,
                lname=lname,
                email=email,
                passoword=passoword,
                phone=phone,
                zipcode=zipcode)

    return user


def create_museum(name, website, img, googlemap_id, phone=None):
    """Create and return the museum"""

    museum = Museum(name=name,
                    phone=phone,
                    website=website,
                    img_url=img,
                    googlemap_id=googlemap_id)

    return museum


def get_users_by_email(email):
    """return a user object"""

    return User.query.filter_by(email=email).all()


def get_muse_by_id(googlemap_id):

    pass
