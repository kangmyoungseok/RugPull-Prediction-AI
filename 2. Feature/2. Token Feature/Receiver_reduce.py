import pandas as pd
from pandas.core.frame import DataFrame
datas = pd.read_csv('Labeling_v2.2.csv',encoding='utf-8-sig').to_dict('records')
len(datas)


result = []
for data in datas:
    if(len(data['receiver_list']) > 1 ):
        if(data['token00_creator_address'] in data['receiver_list']):
            print(data['token00_creator_address'])
            data['receiver_list'] = data['token00_creator_address']
            result.append(data)
            continue
        if(data['LP_Creator_address'] in data['receiver_list']):
            data['receiver_list'] = data['LP_Creator_address']
            print(data['LP_Creator_address'])
            result.append(data)
            continue
    else:
        data['receiver_list'] = data['receiver_list'][0]
        result.append(data)
print(len(result))

df = pd.DataFrame(result)
df.to_csv('Labeling_v2.3.csv',encoding='utf-8-sig',index=False)
