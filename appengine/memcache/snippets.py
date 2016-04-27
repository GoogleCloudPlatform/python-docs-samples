# [START import]
from google.appengine.api import memcache
# [END import]


def query_for_data():
    return 'data'


# [START get_data]
def get_data():
    data = memcache.get('key')
    if data is not None:
        return data
    else:
        data = query_for_data()
        memcache.add('key', data, 60)
    return data
# [END get_data]


def add_values():
    # [START add_values]
    # Add a value if it doesn't exist in the cache
    # with a cache expiration of 1 hour.
    memcache.add(key="weather_USA_98105", value="raining", time=3600)

    # Set several values, overwriting any existing values for these keys.
    memcache.set_multi(
        {"USA_98115": "cloudy", "USA_94105": "foggy", "USA_94043": "sunny"},
        key_prefix="weather_",
        time=3600
    )

    # Atomically increment an integer value.
    memcache.set(key="counter", value=0)
    memcache.incr("counter")
    memcache.incr("counter")
    memcache.incr("counter")
    # [END add_values]
