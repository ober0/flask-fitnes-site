#pip install qrcode


import json
import sqlite3
import qrcode

conn = sqlite3.connect('../create-db/database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM clients")
rows = cursor.fetchall()
for row in rows:
    user = {
        'name': row[1],
        'phone_number': row[2],
        'date_signing': row[3],
        'activate_date': row[4],
        'freezing': row[5],
        'subscription_number': row[6]
    }

    data = json.dumps(user)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=5,
    )
    qr.add_data(data.encode('utf-8'))
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')

    img.save(f'files-qr/qr-for-user-{user["subscription_number"]}.png')