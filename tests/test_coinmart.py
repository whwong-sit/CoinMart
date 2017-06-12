# coding=utf-8
import os
import pytest
from coinmart import coinmart
import tempfile
import requests
import unittest

from flask import request


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

def getExchangeRate(currency_1, currency_2):
    currency_2_lowercase = currency_2.lower()
    main_api = 'https://api.coinmarketcap.com/v1/ticker/'
    search_currency = currency_1 + '/?convert=' + currency_2
    url = main_api + search_currency
    json_data = requests.get(url).json()
    json_convert_price = json_data[0]['price_' + currency_2_lowercase]
    price = float(json_convert_price)
    return price

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
        rv = login(client, 'admin', 'default')
        assert b'Login Success!' in rv.data
        rv = client.post('/register', data=dict(
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
        username='Test1',
        password='test',
        email='test@yahoo.com',
        cfm_password='test'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data


def test_register_passwords_dont_match(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/register', data=dict(
        username='Test2',
        password='Svalli30',
        email='test@yahoo.com',
        cfm_password='Svalli301'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Passwords do not match' in rv.data

def test_register_no_numbers(client):
    rv = client.post('/register', data=dict(
        username='Test3',
        password='Password',
        email='test@yahoo.com',
        cfm_password='Password'
    ), follow_redirects=True)
    assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data

def test_register_no_capitals(client):
    rv = client.post('/register', data=dict(
        username='Test4',
        password='password32',
        email='test@yahoo.com',
        cfm_password='password32'
    ), follow_redirects=True)
    assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data

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

def test_user_ready_registered(client):
    rv = client.post('/register', data=dict(
        username='Test1',
        password='Hema7067',
        email='test@yahoo.com',
        cfm_password='Hema7067'
    ), follow_redirects=True)
    rv = logout(client)
    rv = client.post('/register', data=dict(
        username = 'Test1',
        password = 'Hema7067',
        email = 'test@yahoo.com',
        cfm_password = 'Hema7067'
        ), follow_redirects=True)
    assert b'User already registered' in rv.data

def test_exchanges_visible(client):
    rv = login(client, 'Test', 'Test_123')
    if __name__ == '__main__':
        data = coinmart.get_user_watchlists()
        for i in data:
            Cryptocurrency = data[i]['cryptocurrency']
            Currency = data[i]['currency']
            Curr_Val = data[i]['current_value']
            Curr_Timestamp = data[i]['current_time']
            Old_Val = data[i]['old_value']
            Old_Timestamp = data[i]['old_time']
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

def test_no_exchanges(client):
    rv = login(client, 'admin', 'default')
    if __name__ == '__main__':
        assert b'Unbelievable. No watchlist created so far' in rv.data

def test_old_exch_correct():
    if __name__ == '__main__':
        data = coinmart.get_user_watchlists()
        for i in data:
            cryptocurrency = data[i]['cryptocurrency']
            currency = data[i]['currency']
            old_stored_exch = data[i]['old_value']
            old_stored_exch_time = data[i]['old_time']
            symbol = coinmart.exchange_rate(cryptocurrency, currency)['symbol']
            old_exch_rate = coinmart.get_previous_exchange_rate(symbol, currency)['old_exch']
            old_exch_time = coinmart.get_previous_exchange_rate(symbol, currency)['old_time']
            if old_stored_exch != old_exch_rate:
                assert False
            elif old_stored_exch_time != old_exch_time:
                assert False
        assert True

def test_getExchangeRateIsFloat():
    assert isinstance(getExchangeRate('bitcoin', 'EUR'), float)


def test_getExchangeRateComparison():
    assert getExchangeRate('bitcoin', 'EUR') != getExchangeRate('bitcoin', 'AUD')


def test_getExchangeRateComparison2():
    assert getExchangeRate('ethereum', 'GBP') != getExchangeRate('bitcoin', 'GBP')

def test_add_watchlist(client):
    with client as c:
        rv = c.post('/login', data=dict(
            username='Test',
            password='Test_123'
        ), follow_redirects=True)
    if __name__ == '__main__':
        coinmart.add_watchlist("Ripple", "USD")
        assert b'Ripple' and b'USD' in rv.data

def test_currency_list():
    with coinmart.app.app_context():
        assert coinmart.monetary_currency_list()
        assert coinmart.crypto_currency_list()

def test_exchanges_update_correct(client):
    with client as c:
        rv = c.post('/login', data=dict(
            username='Test',
            password='Test_123'
        ), follow_redirects=True)
    if __name__ == '__main__':
        client.getUpdatedWatchlistExchanges()
        data = client.get_user_watchlists()
        for i in range(len(data)):
            cryptocurrency = data[i]['cryptocurrency']
            currency = data[i]['currency']
            curr_exch_rate = client.exchange_rate(cryptocurrency, currency)['price']
            curr_stored_exch = data[i]['current_value']
            if curr_exch_rate == curr_stored_exch:
                assert True
            else:
                assert False

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

def test_create_watchlist(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/addwatchlist', data=dict(
        watchlistname="admin",
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'add watch list Success!' in rv.data

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

def test_addapair_in_a_watchlist(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/addpair', data=dict(
        msg="admin bitcoin",
        currency="EUR"
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'New pair added' in rv.data
