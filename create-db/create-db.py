#pip install openpyxl pandas
from http import client

import pandas as pd
import sqlite3

file = 'file.xlsx'

df = pd.read_excel(file)
data = df.to_dict('records')

conn = sqlite3.connect('../instance/database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clients
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
phone_number TEXT,
date_signing TEXT,
activate_date TEXT,
freezing TEXT,
subscription_number TEXT,
summa TEXT,
time TEXT
)''')





for i in data:
    print(i)
    name = i['ФИО']
    if name == 'nan' or name == None:
        name = 'None'

    phone_number = i['НОМЕР ТЕЛЕФОНА']
    if phone_number == 'nan' or phone_number == None:
        phone_number = 'None'

    try:
        date_signing = i['ДАТА ПОДПИСАНИЯ'].strftime('%d.%m.%Y')
    except:
        date_signing = 'None'
    if date_signing == 'nan' or date_signing == None:
        date_signing = 'None'

    activate_date = str(i['ДАТА АКТИВАЦИИ'])
    if activate_date == 'nan' or activate_date == None:
        activate_date = 'None'
    if '00:00:00' in activate_date:
        activate_date = activate_date.replace('00:00:00', '')

    subscription_number = i['НОМЕР АБН']
    if subscription_number == 'nan' or subscription_number == None:
        subscription_number = 'None'
    try:
        freezing = str(i['ЗАМОРОЗКА'])
        if freezing == 'nan' or freezing == None :
            freezing = 'None'
    except:
        freezing = ''
    try:
        summa = str(i['СУММА'])
        if summa == 'nan' or summa == None:
            summa = 'None'
    except:
        summa = 'None'
    try:
        time = str(i['ВРЕМЯ'])
        if time == 'nan' or time == None:
            time = 'None'
    except:
        time = 'None'

    user = {
        'name': name,
        'phone_number': phone_number,
        'date_signing': date_signing,
        'activate_date': activate_date,
        'freezing': freezing,
        'subscription_number': subscription_number,
        'summa': summa,
        'time': time
    }

    try:
        cursor.execute('''
        INSERT INTO clients(name, phone_number, date_signing, activate_date, freezing, subscription_number, summa, time) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (user['name'],
                        user['phone_number'],
                        user['date_signing'],
                        user['activate_date'],
                        user['freezing'],
                        user['subscription_number'],
                        user['summa'],
                        user['time']
                        ))
    except Exception as e:
        print(e, "\n", user)

conn.commit()
conn.close()

