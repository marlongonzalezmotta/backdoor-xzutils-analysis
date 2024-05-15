import json
import datetime
import statistics
from collections import defaultdict

def load_and_process_data(filename, author):
    with open(filename, 'r') as f:
        data = json.load(f)

    for item in data:
        item['date'] = datetime.datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S %z')

    author_data = [item for item in data if item['author'] == author]

    return author_data

def calculate_work_time_stats(author_data):
    times = [(item['date'].time().hour + item['date'].time().minute/60) % 24 for item in author_data]
    times = [time if time >= 5.5 else time + 24 for time in times]
    total_commits = len(times)
    median_time = statistics.median(times)
    mean_time = statistics.mean(times)
    mode_time = statistics.mode(times)
    min_time = min(times)
    max_time = max(times)

    return total_commits, median_time, mean_time, mode_time, min_time, max_time

def decimal_to_time(decimal_hour):
    hour = int(decimal_hour) % 24
    minute = int((decimal_hour - hour) * 60)
    return f'{hour:02d}:{minute:02d}'

def calculate_work_time_by_weekday(author_data):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_times = defaultdict(list)

    for item in author_data:
        weekday = weekdays[item['date'].weekday()]
        time = (item['date'].time().hour + item['date'].time().minute/60) % 24
        time = time if time >= 5.5 else time + 24
        weekday_times[weekday].append(time)

    weekday_stats = {}
    for weekday, times in weekday_times.items():
        median_time = statistics.median(times)
        mean_time = statistics.mean(times)
        mode_time = statistics.mode(times)
        min_time = min(times)
        max_time = max(times)

        weekday_stats[weekday] = (median_time, mean_time, mode_time, min_time, max_time)

    return weekday_stats

author_data = load_and_process_data('jia-tan-logs-converted-to-finland.json', 'jiat0218@gmail.com')

total_commits, median_time, mean_time, mode_time, min_time, max_time = calculate_work_time_stats(author_data)

dates = [item['date'] for item in author_data]
start_date = min(dates)
end_date = max(dates)

print(f'Analysis of jiat0218@gmail.com:')
print()
print(f'---Result of the average commits of ALL DAYS from {start_date} to {end_date}:---')
print(f'Total commits analyzed: {total_commits}.')
print(f'The median commit time is {decimal_to_time(median_time)} hours.')
print(f'The mean commit time is {decimal_to_time(mean_time)} hours.')
print(f'The MOST FREQUENT COMMIT TIME IS {decimal_to_time(mode_time)} hours.')
print(f'The earliest commit time is {decimal_to_time(min_time)} hours.')
print(f'The latest commit time is {decimal_to_time(max_time)} hours.')
print()
print(f'---Result of the average of the WEEKDAYS commits from {start_date} to {end_date}---')

weekday_stats = calculate_work_time_by_weekday(author_data)

for weekday, stats in weekday_stats.items():
    median_time, mean_time, mode_time, min_time, max_time = stats
    print(f'\n{weekday}:')
    print(f'The median commit time is {decimal_to_time(median_time)} hours.')
    print(f'The mean commit time is {decimal_to_time(mean_time)} hours.')
    print(f'The MOST FREQUENT COMMIT TIME IS {decimal_to_time(mode_time)} hours.')
    print(f'The earliest commit time is {decimal_to_time(min_time)} hours.')
    print(f'The latest commit time is {decimal_to_time(max_time)} hours.')
