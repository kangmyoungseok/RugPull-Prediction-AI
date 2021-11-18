import pandas as pd
from lib.BitqueryLib import *
datas1 = pd.read_csv('Labeling_v2.7.2.csv',encoding='utf-8-sig').to_dict('records')  #코랩
datas2 = pd.read_csv('Labeling_v2.7.1.csv',encoding='utf-8-sig').to_dict('records')   #로컬

result = []

for data in datas1:
    if(data['is_rugpull'] == True):
        result.append(data)

for data in datas2:
    if(data['is_rugpull'] == False):
        result.append(data)

#에러인거 다시 쿼리 날려


for data in result:
    if(data['current_token_total_supply']!= -1):
        continue
    token_address = data['token00.id']
    decimals = 10 ** int(data['token00.decimals'])
            
    #현재 Total Supply (그 시점의 토탈 Supply 대체)
    current_token_total_supply = call_etherscan_current_total_supply(token_address,decimals)
    print('id : %s,before : %s, after : %s'%(token_address,data['current_token_total_supply'],current_token_total_supply))
    data['current_token_total_supply'] = current_token_total_supply

for data in result:
    if(str(data['current_token_total_supply']) != '-1'):
        continue
    token_address = data['token00.id']
    decimals = 10 ** int(data['token00.decimals'])
            
    #현재 Total Supply (그 시점의 토탈 Supply 대체)
    current_token_total_supply = call_etherscan_current_total_supply(token_address,decimals)
    print('id : %s,before : %s, after : %s'%(token_address,data['current_token_total_supply'],current_token_total_supply))
    data['current_token_total_supply'] = current_token_total_supply


for data in result:
    if(str(data['current_token_total_supply']) != '-1'):
        continue
    token_address = data['token00.id']
    decimals = 10 ** int(data['token00.decimals'])
            
    #현재 Total Supply (그 시점의 토탈 Supply 대체)
    current_token_total_supply = call_etherscan_current_total_supply(token_address,decimals)
    print('id : %s,before : %s, after : %s'%(token_address,data['current_token_total_supply'],current_token_total_supply))
    data['current_token_total_supply'] = current_token_total_supply

print(len(result))

pd.DataFrame(result).to_csv('Labeling_v2.8.csv',encoding='utf-8-sig',index=False)
