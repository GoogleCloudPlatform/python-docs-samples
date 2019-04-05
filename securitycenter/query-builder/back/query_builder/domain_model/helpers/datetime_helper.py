from datetime import datetime as dt

import pytz


def datetime_to_utc(value):
    date_value = dt.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
    utc_date = date_value.astimezone(pytz.utc)
    return utc_date.strftime('%Y-%m-%dT%H:%M:%S')


def from_now_to_datetime_utc(duration):
    timestamp = (_unix_time_millis_without_timestamp(dt.now()) - duration)
    date_value = dt.fromtimestamp(timestamp)
    return date_value.strftime('%Y-%m-%dT%H:%M:%S')


def duration_to_seconds(duration):
    time_units = duration.lower().split('+')
    total_seconds = 0
    for t_unit in time_units:
        total_seconds = total_seconds + _convert_time_unit(t_unit)
    return total_seconds


def _convert_time_unit(time_unit):
    value, unit = time_unit[:-1], time_unit[-1:]
    return int(value) * _unit_in_seconds(unit.lower().strip())


def _unit_in_seconds(unit):
    if unit == 'w':
        return 7*24*60*60
    if unit == 'd':
        return 24*60*60
    if unit == 'h':
        return 60*60
    if unit == 'm':
        return 60
    if unit == 's':
        return 1


def _unix_time_millis_without_timestamp(date):
    return int((date - dt.utcfromtimestamp(0)).total_seconds())
