#False인 데이터의 타임스탬프를 구한다.
import pandas as pd
from lib.mylib import *
from lib.TheGraphLib import *
import os

datas = pd.read_csv('Labeling_v2.1.csv',encoding='utf-8-sig').to_dict('records')
#Labeling_file = os.path.join(os.path.abspath("Labeling File"),"Labeling_v1.2.csv" )

#datas = pd.read_csv(Labeling_file).to_dict('records')

for data in datas:
    #정상인 경우에는 30일 까지의 TimeStamp를 구한다.
    if(data['is_rugpull'] == False):
        feature_timestamp = data['last_transaction_timestamp']
        data['feature_timestamp'] = feature_timestamp
    else:
        data['feature_timestamp'] = data['rugpull_timestamp']

df = pd.DataFrame(datas)
df.to_csv('Labeling_v3.1.csv',encoding='utf-8-sig',index=False)


