import checkQR
import secrets
from flask import Flask, render_template, redirect, request, session, abort
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import webbrowser
import datetime

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
    admin = db.Column(db.String(100))

    def __repr__(self):
        return '<id %r>' % self.id


class Arrivals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abn_id = db.Column(db.String(80))
    name = db.Column(db.String(100))
    locker_num = db.Column(db.String(80))
    date_arrival = db.Column(db.DateTime)
    admin = db.Column(db.String(100))

    def __repr__(self):
        return '<id %r>' % self.id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    admin = db.Column(db.String(80))

    def __repr__(self):
        return '<id %r>' % self.id



@app.route('/check_last')
def check_last():
    clients = []
    clients_noNumber = []
    if 'auth_status' in session:
        if session['auth_status'] == 'admin' or session['auth_status'] == 'user':
            clients_db = Clients.query.all()
            for el_full in clients_db:
                el = el_full.activate_date
                phone_number = el_full.phone_number
                if str(el).count('-') == 1:
                    try:
                        year = str(el).split('-')[1].split('.')[2]
                        month = str(el).split('-')[1].split('.')[1]
                        day = str(el).split('-')[1].split('.')[0]
                        year_now = datetime.datetime.utcnow().strftime('%Y')
                        month_now = datetime.datetime.utcnow().strftime('%m')
                        day_now = datetime.datetime.utcnow().strftime('%d')
                        if year == year_now[2:] or year == year_now or (month_now == '12' and int(year) == int(year_now + 1)):
                            if int(day) >= int(day_now):
                                if month == month_now:
                                    if len(str(phone_number)) > 6:
                                        clients.append(el_full)
                                    else:
                                        clients_noNumber.append(el_full)
                            else:
                                if int(month) == (int(month_now) + 1):
                                    if len(str(phone_number)) > 6:
                                        clients.append(el_full)
                                    else:
                                        clients_noNumber.append(el_full)
                    except IndexError:
                        pass
            day_ended = str(int(day_now) - 1)
            if len(day_ended) == 1:
                day_ended = f'0{day_ended}'
            month_ended = str(int(month_now) + 1)
            if len(month_ended) == 1:
                month_ended = f'0{month_ended}'
            year_ended = str(year)
            if len(year_ended) == 2:
                year_ended = f'20{year_ended}'

            for i in clients_noNumber:
                clients.append(i)
            return render_template('table.html',
                                   clients=clients,
                                   day=day_now,
                                   month=month_now,
                                   year=year_now,
                                   day_ended=day_ended,
                                   month_ended=month_ended,
                                   year_ended=year_ended,
                                   isAdmin=session['auth_status'] == 'admin',
                                   name=session['auth_user']
                                   )
    return redirect('/')
def check_qr():
    while True:
        time.sleep(0.3)
        result = checkQR.check_qr()
        if result != None:
            with open('instance/check.txt', 'w') as f:
                f.write('')
            webbrowser.open_new_tab(f'http://127.0.0.1:5000/client?id={result}')


@app.route('/edit-worker', methods=['GET', 'POST'])
def edit_worker():
    if request.method == 'GET':
        if 'auth_status' in session:
            if session['auth_status'] == 'admin':
                return render_template('/edit-worker.html', isAdmin=(session['auth_status'] == 'admin'), users=Users.query.all())
    elif request.method == 'POST':
        id = request.form['name']
        password = request.form['password']
        admin = request.form['admin']

        print(id)
        if id != '1':
            user = Users.query.filter_by(id=id).first()
            user.password = password
            user.admin = admin

            try:
                db.session.commit()
                return render_template('return_page.html',
                                       title='Успешно!',
                                       about=f'Работник {user.name} обновлен!',
                                       href_to_back='/add-worker',
                                       time=5000)
            except Exception as e:
                db.session.rollback()
                return render_template('return_page.html',
                                       title='Ошибка',
                                       about=f'Ошибка базы данных: {e}',
                                       href_to_back='/edit-worker',
                                       time=5000)
        else:
            return render_template('return_page.html',
                                   title='Ошибка',
                                   about=f'Нельзя редактировать Главного администратора',
                                   href_to_back='/edit-worker',
                                   time=5000)
    return redirect('/')
@app.route('/auth', methods=['POST'])
def auth():
    if request.method == "POST":
        id = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(id=id).first()
        if user:
            if user.password == password:
                session['auth_user'] = user.name
                if user.admin == 'yes':
                    session['auth_status'] = 'admin'
                else:
                    session['auth_status'] = 'user'
                return redirect('/')
        return render_template('auth.html', workers=Users.query.all(), not_succ='true')

    return abort(404)

