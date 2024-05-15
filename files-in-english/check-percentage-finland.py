import json
from datetime import datetime
import pytz

total_commits = 0
finland_commits = 0

with open('lasse-collin-logs.json', 'r') as f:
    commits = json.load(f)

for commit in commits:
    total_commits += 1

    date_str = commit['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')

    finland_tz = pytz.timezone('Europe/Helsinki')
    date_obj_finland = date_obj.astimezone(finland_tz)

    if date_obj.utcoffset() == date_obj_finland.utcoffset():
        finland_commits += 1

percentage = (finland_commits / total_commits) * 100

print(f'Total commits analyzed: {total_commits}')
print(f'{percentage}% of commits correspond to Finland timezone.')
