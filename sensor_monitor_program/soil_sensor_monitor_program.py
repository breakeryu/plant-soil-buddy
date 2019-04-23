import os
import psycopg2
import serial
import time
from datetime import datetime

def get_current_time() :
    return f"{datetime.now():%Y-%m-%d %H:%M:%S}"

conn = psycopg2.connect("dbname=plant_soil_buddy user=postgres password=root")

c = conn.cursor()

user_data = None

while not user_data :
    print('Enter your username: ', end='')
    username = input()

    c.execute("SELECT id, username FROM auth_user WHERE username='%s'"%(username))

    user_data = c.fetchone()

    if not user_data :
        print('Invalid Username')

print('Welcome! '+user_data[1])

soil_profile = None

while not soil_profile :
    print('Enter your soil profile name: ', end='')
    name = input()

    print('Enter your soil profile location: ', end='')
    location = input()

    t = (user_data[1], name, location,)

    c.execute("SELECT api_soilprofile.name FROM api_soilprofile JOIN auth_user ON api_soilprofile.owner_id=auth_user.id WHERE username='%s' AND name='%s' AND location='%s'"%t)

    soil_profile = c.fetchone()

    if not soil_profile :
        print('Invalid Soil Profile Name and/or Location')

every_minutes = 0

while every_minutes < 0.1 or every_minutes > 720:
    print('Enter how often the sensors will record in every minutes, decimal allowed, annual plant = [0.1, 30), biennial plant = [30, 60), perennial plant = [60, 720]: ', end='')
    try:
        every_minutes = float(input())
    except ValueError :
        print('Invalid')
        continue

    if every_minutes <= 0 :
        print('Invalid')
    elif every_minutes < 0.1 :
        print('Too frequent!')
    elif every_minutes > 720 :
        print('Too long!')

print('Record every '+str(60 * every_minutes)+' seconds')

status = 'Disconnected'

while not status == 'Connected':
    print('Enter your USB port for Arduino (Example: COM8): ', end='')
    port = input()
    
    try :
        print('Connecting to Arduino Decives...')
        arduino = serial.Serial(port, 9600)

        status = 'Connected'

        print('Connection Success.')

        print('')

        print('You can simply stop by plugging the USB off.')

        print('Now Loading...')
               
    except serial.serialutil.SerialException :
        status = 'Disconnected'
        print('Connection Failed.')

t_end = time.time() + (60 * every_minutes)
while True:
    try :
        values = str(arduino.readline()).split(" ")

        moist = int(values[0].split("b'")[1])
        acidity = float(values[1])
        
        #for last value, use : values[x].split("\\r\\n")[0]

        if moist < 0:
            moist = 0

        if moist > 100:
            moist = 100

        if acidity < 0:
            acidity = 0

        if acidity > 14:
            acidity = 14
            
        print('Moist: '+str(moist)+' % , Acidity: '+str(acidity)+' pH')
            
    except serial.serialutil.SerialException :
        print('Disconnected')
        arduino.close()
        break
    except ValueError :
        print('Disconnected')
        arduino.close()
        break

    if time.time() >= t_end :
        print('Recording...')
        t = (soil_profile[0], moist, acidity, get_current_time(), every_minutes)

        c.execute("INSERT INTO api_sensorrecord (soil_id_id, moist, ph, record_date, record_frequency_min) VALUES ((SELECT id from api_soilprofile WHERE name='%s'), %.2f, %.2f, '%s', %.2f)"%t)
        conn.commit()
        t_end = time.time() + (60 * every_minutes)


