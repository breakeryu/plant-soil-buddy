import os
import sqlite3
import serial
import time
from datetime import datetime

def get_current_time() :
    return f"{datetime.now():%Y-%m-%d %H:%M:%S}"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_FILE_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

conn = sqlite3.connect(DB_FILE_PATH)

c = conn.cursor()

user_data = None

while not user_data :
    print('Enter your username: ', end='')
    username = input()

    t = (username,)

    c.execute('SELECT id, username FROM auth_user WHERE username=?',t)

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

    c.execute('SELECT api_soilprofile.name FROM api_soilprofile JOIN auth_user ON api_soilprofile.owner_id=auth_user.id WHERE username=? AND name=? AND location=?',t)

    soil_profile = c.fetchone()

    if not soil_profile :
        print('Invalid Soil Profile Name and/or Location')

every_minutes = 0

while every_minutes < 0.1 :
    print('Enter how often the sensors will record in every minutes (decimal allowed, 1 hr=60 mins, 1 day=1440 mins): ', end='')
    try:
        every_minutes = float(input())
    except ValueError :
        print('Invalid')
        continue

    if every_minutes <= 0 :
        print('Invalid')
    elif every_minutes < 0.1 :
        print('Too frequent!')

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

        #arduino.close()
               
    except serial.serialutil.SerialException :
        status = 'Disconnected'
        print('Connection Failed.')

t_end = time.time() + (60 * every_minutes)
while True:
    try :
        values = str(arduino.readline()).split(" ")

        moist = int(values[0].split("b'")[1])
        acidity = float(values[1])
        #fertility = int(values[2].split("\\r\\n")[0])

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
        break
    except ValueError :
        print('Disconnected')
        break

    if time.time() >= t_end :
        print('Recording...')
        t = (soil_profile[0], moist, acidity, get_current_time())

        c.execute('INSERT INTO api_sensorrecord (soil_id_id, moist, ph, record_date) VALUES ((SELECT id from api_soilprofile WHERE name=?), ?, ?, ?)',t)
        conn.commit()
        t_end = time.time() + (60 * every_minutes)



#password = getpass.getpass(prompt='Enter your password: ')

#hasher = PBKDF2PasswordHasher()

#salt=None

#if not salt:
#    salt = hasher.salt()


#print(c.fetchone()[0])
#print(hasher.encode(password=password, salt=salt))
#print(hash_password(password))
