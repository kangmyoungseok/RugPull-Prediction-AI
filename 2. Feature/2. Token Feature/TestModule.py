import pandas as pd

datas1 = pd.read_csv('Creator_list_v1.2.csv',encoding='utf-8-sig').to_dict('records')
datas2 = pd.read_csv('Pairs_v2.4.csv',encoding='utf-8-sig').to_dict('records')

len(datas1)

creator_list = {}
for data in datas1:
    creator_list[data['token00.id']] = data['token00_creator_address']