@app.route('/delete-worker', methods=['GET', 'POST'])
def delete_worker():
    if request.method == "GET":
        if "auth_user" in session:
            if session['auth_status'] == 'admin':
                return render_template('delete-worker.html', users=Users.query.all())
            else:
                return redirect('/auth')
        else:
            return redirect('/auth')
    elif request.method == "POST":
        print(1)
        id = request.form['name']
        user = Users.query.filter_by(id=id).first()
        name = user.name

        print(user.id, type(user.id))
        if user.id != 1:
            try:
                db.session.delete(user)
                db.session.commit()
                return render_template('return_page.html',
                                   title='Успешное удаление!',
                                   about=f'Работник {name} успешно удален',
                                   href_to_back='/delete-worker',
                                   time=5000)
            except Exception as e:
                print(e)
        else:
            return render_template('return_page.html',
                                   title='Отклонено!',
                                   about=f'Нельзя удалить главного администратора',
                                   href_to_back='/add-worker',
                                   time=5000)
    return abort(404)


@app.route('/exit_session')
def exit_session():
    session.clear()
    return redirect('/')


@app.route('/add-worker', methods=['GET', 'POST'])
def add_worker():
    if request.method == "GET":
        if 'auth_status' in session and session['auth_status'] == 'admin':
            return render_template('new-worker.html', isAdmin=(session['auth_status'] == 'admin'), userName=session['auth_user'])
    elif request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        admin = request.form['status']

        user = Users(name=name, password=password, admin=admin)

        try:
            db.session.add(user)
            db.session.commit()
            return render_template('return_page.html',
                                   title='Успешное добавление!',
                                   about=f'Работник {name} успешно добавлен',
                                   href_to_back='/',
                                   time=5000)
        except Exception as e:
            db.session.rollback()

    return redirect('/')

@app.route('/')
def index():
    if 'auth_status' in session:
        if session['auth_status'] == 'admin' or session['auth_status'] == 'user':
            admin = str(session['auth_status'] == 'admin')
            print(admin)
            return render_template('index.html', isAdmin=admin, userName=session['auth_user'])
    return render_template('auth.html', workers=Users.query.all())


@app.route('/process', methods=['POST'])
def process():
    action = request.form['action']
    if action == 'arrival':
        arrival = Arrivals(abn_id = request.form['abn_id'], locker_num = request.form.get('locker'), name = request.form['name'], date_arrival = datetime.datetime.now(), admin=session['auth_user'])
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
        if 'auth_status' in session:
            return render_template('edit-user.html', users=Users.query.all(), data=user_data, isAdmin=(session['auth_status'] == 'admin'), userName=session['auth_user'])
        else:
            return render_template('auth.html', workers=Users.query.all())
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
    if request.form.get('admin') != None:
        client.admin = request.form.get('admin')

    try:
        db.session.commit()
        return redirect(f'/client?id={client.subscription_number}&arrival=success')
    except Exception as e:
        db.session.rollback()
        return e


@app.route('/new_subscription', methods=['POST', 'GET'])
def new_subscription():
    if request.method == 'GET':
        if 'auth_status' in session:
            return render_template('new-user.html', isAdmin=(session['auth_status'] == 'admin'), userName=session['auth_user'])
        else:
            return render_template('auth.html', workers=Users.query.all())
    elif request.method == 'POST':
        client = Clients(name=request.form['name'],
                         phone_number=request.form['number'],
                         date_signing=request.form['date_signing'],
                         activate_date=request.form['activate_date'],
                         freezing=request.form['freezing'],
                         subscription_number=request.form['subscription_number'],
                         summa =request.form['summa'],
                         time = request.form['time'],
                         admin = session['auth_user']
                         )
        try:
            db.session.add(client)
            db.session.commit()
            return redirect(f'/client?id={request.form["subscription_number"]}&arrival=success')
        except Exception as e:
            db.session.rollback()
            print(e)
            return ''
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
                'time': client.time,
                'admin': client.admin
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
                    'time': client.time,
                    'admin': client.admin
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
        arrivals = Arrivals.query.order_by(Arrivals.id.desc()).all()
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

    if 'auth_status' in session:
        return render_template('arrival.html', data=data, date=date, isAdmin=(session['auth_status'] == 'admin'), userName=session['auth_user'])
    return render_template('auth.html', workers=Users.query.all())



@app.route('/view_arrivals')
def view_arrivals():
    if 'auth_status' in session:
        return render_template('select-date-arrivals.html', isAdmin=(session['auth_status'] == 'admin'), userName=session['auth_user'])
    else:
        return redirect('/')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    qr_thread = threading.Thread(target=check_qr)
    qr_thread.daemon = True
    qr_thread.start()

    #webbrowser.open('http://127.0.0.1:5000')

    app.run(debug=True)
