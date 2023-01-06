import csv

PATH_PREFIX = 'orders/'

class BlockOrderReader(object):
    def get_block_orders(self, path):
        blocks = []
        with open(PATH_PREFIX + path, 'rU') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row[0] == "BB":
                    blocks.append(self.read_line(row))
        orders = {}
        orders['blocks'] = blocks
        #model flexible hourly orders as exclusive group
        orders['exclusive_groups'] = list(self.get_exclusive_groups(orders['blocks']).values())
        orders['linked'] = self.get_linked_blocks(orders['blocks'])
        return orders
                
    
    def read_line(self, row):
        order = {}
        order['id'] = row[1]
        order['price'] = float(row[5])
        quantities = []
        for i in range(3):
            quantities.append(float(row[6+i]))
        for i in range(21):
            quantities.append(float(row[10+i]))
        order['hours'] = quantities
        order['type'] = row[2]
        order['special_id'] = row[3]
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

    def get_linked_blocks(self, blocks):
        linked = []
        blocks = [block for block in blocks if block['type'] == 'C02']
        for block in blocks:
            linked.append({'child': block['id'], 'parent': block['special_id']})
        return linked