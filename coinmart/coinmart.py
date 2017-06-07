# all the imports
import os
import sqlite3
import re
import time
import requests

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

os.environ['FLASK_APP'] = 'coinmart'

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , CoinMartIndividual.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'coinmart.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('COINMART_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db(schema='schema.sql'):
    db = get_db()
    with app.open_resource(schema, mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_watchlists():
    watchlistsname = get_user_watchlistsname()
    return render_template('dashboard.html',watchlistsname=watchlistsname)


def get_user_watchlists(showwatchlist):
    db = get_db()
    auth_user = session.get("username")
    cur = db.execute('select user_watchlists.username, user_watchlists.watchlist_name, watchlist_items.cryptocurrency, watchlist_items.currency, watchlist_items.current_value, historical_watchlist_data.old_value, historical_watchlist_data.old_time from user_watchlists, watchlist_items, historical_watchlist_data where user_watchlists.watchlist_name = watchlist_items.watchlist_name and user_watchlists.watchlist_name = historical_watchlist_data.watchlist_name and user_watchlists.username = ? and user_watchlists.watchlist_name=? and watchlist_items.cryptocurrency = historical_watchlist_data.cryptocurrency and  watchlist_items.currency = historical_watchlist_data.currency ',[auth_user,showwatchlist])
    watchlists = cur.fetchall()
    return watchlists


def get_user_watchlistsname():
    db = get_db()
    auth_user = session.get("username")
    cur = db.execute(
        'select user_watchlists.username, user_watchlists.watchlist_name from user_watchlists where user_watchlists.username = "%s"' % auth_user)
    watchlistsname = cur.fetchall()
    return watchlistsname


def exchange_rate(crypto_currency, monetary_currency):
    data = {}
    currency_convert_from = crypto_currency
    currency_convert_to = monetary_currency
    currency_convert_to_lowercase = currency_convert_to.lower()

    main_api = 'https://api.coinmarketcap.com/v1/ticker/'
    search_currency = currency_convert_from + '/?convert=' + currency_convert_to
    url = main_api + search_currency
    json_data = requests.get(url).json()
    json_convert_price = json_data[0]['price_' + currency_convert_to_lowercase]
    price = float(json_convert_price)
    date_time = time.strftime("%b %d %Y %H:%M:%S")
    data['cypto_currency'] = json_data[0]['name']
    data['monetary_currency'] = currency_convert_to_lowercase
    data['price'] = price
    data['date_time'] = date_time
    return data

def delete_watchlist_method(username,watchlistname):
    db = get_db()
    cur = db.execute(
        'DELETE FROM watchlist_items where watchlist_items.username =? and watchlist_items.watchlist_name =? ',
        [username, watchlistname])
    db.commit()
    cur.fetchall()
    cur.close()
    cur = db.execute(
        'DELETE FROM historical_watchlist_data where historical_watchlist_data.username=? and historical_watchlist_data.watchlist_name =? ',
        [username, watchlistname])
    db.commit()
    cur.fetchall()
    cur.close()
    cur = db.execute(
        'DELETE FROM user_watchlists where user_watchlists.username=? and user_watchlists.watchlist_name =? ',
        [username, watchlistname])
    db.commit()
    cur.fetchall()
    cur.close()


def delete_userwatchlistspair(username,watchlistname,cryptocurrency,currency):
    db = get_db()
    cur = db.execute('DELETE FROM watchlist_items where watchlist_items.username =? and watchlist_items.watchlist_name =? and watchlist_items.cryptocurrency  = ? and watchlist_items.currency   = ?',[username,watchlistname,cryptocurrency,currency ])
    db.commit()
    cur.fetchall()
    cur.close()
    cur = db.execute(
        'DELETE FROM historical_watchlist_data where historical_watchlist_data.username=? and historical_watchlist_data.watchlist_name =? and historical_watchlist_data.cryptocurrency  = ? and historical_watchlist_data.currency   = ?',
        [username,watchlistname, cryptocurrency, currency])
    db.commit()
    cur.fetchall()
    cur.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def add_watchlistname(watchlist_name):
    auth_user = session.get("username")
    if not session['logged_in']:
        abort(401)
    db=get_db()
    db.execute("insert into user_watchlists(username, watchlist_name) values (?,?)", [auth_user, watchlist_name])
    db.commit()


def add_watchlist_pair_method(watchlistname,cryptocurrencyid,currency):
    auth_user = session.get("username")
    watchlistinfo = exchange_rate(cryptocurrencyid,currency)
    if not session['logged_in']:
        abort(401)
    db=get_db()
    db.execute("insert into watchlist_items(username,watchlist_name,cryptocurrency,currency,current_value,current_time) values (?,?,?,?,?,?)",
               [auth_user,watchlistname, cryptocurrencyid, currency, watchlistinfo['price'], watchlistinfo['date_time']])
    cursor = db.execute("select * from historical_watchlist_data, watchlist_items where historical_watchlist_data.old_time <> watchlist_items.current_time and historical_watchlist_data.watchlist_name = watchlist_items.watchlist_name and "
                        "historical_watchlist_data.cryptocurrency = watchlist_items.cryptocurrency and historical_watchlist_data.currency = watchlist_items.currency")
    if len(cursor.fetchall())< 1 :
        db.execute(
            "insert into historical_watchlist_data(username,watchlist_name,cryptocurrency,currency,old_value,old_time) values (?,?,?,?,?,?)",
            [auth_user,watchlistname, cryptocurrencyid, currency, watchlistinfo['price'], watchlistinfo['date_time']])
    db.commit()
    flash('New pair added')


@app.route('/addpair', methods=['GET', 'POST'])
def add_watchlist_pair():
    if not session['logged_in']:
        abort(401)
    else:
        if request.method == 'POST':
            msg = request.form['cryptocurrency'].split(" ")
            cryptocurrencyid=msg[0]
            currency = request.form['currency']
            showwatchlist=msg[1]
            add_watchlist_pair_method(showwatchlist,cryptocurrencyid,currency)
        else:
            showwatchlist = request.args.get("name")
        watchlistsname = get_user_watchlistsname()
        user_watchlist = get_user_watchlists(showwatchlist)
    return render_template("dashboard.html",watchlists=user_watchlist, watchlistsname=watchlistsname,showwatchlist=showwatchlist)


@app.route('/addwatchlist', methods=['GET', 'POST'])
def add_watchlist():
    addwatchlist=1
    if not session['logged_in']:
        abort(401)
    else:
        addwatchlist = 1
        if request.method == 'POST':
            watchlistname = request.form['watchlistname']
            addwatchlist = None
            add_watchlistname(watchlistname)
            flash("add watch list Success!")
    watchlistsname = get_user_watchlistsname()
    return render_template('dashboard.html',watchlistsname=watchlistsname, addwathlist=addwatchlist)


@app.route('/deletewatchlist', methods=['GET', 'POST'])
def delete_watchlist():
    if not session['logged_in']:
        abort(401)
    meg = request.args.get("name").split("_")
    delete_watchlist_method(session['username'], meg[1])
    flash("delete watch list Success!")
    watchlistsname = get_user_watchlistsname()
    return render_template("dashboard.html", watchlistsname=watchlistsname)


@app.route('/deletepair', methods=['GET', 'POST'])
def delete_pair():
    if not session['logged_in']:
        abort(401)
    meg = request.args.get("name").split("_")
    delete_userwatchlistspair(session['username'],meg[0],meg[1],meg[2])
    flash("delete Success!")
    watchlistsname = get_user_watchlistsname()
    user_watchlist = get_user_watchlists(meg[0])
    showwatchlist=meg[0]
    return render_template("dashboard.html", watchlistsname=watchlistsname, watchlists=user_watchlist,showwatchlist=showwatchlist)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        if user and passw:
            db = get_db()
            cur = db.execute("select *  from users where username =? and password=?", [user, passw])
            rows = cur.fetchone()
            cur1 = db.execute("select *  from users where Email =? and password=?", [user, passw])
            rows1 = cur1.fetchone()
            cur2 = db.execute("select username  from users")
            rows2 = cur2.fetchone()
            if rows or rows1:
                session['logged_in'] = True
                session['username'] = user
                flash("Login Success!")
                watchlistsname = get_user_watchlistsname()
                return render_template('dashboard.html',watchlistsname=watchlistsname)
            elif user not in rows2:
              error = 'User not registered'
            else:
              error = 'Incorrect username or password'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    time.sleep(1)
    return redirect(url_for('show_watchlists'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    users = [dict(username=row[0], password=row[1]) for row in get_db().execute('select username, password from users order by username desc').fetchall()]
    registeredmembers=[]
    for i in users:
        registeredmembers.append(i['username'])
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        email = request.form['email']
        cfm_passw = request.form['cfm_password']
        if user in registeredmembers:
            error = 'User already registered'
        elif passw != cfm_passw:
            error = 'Passwords do not match'
        elif len(passw) < 8:
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        elif not re.search("[0-9]", passw):
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        elif not re.search("[A-Z]", passw):
            error = 'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number'
        else:
            get_db().execute('insert into users (username, password, email) values (?, ?, ?)', [user, passw, email])
            get_db().commit()
            session['logged_in'] = True
            flash('You were successfully registered and have been logged in')
            return redirect(url_for('show_watchlists'))
    return render_template('register.html', error=error)


@app.route('/shutdown')
def shutdown():
    if app.environment == 'test':
        shutdown_server()
    return "Server shutdown"


@app.cli.command('start')
def start():
    app.config.from_object(__name__) # load config from this file

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'coinmart.db'),
        SECRET_KEY='Production key',
    ))
    app.config.from_envvar('COINMART_SETTINGS',  silent=True)
    app.run(port=5000)


def test_server():
    ### Setup for integration testing
    app.config.from_object(__name__) # load config from this file

    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'coinmart_test.db'),
        SECRET_KEY='Test key',
        SERVER_NAME='localhost:5006',
        # DEBUG=True, # does not work from behave
    ))
    app.config.from_envvar('COINMART_TEST_SETTINGS',  silent=True)
    app.environment = 'test'
    with app.app_context():
        init_db('test_schema.sql')
    app.run()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with Werkzeug server")
    if app.environment == 'test':
        func()
        os.unlink(app.config['DATABASE'])


if __name__ == '__main__':
    # start()
    # initdb_command()
    app.run(port=5050)