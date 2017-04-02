'''
'''

from flask import Flask, render_template, request
import app as meteoapp


app = Flask(__name__)


@app.route('/')
def index():
    '''
    '''
    data = meteoapp.get_data()
    return render_template('index.html', title='Home', temp=data['temp'], hum=data['hum'], time=data['time'])


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0')
