from smbus2 import SMBusWrapper
import time

ADDR = 0x27

# measurement request
with SMBusWrapper(1) as bus:
	offset = 0
	data = 0
	bus.write_byte_data(ADDR, offset, data)

time.sleep(0.1)

# read data
with SMBusWrapper(1) as bus:
	offset = 0
	bytes = 4
	data = bus.read_i2c_block_data(ADDR, offset, bytes)

print(data)
print('hello')

# parse data
stat = data[0] >> 6
hum_data = ((data[0] & 0b00111111) << 8) | data[1]
temp_data = (data[2] << 6) | (data[3] >> 2)

# compute hum and temp
hum = hum_data / (2**14 - 2) * 100
temp = temp_data / (2**14 -2) * 165 - 40

print('s={:} h={:.2f} % t={:.2f} C'.format(stat, hum, temp))
