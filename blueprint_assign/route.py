import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_utilities.work_with_db import select_dict, insert_table
from db_utilities.sql_provider import SQLProvider
from access import login_req, group_req


blueprint_assign = Blueprint('bp_assign', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_assign.route('/', methods=['GET', 'POST'])
@group_req
def request_1():
    if request.method == 'GET':
        return render_template('request1.html')

    spec = request.form.get('spec')
    _sql = provider.get('spec.sql', spec=spec)
    doctors = select_dict(current_app.config['db_config'], _sql)

    if doctors:
        # return render_template('dynamic.html', doctors=doctors)
        return render_template('request1.html', doctors=doctors, spec=spec)
    else:
        return render_template('request1.html', msg="Таких докторов не найдено")


@blueprint_assign.route('/assign', methods=['GET', 'POST'])
@group_req
def assign2():
    doctor_id = request.args.get('doctor_id')
    patient_id = request.args.get('patient_id')
    if request.method == 'GET':
        return render_template('assign2.html', doctor_id=doctor_id, patient_id=patient_id)
    date = request.form.get('date')
    _sql = provider.get('schedule.sql', doctor_id=doctor_id, date=date)
    shift = select_dict(current_app.config['db_config'], _sql)
    if shift is None:
        if date and doctor_id and patient_id:
            _sql = provider.get('make_app.sql', doctor_id=doctor_id, pat_id=patient_id, app_date=date)
            insert_table(current_app.config['db_config'], _sql)
            return render_template('assign2.html', title='Страница создания отчетов', msg="Создано успешно!")
    else:
        return render_template('assign2.html', error="Эта дата уже занята!")
