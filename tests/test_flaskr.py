import os
import flaskr
from flaskr import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def login(self, username, password):
        self.app.get('/logout', follow_redirects=True)
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def register(self, username, email, password, password1):
        self.app.get('/logout', follow_redirects=True)
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            cfm_password=password1
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_register(self):
        rv = self.register('admin', 'admin@admin.com', 'Admin111', 'Admin111')
        assert b'You were successfully registered and have been logged in' in rv.data
        rv = self.register('admin', 'admin@admin.com', 'Admin111', 'Admin111')
        assert b'User already registered' in rv.data
        rv = self.register('admin1', 'admin@admin.com', 'default', 'default')
        assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data
        rv = self.register('admin1', 'admin@admin.com', 'Defaultt', 'Defaultt')
        assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data
        rv = self.register('admin1', 'admin@admin.com', 'default1', 'default1')
        assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data
        rv = self.register('admin1', 'admin@admin.com', 'default', 'Default')
        assert b'Passwords do not match' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'Admin111')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert b'User not registered' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Incorrect username or password' in rv.data
        rv = self.login('admin@uni.sydney.edu.au', 'defaultx')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()