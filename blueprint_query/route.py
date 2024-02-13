import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider
from access import login_req, group_req


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/price', methods=['GET', 'POST'])
def auto(): # контроллер авторизации
    if request.method == 'GET':
        return render_template('login.html')

    login = request.form.get('login')
    password = request.form.get('password')
    _sql = provider.get('auto.sql', login=login, password=password)
    user = select_dict(current_app.config['db_config'], _sql)
    if login and password:
        if user:
            # flash("You registered successfully", "success")
            user = user.pop()
            session['user_id'] = user['login']
            session['uss_id'] = user['id']
            session['id_pass'] = user['id_pass']
            print(session['uss_id'])
            session['user_group'] = user['group']
            return redirect(url_for('main_menu'))
        else:
            return render_template('no_user.html')
    else:
        return render_template('login.html', msg="Вы не до конца ввели данные!")


@blueprint_query.route('/', methods=['GET', 'POST'])
@group_req
def request_1():
    if request.method == 'GET':
        return render_template('request.html')

    date = request.form.get('date')
    _sql = provider.get('request1.sql', date=date)
    tickets = select_dict(current_app.config['db_config'], _sql)
    num_tickets = len(tickets)

    if date:
        if tickets:
            # return render_template('dynamic.html', doctors=doctors)
            return render_template('request.html', tickets=tickets, date=date, num_tickets=num_tickets)
        else:
            return render_template('request.html', msg="Билетов не найдено")
    else:
        return render_template('request.html', msg='Вы не ввели число дней.')


@blueprint_query.route('/request2', methods=['GET', 'POST'])
@group_req
def request_2():
    if request.method == 'GET':
        return render_template('request2.html')

    naming = request.form.get('naming')
    _sql = provider.get('request2.sql', naming=naming)
    flights = select_dict(current_app.config['db_config'], _sql)

    if naming:
        if flights:
            num_flights = len(flights)
            return render_template('request2.html', flights=flights, num_flights=num_flights)
        else:
            return render_template('request2.html', msg="Таких рейсов не найдено.")
    else:
        return render_template('request2.html', msg="Вы не ввели номер рейса.")


@blueprint_query.route('/request3', methods=['GET', 'POST'])
@group_req
def request_3():
    _sql = provider.get('dates.sql')
    dates = select_dict(current_app.config['db_config'], _sql)

    if request.method == 'GET':
        return render_template('request3.html', dates=dates)

    date = request.form.get('date')
    _sql = provider.get('request3.sql', date=date)
    flights = select_dict(current_app.config['db_config'], _sql)

    if flights:
        return render_template('request3.html', flights=flights, dates=dates)
    else:
        return render_template('request3.html', dates=dates)


@blueprint_query.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')

    login = request.form.get('login')
    password = request.form.get('password')
    nm = request.form.get('nm')
    sm = request.form.get('sm')
    if login and password and nm and sm:
        _sql = provider.get('reg.sql', login=login, password=password, nm=nm, sm=sm)
        insert_table(current_app.config['db_config'], _sql)
        return 'Вы успешно зарегистрированы'
    return 'Введены некорректные данные'


@blueprint_query.route('/logout')
@login_req
def logout():
    session.pop('user_id', None)
    # print(session['user_id'])
    return redirect(url_for('main_menu'))