import checkQR
import secrets
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = secrets.token_hex(16)

db = SQLAlchemy(app)

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(80))
    date_signing = db.Column(db.String(100))
    activate_date = db.Column(db.String(100))
    freezing = db.Column(db.String(100))
    subscription_number = db.Column(db.String(100))

    def __repr__(self):
        return '<id %r>' % self.id

def check_qr():
    while True:
        time.sleep(0.3)
        result = checkQR.check_qr()
        if result != None:
            with open('instance/check.txt', 'w') as f:
                f.write('')
            webbrowser.open_new_tab(f'http://127.0.0.1:5000/client?id={result}')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client', methods=['GET'])
def client():
    client_subscription_number = str(request.args.get('id'))
    print(client_subscription_number, type(client_subscription_number))
    client = Clients.query.filter_by(subscription_number=client_subscription_number).first()
    if client:
        data = {
            'id': client.id,
            'name': client.name,
            'phone_number': client.phone_number,
            'date_signing': client.date_signing,
            'activate_date': client.activate_date,
            'freezing': client.freezing,
            'subscription_number': client_subscription_number
        }
        return render_template('client.html', data=data)
    else:
        return render_template('no-user.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    qr_thread = threading.Thread(target=check_qr)
    qr_thread.daemon = True
    qr_thread.start()

    webbrowser.open('http://127.0.0.1:5000')

    app.run(debug=True)
