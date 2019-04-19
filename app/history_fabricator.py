#!/usr/bin/env python3
from sql_connect import connect_with_config
from fileio import load_yml_to_dict

config = load_yml_to_dict('config.yml')
db_connection = connect_with_config(config)
assert db_connection

import argparse
import functools
import datetime

from datetime import datetime, timedelta, time
from random import randint, choice
import sql


busy_hours_start = time(7, 30, 0, 0)
busy_hours_end = time(16, 0, 0, 0)
start_of_adult_day = timedelta(hours=5)
end_of_working_hours = timedelta(hours=16, minutes=0)
weekday_working_hours = end_of_working_hours - timedelta(hours=7, minutes=30)
total_weekday_hours = timedelta(hours=22, minutes=30) - start_of_adult_day
total_weekday_hours -= weekday_working_hours
total_weekend_hours = timedelta(hours=20, minutes=30) - timedelta(hours=6, minutes=0)

weekends = {6, 7}
skip_day = {3}


def _contains_room_and_name(args, _dict) -> bool:
    values = _dict.values()
    return args.room in values and args.name in values


def each_datetime_across(from_ts: datetime, until_ts: datetime) -> datetime:
    current_day = from_ts
    one_day = timedelta(days=1)
    while current_day <= until_ts: #NOTE: inclusive
        yield current_day
        current_day += one_day


def main(args):
    devices = sql.get_device(db_connection)
    contains_room_and_name = functools.partial(_contains_room_and_name, args)
    match = list(filter(contains_room_and_name, devices))[0]
    assert match, f'No matches for {args.room}, {args.name}'
    for date in each_datetime_across(args.from_ts, args.until_ts):
        if args.four and date.isoweekday() in skip_day | weekends:
            continue
        if date.isoweekday() not in weekends:
            count = args.mf_count
            duration = timedelta(minutes=args.mf_duration)
            usable_hours = total_weekday_hours
            weekday = True
        else:
            count = args.ss_count
            duration = timedelta(minutes=args.ss_duration)
            usable_hours = total_weekend_hours
            weekday = False
        date += start_of_adult_day
        time_offset = (usable_hours-duration) / count
        for point in range(0, count):
            jitter = timedelta(minutes = randint(0, duration.seconds // 60))
            date += time_offset + jitter
            in_work_hours = (busy_hours_start <= (date - duration).time() and
                             date.time() <= busy_hours_end)
            if weekday and in_work_hours:
                date = datetime.combine(date.date(), busy_hours_end) + jitter

            if match['device_type'] == 'BULB':
                state = choice(['ON LOW', 'ON MID', 'ON HIGH'])
            else:
                state = 'ON'

            if not args.test:
                print(sql.add_event(db_connection, match['uuid'], state, date))
                print(sql.add_event(db_connection, match['uuid'], 'OFF', date + duration))
            else:
                print(f' {state} at {date}')
                print(f'OFF at {date+duration}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool to help generate device history.')
    parser.add_argument(
        'room',
        type=str,
        help='The room the device is in',
        metavar='ROOM')
    parser.add_argument(
        'name',
        type=str,
        help='The device to build events for',
        metavar='DEVICE')
    parser.add_argument(
        '--from',
        dest='from_ts',
        type=datetime.fromisoformat,
        help='When to start building history from',
        metavar='ISO_DATE')
    parser.add_argument(
        '--until',
        dest='until_ts',
        type=datetime.fromisoformat,
        help='When (inclusive) to stop building history at',
        metavar='ISO_DATE')
    parser.add_argument(
        '--mf-count',
        dest='mf_count',
        type=int,
        help='How many events occur on Monday-Friday',
        metavar='NUM')
    parser.add_argument(
        '--ss-count',
        dest='ss_count',
        type=int,
        help='How many events occur on Saturday-Sunday',
        metavar='NUM')
    parser.add_argument(
        '--mf-duration',
        dest='mf_duration',
        type=int,
        help='How long (in minutes) events last on Monday-Friday',
        metavar='MIN')
    parser.add_argument(
        '--ss-duration',
        dest='ss_duration',
        type=int,
        help='How long (in minutes) events last on Saturday-Sunday',
        metavar='MIN')
    parser.add_argument(
        '--four',
        dest='four',
        default=False,
        type=bool,
        help='Special flag for things that run four times a week',
        metavar='BOOL')
    parser.add_argument(
        '--test',
        dest='test',
        default=False,
        type=bool,
        help='Show times to insert at, but don\' interact with the DB',
        metavar='BOOL')
    args = parser.parse_args()
    main(args)
