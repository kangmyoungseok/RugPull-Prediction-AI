#기존 Labeling_v1.8.csv 파일에서 
import lib.mylib
import pandas as pd
from pandas.core.frame import DataFrame

datas = pd.read_csv('Labeling_v1.8.csv',encoding='utf-8-sig').to_dict('records')
datas[0]
result = []
for data in datas:
    if(data['is_rugpull'] == False):
        result.append(data)
result
pd.DataFrame(result).to_csv('False_data.csv',encoding='utf-8-sig',index=False)
