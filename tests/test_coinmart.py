# coding=utf-8
import os
import pytest
import coinmart
from coinmart import coinmart
import tempfile


@pytest.fixture
def client(request):
    db_fd, coinmart.app.config['DATABASE'] = tempfile.mkstemp()
    coinmart.app.config['TESTING'] = True
    client = coinmart.app.test_client()
    with coinmart.app.app_context():
        coinmart.init_db()
    def teardown():
        os.close(db_fd)
        os.unlink(coinmart.app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_empty_db(client):
    rv = client.get('/')
    if __name__ == '__main__':
        assert b'Unbelievable. No watchlist created so far' in rv.data

def test_login_logout(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data

def test_login_logout1(client):
    rv = login(client, 'admin@uni.sydney.edu.au', 'default')
    assert b'Login Success!' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data

def test_login_incorrect_credentials(client):
    with client as c:
        rv = c.post('/login', data=dict(
            username='admin',
            password='test'
        ), follow_redirects=False)
    if __name__ == '__main__':
        assert b'Incorrect username or password' in rv.data


def test_register_login(client):
    with client as c:
        rv = login(c, 'admin', 'default')
        assert b'Login Success!' in rv.data
        rv = c.post('/register', data=dict(
            username='Test',
            password='Hema7067',
            email='Test@yahoo.com',
            cfm_password='Hema7067'
        ), follow_redirects=True)
        if __name__ == '__main__':
            assert b'You were successfully registered and have been logged in' in rv.data


def test_register_invalid_password(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/register', data=dict(
        username='test',
        password='test',
        email='test@yahoo.com',
        cfm_password='test'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data


def test_register_password_match(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/register', data=dict(
        username='Test',
        password='Svalli30',
        email='test@yahoo.com',
        cfm_password='Svalli301'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Passwords do not match' in rv.data


def test_registered_users(client):
    rv = login(client, coinmart.app.config['USERNAME'],
               coinmart.app.config['PASSWORD'])
    assert b'Login Success!' in rv.data
    rv = client.post('/register', data=dict(
        username='Test1',
        password='Hema7067',
        email='test@yahoo.com',
        cfm_password='Hema7067'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'User already registered' in rv.data

def test_update_exchanges(client):
    with client as c:
        rv = login(client, 'Test', 'Test_123')
    if __name__ == '__main__':
        data = coinmart.get_user_watchlists()
        for i in data:
            Cryptocurrency = data[i]['cryptocurrency']
            Currency = data[i]['currency']
            Curr_Val = data[i]['value']
            Curr_Timestamp = data[i]['time_stamp']
            Old_Val = data[i]['old_value']
            Old_Timestamp = data[i]['old_time_stamp']
            cryptocurrency_visible = Cryptocurrency in rv.data
            currency_visible = Currency in rv.data
            value_visible = Curr_Val in rv.data
            timestamp_visible = Curr_Timestamp in rv.data
            old_value_visible = Old_Val in rv.data
            old_timestamp_visible = Old_Timestamp in rv.data
            watchlist_visible = (cryptocurrency_visible and currency_visible and value_visible and timestamp_visible and old_value_visible and old_timestamp_visible)
            if watchlist_visible == False:
                assert False
        assert True

def test_exchange_rate_is_float():
    with coinmart.app.app_context():
        response = coinmart.exchange_rate('bitcoin', 'EUR')
        assert isinstance(response['price'], float)
        assert isinstance(response['date_time'], str)


def test_exchange_rate_comparison():
    with coinmart.app.app_context():
        assert coinmart.exchange_rate('bitcoin', 'EUR') != coinmart.exchange_rate('bitcoin', 'AUD')
        assert coinmart.exchange_rate('ethereum', 'GBP') != coinmart.exchange_rate('bitcoin', 'GBP')


def test_currency_list():
    with coinmart.app.app_context():
        assert coinmart.monetary_currency_list()
        assert coinmart.crypto_currency_list()


def test_user_watchlist(client):
    with client as c:
        rv = c.post('/login', data=dict(
            username='Test',
            password='Test_123'
        ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Login Success!' in rv.data
        assert client.get('/')
        assert client.show_watchlists()


def test_add_watchlist(client):
    with client as c:
        rv = c.post('/login', data=dict(
            username='Test',
            password='Test_123'
        ), follow_redirects=True)
    if __name__ == '__main__':
        client.add_watchlist('bitcoin', 'EUR')
        assert b'New watchlist added' in rv.data
        assert client.get('/')
        assert client.show_watchlists()
