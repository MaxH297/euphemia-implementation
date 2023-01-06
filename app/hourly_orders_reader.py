import csv

from datetime import *

PATH_PREFIX = 'orders/'

class HourlyOrderReader(object):

    def get_hourly_orders(self, path):
        orders = {}
        orders['buy'] = []
        orders['sell'] = []
        with open(PATH_PREFIX + path, 'rU') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 7 and (row[6] == 'Purchase' or row[6] == 'Sell'):
                    if (row[6] == "Purchase"):
                        orders['buy'].append(self.read_line(row))
                    else:
                        orders['sell'].append(self.read_line(row))
        return orders
                
    
    def read_line(self, row):
        order = {}
        #order['id'] = row[0]
        order['side'] = 'BUY' if row[6] == 'Purchase' else 'SELL'
        order['price'] = float(row[4])
        order['quantity'] = float(row[5])
        order['hour'] = int(row[3] if row[3] != "3B" else 50) - 1
        return order
