import json
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from blueprint_basket.route import blueprint_market
from blueprint_assign.route import blueprint_assign
from flask import Flask, render_template, session, redirect, url_for
from access import login_req, group_req

app = Flask(__name__)

with open('data_files/db_config.json') as file:
    app.config['db_config'] = json.load(file)

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/order')
app.register_blueprint(blueprint_assign, url_prefix='/assign')

with open('data_files/access.json') as file:
    app.config['access_config'] = json.load(file)
with open('data_files/cache.json') as file:
    app.config['cache'] = json.load(file)

app.secret_key = 'key'


@app.route('/')
def main_menu():
    # return render_template('main_menu.html')
    return render_template('index.html')


@app.route('/query')
@login_req
def request_menu():
    return render_template('request_menu.html')


@app.route('/report')
@login_req
def insert():
    return render_template('reports_menu.html')


@app.route('/basket')
@login_req
def basket():
    return render_template('market.html')


@app.route('/exit')
@login_req
def ex():
    session.pop("user_id")
    session.clear()
    return redirect(url_for('main_menu'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
