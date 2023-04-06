"""CRUD operations."""

from model import db, User, Museum, User_muse, connect_to_db

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


def create_museum(name, website, img, googlemap_id, phone=None):
    """Create and return the museum"""

    museum = Museum(name=name,
                    phone=phone,
                    website=website,
                    img_url=img,
                    googlemap_id=googlemap_id)

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



def get_muse_by_id(googlemap_id):

    pass



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
