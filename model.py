from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.BigInteger, nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)

    museums = db.relationship("Museum", secondary="user_muses", back_populates="users")


    def __repr__(self):
        return f"<User user_id={self.id} Name={self.fname} {self.lname} email={self.email}>"


class Museum(db.Model):
    """A museum."""

    __tablename__ = "museums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True,)
    phone = db.Column(db.BigInteger, nullable=True)
    website = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    googlemap_id = db.Column(db.String, nullable=False)

    users = db.relationship("User", secondary="user_muses", back_populates="museums")

    def __repr__(self):
        return f"<Museum museum_id={self.id} name={self.name}>"


class User_muse(db.Model):
    """Association table between user and musesum"""

    __tablename__ = "user_muses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    museum_id = db.Column(db.Integer, db.ForeignKey("museums.id"), nullable=False)

    def __repr__(self):
        return f"<User Museum id={self.id} user_id={self.user_id} museum_id={self.museum_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///artzip", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)

    # db.session.add()
    # db.session.commit()

    #Testing

    db.create_all()
    t1 = User(fname="t1", lname="t11", email="t1@gmail.com", password="dsda")
    t2 = User(fname="t2", lname="t22", email="t2@gmail.com", password="dsdajj", phone=9173652000)
    t3 = User(fname="t3", lname="t33", email="t3@gmail.com", password="dsddda", zipcode=89178)
    m1 = Museum(name='m1', phone=9182727899, website="m1.com", img_url="img1", googlemap_id="m1")
    m2 = Museum(name='m2', website="m2.com", img_url="img2", googlemap_id="m2")
    m3 = Museum(name='m3', phone=6460007899, website="m3.com", img_url="img3", googlemap_id="m3")

    db.session.add_all([t1, t2, t3, m1, m2, m3])
    db.session.commit()

    um1=User_muse(user_id=t1.id, museum_id=m1.id)
    um2=User_muse(user_id=t1.id, museum_id=m2.id)
    um3=User_muse(user_id=t3.id, museum_id=m3.id)
    um4=User_muse(user_id=t2.id, museum_id=m3.id)

    db.session.add_all([um1, um2, um3, um4])
    db.session.commit()
