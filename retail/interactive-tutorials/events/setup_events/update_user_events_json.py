import datetime
import re

"""
Run the file to update the user_events.json and user_events_some_invalid.json files with more recent timestamp
"""


def update_events_timestamp(json_file):
    # Get the yesterday's date
    request_time = datetime.datetime.now() - datetime.timedelta(days=1)
    day = request_time.date().strftime("%Y-%m-%d")
    print(day)

    # Read in the file
    with open(json_file, 'r') as file:
        filedata = file.read()

    # Replace the target string  '"eventTime":"YYYY-mm-dd' with yesterday date
    filedata = re.sub('\"eventTime\":\"([0-9]{4})-([0-9]{2})-([0-9]{2})',
                      '\"eventTime\":\"' + day, filedata, flags=re.M)

    # Write the file out again
    with open(json_file, 'w') as file:
        file.write(filedata)
    print(f"The {json_file} is updated")


if __name__ == "__main__":
    update_events_timestamp("../resources/user_events.json")
    update_events_timestamp("../resources/user_events_some_invalid.json")
