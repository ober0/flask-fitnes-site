#pip install openpyxl pandas
from http import client

import pandas as pd
import sqlite3

file = 'file.xlsx'

df = pd.read_excel(file)
data = df.to_dict('records')

conn = sqlite3.connect('database.db')
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
subscription_number TEXT
)''')





for i in data:
    print(i)
    name = i['ФИО']
    if name == 'nan' or name == None:
        name = 'None'

    phone_number = i['номер телфона']
    if phone_number == 'nan' or phone_number == None:
        phone_number = 'None'

    try:
        date_signing = i['дата подписания'].strftime('%d.%m.%Y')
    except:
        date_signing = 'None'
    if date_signing == 'nan' or date_signing == None:
        date_signing = 'None'

    activate_date = str(i['дата активации'])
    if activate_date == 'nan' or activate_date == None:
        activate_date = 'None'
    if '00:00:00' in activate_date:
        activate_date = activate_date.replace('00:00:00', '')

    subscription_number = i['номер абонемента']
    if subscription_number == 'nan' or subscription_number == None:
        subscription_number = 'None'

    freezing = str(i['заморозка'])
    if freezing == 'nan' or freezing == None :
        freezing = 'None'

    user = {
        'name': name,
        'phone_number': phone_number,
        'date_signing': date_signing,
        'activate_date': activate_date,
        'freezing': freezing,
        'subscription_number': subscription_number,
    }

    try:
        cursor.execute('''
        INSERT INTO clients(name, phone_number, date_signing, activate_date, freezing, subscription_number) 
        VALUES (?, ?, ?, ?, ?, ?)''',
                       (user['name'], user['phone_number'], user['date_signing'], user['activate_date'],user['freezing'], user['subscription_number']))
    except Exception as e:
        print(e, "\n", user)

conn.commit()
conn.close()

