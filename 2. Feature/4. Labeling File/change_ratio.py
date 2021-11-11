import pandas as pd
from pandas.core.frame import DataFrame
from decimal import Decimal

datas = pd.read_csv('Labeling_v1.9.csv').to_dict('records')
#int(datas[0]['id'][-1]) % 2


#datas[0]['is_rugpull']

result = []
for data in datas:
    if(data['is_rugpull'] == True):
        if(data['id'][-1] in ['1','4','a','c','7','9','d']):
            result.append(data)
    else:
        result.append(data)
len(result)

8667 -1665


pd.DataFrame(result).to_csv('Labeling_v1.10.csv',encoding='utf-8-sig',index=False)



