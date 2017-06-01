'''
Main application of Raspberry Pi meteo station.

App read data from I2C hum/temp senosr, save data to SQLite database and generate plots.
'''

from smbus2 import SMBusWrapper
import time
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

ADDR = 0x27


def get_hih8120_data():
    '''
    Get humidity and temperature data from HIH8120 sensor (I2C)
    '''
    # measurement request
    with SMBusWrapper(1) as bus:
        offset = 0
        data = 0
        bus.write_byte_data(ADDR, offset, data)

    # wait
    time.sleep(0.1)

    # read data
    with SMBusWrapper(1) as bus:
        offset = 0
        bytes = 4
        data = bus.read_i2c_block_data(ADDR, offset, bytes)

    pdata = parse_hih8120_data(data)
    return pdata


def parse_hih8120_data(data):
    '''
    Parse and convert hum and temp data to physical units.
    '''
    # parse data
    stat = data[0] >> 6
    hum_data = ((data[0] & 0b00111111) << 8) | data[1]
    temp_data = (data[2] << 6) | (data[3] >> 2)

    # compute hum and temp
    hum = hum_data / (2**14 - 2) * 100
    temp = temp_data / (2**14 - 2) * 165 - 40

    return {'hum': hum, 'temp': temp}


def get_data():
    '''
    Get all meteo data, intended for API call.

    Return dict containing 'time', 'temp' and 'hum'.
    '''
    pdata = get_hih8120_data()
    pdata['time'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    return pdata


def save_to_txt(pdata):
    '''
    Save data to a flat file.
    '''
    print('{:}\t{:.2f}\t{:.2f}'.format(pdata['time'], pdata['hum'], pdata['temp']), file=open('log.txt', 'a'))


def save_to_db(pdata):
    '''
    Save data to database.
    '''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO meteo VALUES (?,?,?)''', (pdata['time'], pdata['temp'], pdata['hum']))
    conn.commit()
    conn.close()


def generate_plot():
    '''
    Generate plot from the temp and hum data of current day.

    The data is read from the database.
    '''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    temp = []
    hum = []
    time = []
    # for row in c.execute("SELECT * FROM meteo WHERE date > date('now', '-10 minutes')"):
    for row in c.execute('''SELECT * FROM meteo WHERE date > date('now', 'start of day') '''):
        # print(row)
        datetime_object = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S')
        time.append(datetime_object)
        temp.append(row[1])
        hum.append(row[2])
    conn.close()

    # dates = matplotlib.dates.date2num(time)
    plt.clf()
    plt.plot(time, temp, 'ro', markersize=1, label='temp')
    plt.plot_date(time, hum, 'bo', markersize=1, label='hum')
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    # plt.title('Temperature and humidity data')
    plt.legend(loc=2)
    plt.savefig('static/plot.png')


def print_data_from_db():
    '''
    Print last temp and hum data to the terminal.

    The data is read from the database.
    '''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # for row in c.execute('''SELECT * FROM meteo WHERE date > date('now', 'start of day') '''):
    #     print(row)
    c.execute('SELECT * FROM meteo ORDER BY date DESC LIMIT 1')
    r = c.fetchone()
    print(r)
    conn.close()


def main():
    '''
    Main application.
    '''

    # Initialize database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS meteo (date text, temp real, hum real)''')
    conn.close()

    # matplotlib.use('Agg')
    # fig, ax = matplotlib.pyplot.subplots( nrows=1, ncols=1 )  # create figure & 1 axis

    while True:
        pdata = get_data()
        # c.execute('''INSERT INTO meteo VALUES (?,?,?)''', (pdata['time'], pdata['temp'], pdata['hum']))
        # conn.commit()
        # save_to_txt(pdata)
        save_to_db(pdata)
        generate_plot()
        print_data_from_db()

        time.sleep(60)


if __name__ == '__main__':
    main()
