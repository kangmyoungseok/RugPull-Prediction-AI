import pandas as pd

datas1 = pd.read_csv('Creator_list_v1.2.csv',encoding='utf-8-sig').to_dict('records')
datas2 = pd.read_csv('Pairs_v2.4.csv',encoding='utf-8-sig').to_dict('records')

len(datas2)
for i in range(1000):
    datas2[i]['creator_address']

creator_list = []
for data in datas2:
    if(str(data['creator_address']) == 'nan'):
        creator_list.append(data)

for data in datas2:
    


str(datas2[100]['creator_address'])

creator_list = {}
for data in datas1:
    creator_list[data['token00.id']] = data['token00_creator_address']


