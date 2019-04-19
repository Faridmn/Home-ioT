#!/usr/bin/env python3
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

from sql_connect import connect_with_config
from fileio import load_yml_to_dict

config = load_yml_to_dict('config.yml')
db_connection = connect_with_config(config)
assert db_connection

import json
import sql

from datetime import datetime, timedelta

from timeutils import parse_date_or_get_default, one_month_ago
from serialization import DateTimeEncoder
from device import device_types, compute_usage
from event import on_types, event_types, determine_event_runtime
from calculate import power_to_dollars
from translation import translation, valid_languages


our_house_uuid = '2eaa7e66-2f65-5e16-99d1-7db9b03999ef'


@app.context_processor
def inject_template_globals() -> dict:
    to_inject = {
        'device_types': device_types,
        'event_types': event_types,
        'lang': sql.get_language(db_connection, our_house_uuid),
        'langs': translation.keys(),
        'translation' : translation[sql.get_language(db_connection, our_house_uuid)],
        'rooms' : json.loads(get_room()),
        'devices' : json.loads(get_device()),
        'get_running_cost': get_running_cost,
        'get_device_status': get_device_status,
    }
    return to_inject


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/admin')
def admin() -> str:
    return render_template('admin.html')


@app.route('/history')
def history() -> str:
    return render_template('history.html')


@app.route('/change-locale', methods=['POST'])
def change_locale() -> str:
    new_language = request.form.get('language_code')
    assert new_language in valid_languages, f'{new_language} is not valid'
    reply = sql.set_language(db_connection, new_language, our_house_uuid)
    assert reply
    return json.dumps(reply)


@app.route('/get-device')
def get_device() -> str:
    uuid = request.args.get('uuid')
    devices = sql.get_device(db_connection, uuid=uuid)
    reply = json.dumps(devices)
    return reply


@app.route('/add-device')
def add_device() -> str:
    name = request.args.get('name')
    location = request.args.get('location')
    device_type = request.args.get('device_type')
    assert name and location and device_type
    reply = sql.add_device(db_connection, name, device_type, location)
    assert reply
    return f'Added: {reply}'


@app.route('/remove-device')
def remove_device() -> str:
    uuid = request.args.get('uuid')
    assert uuid
    reply = sql.remove_device(db_connection, uuid)
    assert reply
    return f'Removed: {reply}'


@app.route('/get-device-events')
def get_device_events() -> str:
    uuid = request.args.get('uuid')
    from_ts = parse_date_or_get_default(request.args.get('from_ts'), one_month_ago())
    to_ts = parse_date_or_get_default(request.args.get('to_ts'))
    events = sql.get_events(db_connection, uuid=uuid, from_ts=from_ts, to_ts=to_ts)
    reply = json.dumps(events, cls=DateTimeEncoder)
    return reply


@app.route('/add-event')
def add_event() -> str:
    uuid = request.args.get('uuid')
    event = request.args.get('event')
    at = parse_date_or_get_default(request.args.get('at'))
    assert uuid and event and at
    reply = sql.add_event(db_connection, uuid, event, at)
    assert reply
    return f'Added event: {reply}'


@app.route('/remove-event')
def remove_event() -> str:
    uuid = request.args.get('uuid')
    at = request.args.get('at')
    assert uuid and at
    reply = sql.remove_event(db_connection, uuid, at)
    assert reply
    return f'Removed event: {reply}'


def get_device_runtime(uuid, from_ts, to_ts) -> dict:
    events = sql.get_events(db_connection, uuid=uuid, from_ts=from_ts, to_ts=to_ts)
    runtime = determine_event_runtime(events, since=from_ts)
    return runtime


@app.route('/get-device-runtime')
def dispatch_get_device_runtime() -> str:
    uuid = request.args.get('uuid')
    from_ts = parse_date_or_get_default(request.args.get('from_ts'), one_month_ago())
    to_ts = parse_date_or_get_default(request.args.get('to_ts'))
    runtime = get_device_runtime(uuid, from_ts, to_ts)
    to_encode = {_id:str(val) for _id, val in runtime.items()}
    reply = json.dumps(to_encode, cls=DateTimeEncoder)
    return reply


def get_device_status(uuid: str = None) -> dict:
    return sql.get_device_state(db_connection, uuid)


@app.route('/get-device-state')
def dispatch_get_device_state() -> str:
    uuid = request.args.get('uuid')
    reply = json.dumps(get_device_status(uuid), cls=DateTimeEncoder)
    return reply


@app.route('/get-room')
def get_room() -> str:
    name = request.args.get('name')
    rooms = sql.get_room(db_connection, name=name)
    reply = json.dumps(rooms)
    return reply


@app.route('/add-new-room-type')
def add_new_room_type() -> str:
    name = request.args.get('name')
    icon = request.args.get('icon')
    assert name and icon
    reply = sql.add_new_room_type(db_connection, name, icon)
    assert reply
    return f'Added: {reply}'


@app.route('/add-room-to-house')
def add_room_to_house() -> str:
    room = request.args.get('room')
    house_uuid = request.args.get('house_uuid')
    if house_uuid is None or len(house_uuid) == 0:
        house_uuid = our_house_uuid
    assert room and house_uuid
    reply = sql.add_room_to_house(db_connection, room, house_uuid)
    assert reply
    return f'Added: {reply}'


@app.route('/get-house-state')
def get_house_state() -> str:
    house_uuid = request.args.get('house_uuid')
    if house_uuid is None or len(house_uuid) == 0:
        house_uuid = our_house_uuid
    assert house_uuid
    reply = json.dumps(sql.get_house_state(db_connection, house_uuid))
    return reply


def get_running_cost(uuid: str,
                     device_type: str,
                     power_usage: int,
                     from_ts: str = one_month_ago(),
                     to_ts: str = datetime.now()) -> dict:
    response = get_device_runtime(uuid, from_ts, to_ts)
    if uuid not in response:
        last_state = sql.get_device_state(db_connection, uuid)[0]
        if last_state['event'] in on_types:
            runtime = datetime.now() - last_state['at']
        else:
            runtime = 0
    else:
        runtime = response[uuid]
    usage = compute_usage(device_type, power_usage, runtime)
    return {'power': usage['power'],
            'power_cost': power_to_dollars(usage['power']),
            'water': usage['water']}


@app.route('/get-running-cost')
def dispatch_get_running_cost() -> str:
    power_usage = request.args.get('power_usage')
    device_type = request.args.get('device_type')
    from_ts = parse_date_or_get_default(request.args.get('from_ts'), one_month_ago())
    to_ts = parse_date_or_get_default(request.args.get('to_ts'))
    reply = json.dumps(get_running_cost(device_type, power_usage, from_ts, to_ts))
    return reply

