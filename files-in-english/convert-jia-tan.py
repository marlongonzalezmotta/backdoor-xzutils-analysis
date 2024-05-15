import json
import datetime
import pytz

def load_and_convert_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    singapore_tz = pytz.timezone('Asia/Singapore')
    finland_tz = pytz.timezone('Europe/Helsinki')

    for item in data:
        date = datetime.datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S %z')
        date = date.astimezone(singapore_tz)
        date = date.astimezone(finland_tz)
        item['date'] = date.strftime('%Y-%m-%d %H:%M:%S %z')

    return data

data = load_and_convert_data('jia-tan-logs.json')

with open('jia-tan-logs-converted-to-finland.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)