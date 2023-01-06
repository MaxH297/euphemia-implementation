import csv
from app.block_orders_reader import BlockOrderReader
from app.euphemia import Euphemia
from app.hourly_orders_reader import HourlyOrderReader
from app.test_instance import TestInstance

dates = []

with open('dates.csv', 'rU') as f:
    reader = csv.reader(f)
    for row in reader:
        dates.append(row[0])

hor = HourlyOrderReader()
bor = BlockOrderReader()

output_rows = []

for date in dates:
    hourly_orders = hor.get_hourly_orders('hourly_' + date + '.csv')
    block_orders = bor.get_block_orders('blocks_' + date + '.csv')
    euphemia = Euphemia(hourly_orders, block_orders)
    euphemia.run_milp()
    prices = euphemia.get_clearing_prices()
    objective = euphemia.get_objective()
    welfare_demand = euphemia.get_welfare_demand()
    welfare_supply = euphemia.get_welfare_supply()
    output_rows.append(date + prices + [objective, welfare_demand, welfare_supply])

with open('output/clearing-results.csv', 'w') as f:
    for row in output_rows:
        writer = csv.writer(f)
        writer.writerow(row)
    f.close()