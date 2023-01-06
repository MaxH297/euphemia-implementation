import csv
import os

from app.hourly_orders_reader import HourlyOrderReader
from app.block_orders_reader import BlockOrderReader
from app.test_orders_reader import TestOrderReader
from app.euphemia import Euphemia

PATH_PREFIX = 'output/'

EMPTYBLOCKS = {
    'blocks': [],
    'exclusive_groups': []
}


class TestInstance(object):

    def __init__(self, dates, filename, run_all=True, reduced=False):
        self.dates = dates
        self.filename = filename
        self.run_all = run_all
        self.reduced = reduced
        if os.path.exists(PATH_PREFIX + filename + '.csv'):
            os.remove(PATH_PREFIX + filename + '.csv')

    def run_tests(self):
        hor = HourlyOrderReader()
        bor = BlockOrderReader()
        tor = TestOrderReader()
        test_group = tor.get_block_orders(self.filename + '.csv')
        for date in self.dates:
            hourly_orders = hor.get_hourly_orders('hourly_' + date + '.csv')
            if not self.reduced:
                block_orders = bor.get_block_orders('blocks_' + date + '.csv')
            else:
                block_orders = {
                    'blocks': [],
                    'exclusive_groups': [],
                    'linked': []
                }
            eg_euphemia = self.prepare_eg_test(
                hourly_orders, block_orders, test_group)
            eg_euphemia.run_milp()
            self.print_row(
                [date, 'eg'] + self.result_row(eg_euphemia, test_group['blocks']))
            if(self.run_all):
                for block in test_group['blocks']:
                    euphemia = self.prepare_single_block_test(
                        hourly_orders, block_orders, block)
                    euphemia.run_milp()
                    self.print_row([date, block['id']] +
                                   self.result_row(euphemia, [block]))

    def prepare_eg_test(self, hourly_orders, block_orders, test_group):
        blocks_all = {
            'blocks': block_orders['blocks'] + test_group['blocks'],
            'exclusive_groups': block_orders['exclusive_groups'] + test_group['exclusive_groups'],
            'linked': block_orders['linked']
        }
        return Euphemia(hourly_orders, blocks_all)

    def prepare_single_block_test(self, hourly_orders, block_orders, block):
        blocks_all = {
            'blocks': block_orders['blocks'] + [block],
            'exclusive_groups': block_orders['exclusive_groups'],
            'linked': block_orders['linked']
        }
        return Euphemia(hourly_orders, blocks_all)

    def result_row(self, euphemia, blocks):
        accepted = {}
        welfare = 0
        prices = euphemia.get_clearing_prices()
        objective = euphemia.get_objective()
        welfare_demand = euphemia.get_welfare_demand()
        welfare_supply = euphemia.get_welfare_supply()
        for block in blocks:
            acc_ratio = euphemia.get_block_acceptance_ratio(block['id'])
            if acc_ratio > 0:
                accepted[block['id']] = acc_ratio
                for i in range(len(prices)):
                    welfare += acc_ratio * \
                        block['hours'][i] * (block['price'] - prices[i])
        return [accepted] + prices + [welfare] + [objective, welfare_demand, welfare_supply]

    def print_row(self, row):
        with open(PATH_PREFIX + self.filename + '.csv', 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            f.close()
