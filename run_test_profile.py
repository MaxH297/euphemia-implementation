import csv
from app.test_instance import TestInstance

filename = 'profile'

dates = []

with open('dates.csv', 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        dates.append(row[0])

test = TestInstance(dates, filename)

test.run_tests()