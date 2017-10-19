'''
Webserver and API for Raspberry Pi meteo station.

Script create webserver (Flask); temp and hum data and plots are presented.
'''

from flask import Flask, render_template, request
import app as meteoapp
import sqlite3
import simplejson as json


app = Flask(__name__)


@app.route('/')
def index():
    '''
    The main page containing text and graphical data.
    '''
    # data = meteoapp.get_data()
    # return render_template('index.html', title='Home', temp=data['temp'], hum=data['hum'], time=data['time'])
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM meteo ORDER BY date DESC LIMIT 1')
    r = c.fetchone()
    return render_template('index.html', title='Home', temp=r['temp'], hum=r['hum'], time=r['date'])
    c.close()


@app.route('/api')
def api():
    '''
    API, data in JSOM format.
    '''
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM meteo ORDER BY date DESC LIMIT 1')
    r = c.fetchone()
    # return '{:.1f}'.format(r['temp'])
    return json.dumps({'data': {'date': r['date'], 'temp': r['temp'], 'hum': r['hum']}}), {'Content-Type': 'application/json'}
    c.close()


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', debug=True)
