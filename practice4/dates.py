#1 
import datetime

today = datetime.date.today()
five_days = datetime.timedelta(days=5)
print(today - five_days)
#2
import datetime

today = datetime.date.today()

yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
#3
import datetime

now = datetime.datetime.now()
no_microseconds = now.replace(microsecond=0)

print(no_microseconds)
#4
import datetime
date1 = datetime.datetime(2026, 2, 20, 12, 0, 0)
date2 = datetime.datetime(2026, 2, 24, 12, 0, 0)
difference = date2 - date1
print("Difference in seconds:", int(difference.total_seconds()))