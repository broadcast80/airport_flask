import os
from datetime import datetime
from flask import render_template, Blueprint, request, current_app, session, url_for, redirect, flash
from db_utilities.sql_provider import SQLProvider
from db_utilities.work_with_db import select_dict, insert_table
from access import group_req
from pymysql import OperationalError

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/create', methods=['GET', 'POST'])
@group_req
def create_report():

    sql1 = provider.get('first_date.sql')
    date1 = select_dict(current_app.config['db_config'], sql1)

    sql2 = provider.get('second.sql')
    print(sql2)
    date2 = select_dict(current_app.config['db_config'], sql2)
    print(date2)

    if request.method == 'GET':
        return render_template('create_report.html', title='CREATE REPORT', date1=date1, date2=date2)

    first_date = request.form.get('date1')
    second_date = request.form.get('date2')

    if first_date and second_date:
        if first_date > second_date:
            return render_template('create_report.html', title='Error', date1=date1, date2=date2,
                                   msg="Первая дата должна быть меньше первой!")
        else:
            try:
                datetime.strptime(first_date, '%Y-%m-%d')
                datetime.strptime(second_date, '%Y-%m-%d')
                _sql = provider.get('create_report.sql', start=first_date, end=second_date)
                insert_table(current_app.config['db_config'], _sql)

                return render_template('create_report.html', title='Страница создания отчетов', date1=date1,
                                       date2=date2, msg="Отчет успешно создан")
            except ValueError:
                return render_template('create_report.html', date1=date1, date2=date2, msg="Неправильный формат даты")
    else:
        return render_template('create_report.html', date1=date1, date2=date2, msg="Не все данные были введены")


@blueprint_report.route('/view', methods=['GET', 'POST'])
@group_req
def view_report():
    _sql = provider.get('second_date.sql')
    date1 = select_dict(current_app.config['db_config'], _sql)
    date2 = select_dict(current_app.config['db_config'], _sql)

    if request.method == 'GET':
        return render_template('view_report.html', title="Страница поиска отчетов", date1=date1, date2=date2)

    first_date = request.form.get('date1')
    second_date = request.form.get('date2')

    if first_date and second_date:
        if first_date > second_date:
            return render_template('view_report.html', title='Error', date1=date1, date2=date2, msg="Первая дата должна быть меньше первой!")
        else:
            _sql = provider.get('view_report.sql', start=first_date, end=second_date)
            reports = select_dict(current_app.config['db_config'], _sql)
            return render_template('view_report.html', title="Страница поиска отчетов", reports=reports, date1=date1, date2=date2)

    else:
        return render_template('view_report.html', date1=date1, date2=date2, msg="Не все данные были введены")
