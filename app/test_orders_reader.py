import csv

PATH_PREFIX = 'input/'

class TestOrderReader(object):
    def get_block_orders(self, path):
        blocks = []
        with open(PATH_PREFIX + path, 'rU') as f:
            reader = csv.reader(f)
            index = 0
            for row in reader:
                if row[0] != "price":
                    blocks.append(self.read_line(row, index))
                    index += 1
        orders = {}
        orders['blocks'] = blocks
        orders['exclusive_groups'] = list(self.get_exclusive_groups(orders['blocks']).values())
        return orders
                
    
    def read_line(self, row, index):
        order = {}
        order['id'] = 'b' + str(index).zfill(3)
        order['price'] = float(row[0])
        quantities = []
        for i in range(24):
            quantities.append(float(row[1 + i]))
        order['hours'] = quantities
        order['type'] = 'C04'
        order['special_id'] = 'eg01'
        order['accRatio'] = 1.0
        return order

    def get_exclusive_groups(self, blocks):
        exclusive_groups = {}
        blocks = [block for block in blocks if block['type'] == 'C04']
        for block in blocks:
            if(block['special_id'] in exclusive_groups):
                exclusive_groups[block['special_id']].append(block['id'])
            else:
                exclusive_groups[block['special_id']] = [block['id']]
        return exclusive_groups