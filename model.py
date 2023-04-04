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
    phone = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)

    museums = db.relationship("Museum", secondary="user_muses", back_populates="users")


    def __repr__(self):
        return f"<User user_id={self.user_id} Name={self.fname} {self.lname} email={self.email}>"


class Museum(db.Model):
    """A museum."""

    ___tablename__ = "museums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    website = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    googlemap_id = db.Column(db.String, nullable=False)

    users = db.relationship("User", secondary="user_muses", back_populates="museums")

    def __repr__(self):
        return f"<Museum museum_id={self.museum_id} name={self.name}>"


class User_muse(db.Model):
    """Association table between user and musesum"""

    __tablename__ = "user_muses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    musesum_id = db.Column(db.Integer, db.ForeignKey("museums.id"), nullable=False)


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
