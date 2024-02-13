import os
import json
from datetime import timedelta
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from db_utilities.work_with_db import select, insert, select_dict
from db_utilities.sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache
from access import login_req, group_req
from datetime import datetime

blueprint_market = Blueprint('bp_market', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/market', methods=['GET', 'POST'])
@login_req
def index():
    basket_items = session.get('basket', {})

    _sql = provider.get('all_items.sql')
    flights = select_dict(current_app.config['db_config'], _sql)
    print(flights)
    return render_template('market_index.html', flights=flights, basket_items=basket_items)


@blueprint_market.route('/', methods=['GET', 'POST'])
@login_req
def market_index():
    configDB = current_app.config['db_config']
    cache_config = current_app.config['cache']
    cached_func = fetch_from_cache('all_items_cached', cache_config)(select)
    # schedule_id = request.args.get('schedule_id')
    # print(schedule_id)
    user_id = request.args.get('id_pass')
    schedule_id = request.args.get('schedule_id')
    print(schedule_id)

    if request.method == 'GET':
        sql = provider.get('seats.sql', id_schedule=schedule_id)
        # items = cached_func(configDB, sql)
        seats = select_dict(current_app.config['db_config'], sql)
        print("there are seats:")
        print(seats)
        basket_items = session.get('basket', {})
        return render_template('seats.html', title='Маркет', seats=seats, basket_items=basket_items)
    else:
        # seat_number = request.form['number']
        prod_id = request.form['prod_id']
        sql = provider.get('all_seats.sql')
        items = cached_func(configDB, sql)

        item_description = []
        for i in range(len(items[0])):
            if str(items[0][i][0]) == str(prod_id):
                print("there are items")
                print(items[0][i])
                item_description.append(items[0][i])

        print("There are item_desctiption")
        print(item_description)
        item_description = item_description[0]
        curr_basket = session.get('basket', {})

        if prod_id in curr_basket:
            return "Место уже занято!"
        else:
            curr_basket[prod_id] = {
                'flight': item_description[3],
                'name': item_description[1],
                'price': item_description[2],
                'date_out': item_description[5],
                'id_schedule': item_description[4]
            }

        print(item_description[5])

        session['basket'] = curr_basket
        session.permanent = True

        sql = provider.get('seats.sql', id_schedule=schedule_id)
        seats = select_dict(current_app.config['db_config'], sql)

        return redirect(url_for('bp_market.market_index', seats=seats))


@blueprint_market.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.index'))


@blueprint_market.route('/checkout', methods=['POST', 'GET'])
def checkout():
    configDB = current_app.config['db_config']
    basket_items = session.get('basket', {})
    id_pass = session['id_pass']

    if request.method == 'GET':
        return render_template('order_details.html', basket_items=basket_items)

    if basket_items:
        order_details = list()
        for item in basket_items.items():
            sql = provider.get('buy_ticket.sql',
                               id_pass=session['id_pass'],
                               pass_pass=request.form.get('passport'),
                               id_schedule=item[1]['id_schedule'],
                               seat=item[1]['name'],
                               fio=request.form.get('fio'))
            insert(configDB, sql)
            order_details.append({
                'id_schedule': item[1]['id_schedule'],
                'price': item[1]['price']
            })
        session.pop('basket')
        return render_template('order_confirmed.html', title='Заказ подтвержден', order_details=order_details)
    else:
        return "Корзина пуста"
    return redirect(url_for('bp_market.market_index'))
