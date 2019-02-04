
import RPi.GPIO as GPIO
import time
import datetime
import csv
import schedule

# Config variables
dev_mode = False
hum_pin = 3
relay_pin = 3
motor_time = 2

# GPIO config, BMC instructions
GPIO.setmode(GPIO.BCM)
# # GPIO Pin setup
GPIO.setup(hum_pin, GPIO.IN)
# GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)


def read_humidity():
    if dev_mode:
        current_hum = 0
        print 'Read humdity in dev: ', current_hum
    else:
        current_hum = GPIO.input(hum_pin)

    # if current_hum < sensor_data[0]:
        # print 'Not higher than before. Check tank for water.'
    save_sensor_data(current_hum)
    return current_hum

# Function for activating the water pump. Default 20 seconds of motor time.
def activate_pump(motor_time=20):
    if dev_mode: print 'activated pump'
    try:
        # Motor runs for x seconds
        GPIO.output(relay_pin, True)
        GPIO.output(relay_pin, False)
        time.sleep(motor_time)
    except Exception as e:
        raise e

def save_sensor_data(humidity):
    timestamp = datetime.datetime.now()
    sensor_data = [0]
    sensor_data.append(timestamp)
    sensor_data.append(humidity)
    with open(r'hum_data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(sensor_data)

def garden_routine():
    humidity = read_humidity()
    if humidity < 10:
        activate_pump()
    else:
        print 'Soil does not need watering.'

if __name__ == '__main__':
    # daily check at 10:30
    schedule.every().day.at("10:30").do(garden_routine)

