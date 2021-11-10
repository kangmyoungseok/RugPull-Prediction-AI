from lib.BitqueryLib import *
import pandas as pd

datas = pd.read_csv('sample.csv').to_dict('records')
    
def call_bitquery_burn_amount_func(timestamp,token_address):
    query = query_burn_amount % (timestamp,token_address)
    response = bitquery_run(query)
    print(response)
    try:
        burn_amount = Decimal(response['data']['ethereum']['transfers'][0]['burned'])
    except:
        burn_amount = '0'
    
    return burn_amount

for data in datas:
    token_address = data['token00.id']
    timestamp = (datetime.fromtimestamp(int(data['feature_timestamp'])).isoformat())
    burn_amount = call_bitquery_burn_amount_func(timestamp,token_address)
    print(burn_amount)




