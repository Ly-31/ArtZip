from server import app
from unittest import TestCase
from model import connect_to_db, db, testing_data
from flask import session

class FlaskTestsBasics(TestCase):

    def setUp(self):

        # get the Flask test client
        self.client = app.test_client()

        # show Flask errors that happen during test
        app.config['TESTING'] = True

    def test_index(self):

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Explore Local Art Scene', result.data)

    def test_login(self):

        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Sign into your account', result.data)

    def test_creat_account(self):

        result = self.client.get('/create-account')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Create an ArtZip account', result.data)

    def test_logout(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '12'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_id', session)
            self.assertIn(b"You've logged out.", result.data)

class FlaskTestssDatabase(TestCase):

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
        """Test login page"""

        result = self.client.post("/login",
                                    data={"login-form-email": "11@gmail.com","login-form-password": "11dsda"},
                                        follow_redirects=True)
        self.assertIn(b'Account Information', result.data)


    # def test_userhome(self):
    #     result = self.client.get('/user-home')
    #     self.assertIn(b'Account Information', result.data)

    # def test_search_result(self):
    #     result = self.client.get('/serach-result')
    #     self.assertIn(b'', result.data)







if __name__ == '__main__':
    import unittest
    unittest.main()
