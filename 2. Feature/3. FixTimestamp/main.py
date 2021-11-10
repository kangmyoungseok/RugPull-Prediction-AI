#기존 Labeling_v1.8.csv 파일에서 
import lib.mylib
import pandas as pd
from pandas.core.frame import DataFrame

datas = pd.read_csv('Labeling_v1.8.csv',encoding='utf-8-sig').to_dict('records')
datas2 = pd.read_csv('1dayTimeStamp.csv',encoding='utf-8-sig').to_dict('records')
len(datas)
len(datas2)

result = []
for data in datas:
    if(data['is_rugpull'] == True):
        result.append(data)
for data in datas2:
    if(data['is_rugpull'] == False):
        result.append(data)
len(result)
pd.DataFrame(result).to_csv('Labeling_v1.9.csv',encoding='utf-8-sig',index=False)
