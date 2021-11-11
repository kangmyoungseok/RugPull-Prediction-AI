import pandas as pd
from pandas.core.frame import DataFrame
from decimal import Decimal

datas = pd.read_csv('Labeling_v1.10.csv').to_dict('records')



def get_txcount(data):
    mint = int(data['mint_count'])
    burn = int(data['burn_count'])
    swap = int(data['swap_count'])
    return mint + burn + swap

def get_holding_ratio(data):
    return Decimal(data['timestamp_creator_LP_amount']) / Decimal(data['total_LP_amount'])

def get_Lock_ratio(data):
    Lock_amount = Decimal(data['LP_Creator_amount']) - Decimal(data['timestamp_creator_LP_amount'])
    return Lock_amount / Decimal(data['total_LP_amount'])

def get_burn_ratio(data):
    return Decimal(data['burn_amount'] / data['current_token_total_supply'])

def get_token_holding_ratio(data):
    return Decimal(data['timestamp_creator_token_amount'] ) / Decimal(data['current_token_total_supply'])


creator_list = []
for data in datas:
    creator_list.append(data['receiver']) 

result = []
for data in datas:
    dataset = {}
    try:
        dataset['Label'] = data['is_rugpull']
        dataset['txcount'] = get_txcount(data)
        dataset['mint_count'] = data['mint_count']
        dataset['swap_count'] = data['swap_count']
        dataset['burn_count'] = data['burn_count']
        dataset['mint_ratio'] = data['mint_ratio']
        dataset['swap_ratio'] = data['swap_ratio']
        dataset['burn_ratio'] = data['burn_ratio']
        dataset['mint_mean_period'] = data['mint_mean_period']
        dataset['swap_mean_period'] = data['swap_mean_period']
        dataset['burn_mean_period'] = data['burn_mean_period']
        dataset['swapIn'] = data['swapIn']
        dataset['swapOut'] = data['swapOut']
        dataset['swap_rate'] = data['swap_rate']
        dataset['LP_avg'] = data['LP_avg']
        dataset['LP_stdev'] = data['LP_stdev']
        dataset['LPCreator_holding_ratio'] = get_holding_ratio(data)
        dataset['Lock_ratio'] = get_Lock_ratio(data)
        dataset['burn_ratio'] = get_burn_ratio(data)
        dataset['Creator_token_holding_ratio'] = get_token_holding_ratio(data)
        dataset['number_of_token_creation_of_Creator'] = creator_list.count(data['receiver'])
    except Exception as e:
        print(e)
        continue    
    result.append(dataset)
len(result)
pd.DataFrame(result).to_csv('Dataset_v1.2.csv',encoding='utf-8-sig',index=False)
