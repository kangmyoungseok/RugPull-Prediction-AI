import pandas as pd
import time
datas5 = pd.read_csv('Labeling_v2.5.csv',encoding='utf-8-sig').to_dict('records')   #얘가 밀렸네 ...
datas = pd.read_csv('Pairs_v2.3.csv',encoding='utf-8-sig').to_dict('records')
token0_list = {}
for data in datas:
    token0_list[data['id']]= data['token0.name']

for data in datas5:
        data['token0.name'] = token0_list[data['id']]

pd.DataFrame(datas5).to_csv('Labeling_v3.1.csv',encoding='utf-8-sig',index=False)

datas[15]
data = datas5[10]

for data in datas5:
    tx_dict3[data['id']]
    data['current_token_total_supply']
    print("------------")

    time.sleep(0.2)