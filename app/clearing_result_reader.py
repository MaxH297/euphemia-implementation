import csv
import json

PATH_PREFIX = 'results/'

class ClearingResultReader(object):
    def get_result(self, path):
        results = {}
        with open(PATH_PREFIX + path, 'rU') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:
                    if not row[0] in results:
                        results[row[0]] = {}
                    results[row[0]][row[1]] = self.read_line(row)
        return results
                
    
    def read_line(self, row):
        result = {}
        result['test'] = row[1]
        accepted_dict = json.loads(row[2].replace("\'", "\""))
        accepted = ''
        for i in accepted_dict:
            if round(float(accepted_dict[i])) == 1:
                accepted = i
        result['accepted'] = accepted
        prices = []
        for i in range(24):
            prices.append(float(row[3 + i]))
        result['prices'] = prices
        result['profit'] = float(row[27])
        result['welfare'] = float(row[28])
        if(len(row) > 29):
            result['welfare_demand'] = float(row[29])
            result['welfare_supply'] = float(row[30])
        return result