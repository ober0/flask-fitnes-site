import checkQR
import secrets
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import webbrowser
import datetime

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


class Arrivals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abn_id = db.Column(db.String(80))
    date_arrival = db.Column(db.DateTime)
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

@app.route('/process', methods=['POST'])
def process():
    action = request.form['action']
    if action == 'arrival':
        arrival = Arrivals(abn_id = request.form['id'], date_arrival = datetime.datetime.now())
        try:
            db.session.add(arrival)
            db.session.commit()
            return redirect(f'/client?id={request.form["id"]}&arrival=success')
        except Exception as e:
            db.session.rollback()
            print(e)
            return 'Ошибка!'
    elif action == 'back':
        return redirect('/')
    elif action == 'edit':
        user = Clients.query.filter_by(subscription_number=request.form['id']).first()
        user_data = {
            'id': user.id,
            'name': user.name,
            'phone_number': user.phone_number,
            'date_signing': user.date_signing,
            'activate_date': user.activate_date,
            'freezing': user.freezing,
            'subscription_number': user.subscription_number
        }
        return render_template('edit-user.html', data=user_data)

@app.route('/edit', methods=['POST'])
def edit():
    client = Clients.query.filter_by(id=request.form['id']).first()
    client.name = request.form['name']
    client.phone_number = request.form['number']
    client.date_signing = request.form['date_signing']
    client.activate_date = request.form['activate_date']
    client.freezing = request.form['freezing']
    client.subscription_number = request.form['subscription_number']
    try:
        db.session.commit()
        return redirect(f'/client?id={client.subscription_number}&arrival=success')
    except Exception as e:
        db.session.rollback()
        return e

@app.route('/client', methods=['GET'])
def client():
    arrival = request.args.get('arrival')
    client_subscription_number = str(request.args.get('id'))
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
        if arrival == 'success':
            arrival = 'true'
        else:
            arrival = 'false'

        return render_template('client.html', data=data, arrival=arrival)
    else:
        return render_template('no-user.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    qr_thread = threading.Thread(target=check_qr)
    qr_thread.daemon = True
    qr_thread.start()

    #webbrowser.open('http://127.0.0.1:5000')

    app.run(debug=True)
