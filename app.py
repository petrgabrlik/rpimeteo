'''
'''

from smbus2 import SMBusWrapper
import time

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
    temp = temp_data / (2**14 -2) * 165 - 40

    return {'hum': hum, 'temp': temp}


def get_data():
    '''
    Get all meteo data, intended for API call
    '''
    pdata = get_hih8120_data()
    pdata['time'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    return pdata


def save_to_txt(pdata):
    '''
    '''
    print('{:}\t{:.2f}\t{:.2f}'.format(pdata['time'], pdata['hum'], pdata['temp']), file=open('log.txt', 'a'))


def main():
    '''
    '''
    while True:
        # pdata = get_hih8120_data()
        # pdata = parse_hih8120_data(data)
        # pdata['time'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        pdata = get_data()
        save_to_txt(pdata)
        # print('raw: {:}'.format(data))
        # print(time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()))
        print('{:} h={:.2f} % t={:.2f} C'.format(pdata['time'], pdata['hum'], pdata['temp']))
        # print(pdata)
        time.sleep(60)


if __name__ == '__main__':
    main()
