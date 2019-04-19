from datetime import datetime, timedelta
from timeutils import one_month_ago, to_minutes
from dataclasses import dataclass


on_types = {
    'ON',
    'ON LOW',
    'ON MID',
    'ON HIGH'
}
off_types = {
    'OFF',
}
event_types = on_types | off_types

def determine_event_runtime(events: dict, *, since: datetime = one_month_ago()) -> dict():
    usage_map = dict()
    for row in sorted(events, key=lambda item: item['at']):
        if row['uuid'] not in usage_map:
            usage_map[row['uuid']] = {
                'runtime': timedelta(0),
                'last_timestamp': since
            }

        if row['event'] in on_types:
            usage_map[row['uuid']]['last_timestamp'] = row['at']
        else:
            usage_map[row['uuid']]['runtime'] += row['at'] - usage_map[row['uuid']]['last_timestamp']

    return {uuid:val['runtime'] for uuid, val in usage_map.items()}
