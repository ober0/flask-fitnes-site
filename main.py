import checkQR
import secrets
from flask import Flask, render_template, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import webbrowser
import datetime
from sqlalchemy import func

app = Flask(__name__, static_url_path='/static')
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
    summa = db.Column(db.String(100))
    time = db.Column(db.String(100))

    def __repr__(self):
        return '<id %r>' % self.id


class Arrivals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abn_id = db.Column(db.String(80))
    name = db.Column(db.String(100))
    locker_num = db.Column(db.String(80))
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
        arrival = Arrivals(abn_id = request.form['abn_id'], locker_num = request.form.get('locker'), name = request.form['name'], date_arrival = datetime.datetime.now())
        try:
            db.session.add(arrival)
            db.session.commit()
            return redirect(f'/client?id={request.form["abn_id"]}&arrival=success')
        except Exception as e:
            db.session.rollback()
            print(e)
            return 'Ошибка!'
    elif action == 'back':
        return redirect('/')
    elif action == 'edit':
        user = Clients.query.filter_by(id=request.form['id']).first()
        user_data = {
            'id': user.id,
            'name': user.name,
            'phone_number': user.phone_number,
            'date_signing': user.date_signing,
            'activate_date': user.activate_date,
            'freezing': user.freezing,
            'subscription_number': user.subscription_number,
            'summa': user.summa,
            'time': user.time,
        }
        return render_template('edit-user.html', data=user_data)

@app.route('/edit', methods=['POST'])
def edit():
    client = Clients.query.filter_by(subscription_number=request.form['subscription_number']).first()
    client.name = request.form.get('name')
    client.phone_number = request.form['number']
    client.date_signing = request.form['date_signing']
    client.activate_date = request.form['activate_date']
    client.freezing = request.form['freezing']
    client.subscription_number = request.form['subscription_number']
    client.summa = request.form['summa']
    client.time = request.form['time']
    try:
        db.session.commit()
        return redirect(f'/client?id={client.subscription_number}&arrival=success')
    except Exception as e:
        db.session.rollback()
        return e


@app.route('/new_subscription', methods=['POST', 'GET'])
def new_subscription():
    if request.method == 'GET':
        return render_template('new-user.html')
    elif request.method == 'POST':
        client = Clients(name=request.form['name'],
                         phone_number=request.form['number'],
                         date_signing=request.form['date_signing'],
                         activate_date=request.form['activate_date'],
                         freezing=request.form['freezing'],
                         subscription_number=request.form['subscription_number'],
                         summa =request.form['summa'],
                         time = request.form['time']
                         )
        try:
            db.session.add(client)
            db.session.commit()
            return redirect(f'/client?id={request.form["subscription_number"]}&arrival=success')
        except Exception as e:
            db.session.rollback()
            return e
@app.route('/client', methods=['GET'])
def client():
    arrival = request.args.get('arrival')
    if arrival == 'success':
        arrival = 'true'
    else:
        arrival = 'false'
    client_subscription_number = str(request.args.get('id'))
    if request.args.get('table_id'):
        client = Clients.query.filter_by(id=request.args.get('table_id')).all()
    else:
        client = Clients.query.filter_by(subscription_number=client_subscription_number).all()
    if not client:
        res = []
        clients = Clients.query.all()
        for i in clients:
            if client_subscription_number.lower() in i.name.lower():
                res.append(i)

        if len(res) == 0:
            client = None
        else:
            client = res
    if client:
        if len(client) == 1:
            client = client[0]
            data = {
                'id': client.id,
                'name': client.name,
                'phone_number': client.phone_number,
                'date_signing': client.date_signing,
                'activate_date': client.activate_date,
                'freezing': client.freezing,
                'subscription_number': client.subscription_number,
                'summa': client.summa,
                'time': client.time
            }


            return render_template('client.html', data=data, arrival=arrival)
        else:
            datas = []
            for client in client:
                data = {
                    'id': client.id,
                    'name': client.name,
                    'phone_number': client.phone_number,
                    'date_signing': client.date_signing,
                    'activate_date': client.activate_date,
                    'freezing': client.freezing,
                    'subscription_number': client_subscription_number,
                    'summa': client.summa,
                    'time': client.time
                }
                datas.append(data)
            return render_template('clients.html', data=datas, arrival=arrival)
    else:

        return render_template('no-user.html')

@app.route('/delete')
def delete():
    id_to_remove = request.args.get('id')
    client = Clients.query.filter_by(id=id_to_remove).first()
    if client:
        db.session.delete(client)
        db.session.commit()
        return render_template('delete-success.html')
    return redirect('/')


@app.route('/submit_date', methods=['POST'])
def submit_date():
    if 'any_date' not in request.form:
        arrivals = Arrivals.query.order_by(Arrivals.id).all()
        date = request.form['date']
        data = []
        for el in arrivals:
            if el.date_arrival.strftime('%Y-%m-%d') == date:
                data.append(el)
                2000-20-20
        date = date[8:10] + '.' + date[5:7] + '.' + date[0:4]
    else:
        data = Arrivals.query.order_by(Arrivals.id.desc()).all()
        date = 'Все время'


    return render_template('arrival.html', data=data, date=date)



@app.route('/test')
def test():
    clients = Clients.query.all()
    clients_data = [{'id': client.id,
                     'Имя': client.name,
                     'Номер телефона': client.phone_number,
                     'Дата подписания': client.date_signing,
                     'Дата активации': client.activate_date,
                     'Заморозка': client.freezing,
                     'Номер абонемента': client.subscription_number,
                     'Сумма': client.summa,
                     'Время': client.time}
                    for client in clients]
    return jsonify(clients_data)

@app.route('/view_arrivals')
def view_arrivals():
    return render_template('select-date-arrivals.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    qr_thread = threading.Thread(target=check_qr)
    qr_thread.daemon = True
    qr_thread.start()

    #webbrowser.open('http://127.0.0.1:5000')

    app.run(debug=True)
