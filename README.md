# RPiMeteo
## Simple meteo station running on Raspberry Pi

### Web app
![alt text](https://github.com/petrgabrlik/rpimeteo/blob/master/static/screen.PNG "Web app" =700x)

### Hardware
![alt text](https://github.com/petrgabrlik/rpimeteo/blob/master/static/hw.jpg "Hardware" =700x)

# RPiMeteo
## Simple meteo station running on Raspberry Pi
Current version is equipped with the Honeywell HIH8120 humidity/temperature sensor, which is connected to RPi via I2C bus. Program is written in Python 3, it is devided into two files:
- app.py - read data from sensor (smbus2), save to SQLite database (sqlite3), draw a plot (matplotlib) every 60 seconds
- api.py - run a webserver (Flask), read data from the database on every get request

### Web app
<img src="https://github.com/petrgabrlik/rpimeteo/blob/master/static/screen.PNG" width="700">

### Hardware
<img src="https://github.com/petrgabrlik/rpimeteo/blob/master/static/hw.jpg" width="700">
