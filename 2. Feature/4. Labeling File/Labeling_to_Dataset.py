import pandas as pd
from pandas.core.frame import DataFrame
from decimal import Decimal

datas = pd.read_csv('Labeling_v3.2.csv').to_dict('records')



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
        dataset['id'] = data['id']
        dataset['Label'] = data['is_rugpull']
#        dataset['txcount'] = get_txcount(data)
        dataset['mint_count_per_week'] = data['mint_count'] / ((int(data['active_period']) / (60* 60 * 24 * 7)) + 1)
#        dataset['swap_count_per_week'] = data['swap_count'] / ((int(data['active_period']) / 60* 60 * 24 * 7) + 1)
        dataset['burn_count_per_week'] = data['burn_count'] / ((int(data['active_period']) / (60* 60 * 24 * 7)) + 1)
        dataset['mint_ratio'] = float(data['mint_ratio'])
        dataset['swap_ratio'] = float(data['swap_ratio'])
        dataset['burn_ratio'] = float(data['burn_ratio'])
        dataset['mint_mean_period'] = float(data['mint_mean_period']) 
        dataset['swap_mean_period'] = float(data['swap_mean_period'])
        dataset['burn_mean_period'] = float(data['burn_mean_period'])
        dataset['swapIn_per_week'] = data['swapIn'] /((int(data['active_period']) / (60* 60 * 24 * 7)) + 1)
        dataset['swapOut_per_week'] = data['swapOut'] / ((int(data['active_period']) / (60* 60 * 24 * 7)) + 1)
        dataset['swap_rate'] = float(data['swap_rate'])
        dataset['LP_avg'] = data['LP_avg']
        dataset['LP_stdev'] = data['LP_stdev']
        dataset['LPCreator_holding_ratio'] = float(get_holding_ratio(data))
        dataset['Lock_ratio'] = float(get_Lock_ratio(data))
        dataset['token_burn_ratio'] = float(get_burn_ratio(data))
        dataset['Creator_token_holding_ratio'] = float(get_token_holding_ratio(data))
        dataset['number_of_token_creation_of_Creator'] = creator_list.count(data['receiver'])
    except Exception as e:
        print(e)
        continue    
    result.append(dataset)
len(result)
pd.DataFrame(result).to_csv('Dataset_v1.9.csv',encoding='utf-8-sig',index=False)


