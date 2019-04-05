from datetime import datetime as dt

import pytz


def from_now_to_datetime_utc(duration):
    timestamp = (unix_time_millis_whitout_timestamp(dt.now()) - duration)
    date_value = dt.fromtimestamp(timestamp)
    return '{}Z'.format(date_value.strftime('%Y-%m-%dT%H:%M:%S'))


def unix_time_millis_whitout_timestamp(date):
    return int((date - dt.utcfromtimestamp(0)).total_seconds())


def datetime_to_utc(value):
    date_value = dt.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
    utc_date = date_value.astimezone(pytz.utc)
    return '{}Z'.format(utc_date.strftime('%Y-%m-%dT%H:%M:%S'))


def fixed_timestamp_to_seconds(value):
    parsed_datetime = dt.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
    return to_seconds(parsed_datetime)


def from_now_to_seconds(value):
    return to_seconds_naive(now()) - duration_to_seconds(value)


def duration_to_seconds(duration):
    time_units = duration.lower().split('+')
    total_seconds = 0
    for t_unit in time_units:
        total_seconds = total_seconds + convert_time_unit(t_unit)
    return total_seconds


def convert_time_unit(time_unit):
    value, unit = time_unit[:-1], time_unit[-1:]
    return int(value) * unit_in_seconds(unit.lower().strip())


def unit_in_seconds(unit):
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


def to_seconds(value):
    unix_epoch = dt.fromtimestamp(0, tz=value.tzinfo)
    time_delta = value - unix_epoch
    return int(time_delta.total_seconds())


def to_seconds_naive(value):
    naive_unix_epoch = dt.utcfromtimestamp(0)
    time_delta = value - naive_unix_epoch
    return int(time_delta.total_seconds())


def now():
    return dt.now()
