from server import app
from unittest import TestCase
from model import connect_to_db, db, testing_data
from flask import session
from model import User, Museum, User_muse
import crud


class FlaskTestsBasics(TestCase):

    def setUp(self):

        # get the Flask test client
        self.client = app.test_client()

        # show Flask errors that happen during test
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage route"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Explore Local Art Scene', result.data)

    def test_login(self):
        """Test login page route"""

        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Sign into your account', result.data)

    def test_creat_account(self):
        """Test create account page route"""

        result = self.client.get('/create-account')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Create an ArtZip account', result.data)

    def test_logout(self):
        """Test logout"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '12'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_id', session)
            self.assertIn(b"You've logged out.", result.data)

class FlaskTestsDatabase(TestCase):

    def setUp(self):

        # get flask test client & show errors
        self.client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database
        connect_to_db(app, "postgresql:///test_artzip")

        # create tables and add sample data
        db.create_all()
        testing_data()

    def tearDown(self):
        print('running teardown')
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login_feature(self):
        """Test login page with valid email and password"""

        result = self.client.post("/login",
                                    data={"login-form-email": "11@gmail.com","login-form-password": "11dsda"},
                                    follow_redirects=True)
        self.assertIn(b'Account Information', result.data)

    def test_login_feature_2(self):
        """Test login page with valid email and incorrect password"""

        result = self.client.post("/login",
                                    data={"login-form-email": "11@gmail.com","login-form-password": "dsda"},
                                    follow_redirects=True)
        self.assertIn(b'Sign into your account', result.data)

    def test_login_feature_3(self):
        """Test login page with invalid email"""

        result = self.client.post("/login",
                                    data={"login-form-email": "nonexist@gmail.com","login-form-password": "none"},
                                    follow_redirects=True)
        self.assertIn(b'Create an ArtZip account', result.data)

    def test_create_account_feature(self):
        """Test create account with valid inputs for all field"""

        result = self.client.post("/create-account",
                                    data={"fname": "test1", "lname": "test1", "email": "test1@gmail.com",
                                            "password": "Test1!test", "phone": "917-000-0000", "zipcode": "10001"},
                                            follow_redirects=True)
        self.assertIn(b'Account created successfully', result.data)
        self.assertIn(b'Sign into your account', result.data)

        # check that the user is created in the database
        users = User.query.all()
        self.assertEqual(len(users), 3)

    def test_create_account_feature_2(self):
        """Test create account with an existing email in the db"""

        result = self.client.post("/create-account",
                                    data={"fname": "t1", "lname": "t1", "email": "11@gmail.com",
                                            "password": "Test1!test", "phone": "917-000-0000", "zipcode": "10001"},
                                            follow_redirects=True)
        self.assertIn(b'There is an account associate with this email, please log in', result.get_data())
        self.assertIn(b'Sign into your account', result.data)

        # check that the user was not created in the database
        users = User.query.all()
        self.assertEqual(len(users), 2)

    def test_userhome(self):
        """Test userhome"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

        result = self.client.get('/user-home')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Account Information', result.data)
        self.assertIn(b'11@gmail.com', result.data)

    def test_add_muse_to_like(self):
        """Test add museum to user's liked list(db)"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

        result = self.client.post("/add-to-list",
                                    json={
                                        "name": "test_muse",
                                        "placeID": "test_placeID",
                                        "website": "www.test.com",
                                        "phone": "917-000-0000"})

        self.assertEqual(result.status_code, 200)

        # check if this museum is added to the museum table
        museums = crud.get_all_muse_name()
        self.assertTrue("test_muse" in museums)

        # check if this museum is added to the user-muse list
        liked = crud.check_like("1", "test_muse")
        self.assertTrue(liked)







    # def test_search_result(self):
    #     result = self.client.get('/serach-result')
    #     self.assertIn(b'results-container', result.data)







if __name__ == '__main__':
    import unittest
    unittest.main()
