import re
from datetime import datetime
from psycopg2._psycopg import connection
from psycopg2.sql import SQL

from device import get_power_and_water_usage


event_columns = ['uuid', 'event', 'at']
device_columns = ['uuid', 'name', 'device_type', 'power_usage', 'water_usage', 'location']
room_data_columns = ['name', 'icon', 'target_id']
house_state_columns = ['uuid','language','inside_temp', 'desired_temp', 'rooms']


def execute(db: connection, query: str, args: tuple) -> None:
    with db, db.cursor() as cur:
        cur.execute(query, args)


def execute_and_get_row(db: connection, query: str, args: tuple, keys: list) -> str:
    with db, db.cursor() as cur:
        cur.execute(query, args)
        reply = cur.fetchone()
    return {key: value for key, value in list(zip(keys, reply))}


def execute_and_get_rows(db: connection, query: str, args: tuple, keys: list) -> list:
    rows = list()
    with db, db.cursor() as cur:
        cur.execute(query, args)
        reply = cur.fetchone()
        while reply:
            row = {key: value for key, value in list(zip(keys, reply))}
            rows.append(row)
            reply = cur.fetchone()
    return rows


def set_language(db: connection, new_language: str, uuid: str) -> dict:
    query = ('UPDATE house_state SET language = %s where id = %s'
             ' RETURNING language')
    args = (new_language, uuid)
    return execute_and_get_row(db, query, args, ['language'])


def get_language(db: connection, uuid: str) -> str: #notably not a dict
    query = ('SELECT language FROM house_state WHERE id = %s')
    args = (uuid,)
    return execute_and_get_row(db, query, args, ['language'])['language']


def add_device(db: connection, name: str, device_type: str, location: str = None) -> dict:
    #NOTE: the id column defaults to a (mostly)random uuid, so we don't give one
    query = ('INSERT INTO device (name, device_type, power_usage, water_usage, location)'
             ' VALUES (%s, %s, %s, %s, %s)'
             ' RETURNING *')
    device_type = device_type.upper() #just to make sure
    power_usage, water_usage = get_power_and_water_usage(device_type)
    args = (name, device_type, power_usage, water_usage, location)
    return execute_and_get_row(db, query, args, device_columns)


def remove_device(db: connection, uuid: str) -> dict:
    cleanup_query = 'DELETE FROM device_event WHERE id = %s'
    args = (uuid,)
    execute(db, cleanup_query, args)
    query = 'DELETE FROM device WHERE id = %s RETURNING *'
    return execute_and_get_row(db, query, args, device_columns)


def get_device(db: connection, *, uuid: str = None) -> list:
    query = 'SELECT * FROM device'
    if uuid is not None and len(uuid) > 0:
        query += ' WHERE (id = %s)'
        args = (uuid,)
    else:
        args = tuple()
    query += ' ORDER BY location, name'
    return execute_and_get_rows(db, query, args, device_columns)


def get_events(db: connection, *,
               uuid: str = None,
               from_ts: datetime,
               to_ts: datetime) -> list:
    query = ('SELECT device.id, at, device_type, event, name, location'
             ' FROM device_event'
             ' INNER JOIN device'
             ' ON device.id = device_event.id'
             ' WHERE (at >= %s) AND (at <= %s)')
    if uuid is not None and len(uuid) > 0:
        query += ' AND (device.id = %s)'
        args = (from_ts, to_ts, uuid)
    else:
        args = (from_ts, to_ts)

    return execute_and_get_rows(db, query, args, ['uuid', 'at', 'device_type',
                                                  'event', 'name', 'location'])


def add_event(db: connection,
              uuid: str,
              event: str,
              at: datetime) -> dict:
    query = ('INSERT INTO device_event (id, event, at)'
             ' VALUES (%s, %s, date_trunc(\'minute\', %s))'
             ' RETURNING *')
    event = event.upper()
    args = (uuid, event, at)
    return execute_and_get_row(db, query, args, event_columns)


def remove_event(db: connection, uuid: str, at: datetime) -> dict:
    query = ('DELETE FROM device_event WHERE (id, at) = (uuid %s, timestamp %s)'
             ' RETURNING *')
    args = (uuid, at)
    return execute_and_get_row(db, query, args, event_columns)


def get_device_state(db: connection, uuid: str) -> list:
    query = ('SELECT DISTINCT ON (id) device.id, name, location, event, at'
             ' FROM device_event'
             ' INNER JOIN device ON device.id = device_event.id'
             ' WHERE at <= now()')
    if uuid is not None and len(uuid) > 0:
        query += ('AND device.id = uuid %s')
        args = (uuid,)
    else:
        args = tuple()
    query += (' ORDER BY id, at DESC')
    return execute_and_get_rows(db, query, args, ['uuid', 'name', 'location', 'event', 'at'])


def get_room(db: connection, *, name: str = None) -> list:
    query = 'SELECT * FROM room_data'
    if name is not None and len(name) > 0:
        query += ' WHERE (name = %s)'
        args = (name,)
    else:
        args = tuple()
    return execute_and_get_rows(db, query, args, room_data_columns)


def add_new_room_type(db: connection,
                      name: str,
                      icon: str) -> dict:
    query = ('INSERT INTO room_data'
             ' VALUES (%s, %s, %s)'
             ' RETURNING *')
    target_id = re.sub(r'[^\w]', '', name)
    args = (name, icon, target_id)
    return execute_and_get_row(db, query, args, room_data_columns)


def add_room_to_house(db: connection,
                      room: str,
                      uuid: str) -> dict:
    query = ('UPDATE house_state'
             ' SET rooms = rooms || %s'
             ' WHERE id = %s'
             ' RETURNING *')
    args = ([room], uuid) # list converts to psql array
    return execute_and_get_row(db, query, args, house_state_columns)


def get_house_state(db: connection, uuid: str) -> list:
    query = ('SELECT * FROM house_state'
             ' WHERE id = %s')
    args = (uuid,)
    return execute_and_get_rows(db, query, args, house_state_columns)

