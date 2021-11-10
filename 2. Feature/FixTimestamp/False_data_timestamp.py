#False인 데이터의 타임스탬프를 구한다.
import pandas as pd
from lib.mylib import *
from lib.TheGraphLib import *
import os



datas = pd.read_csv('False_data.csv').to_dict('records')

mint_query = '''
{
  mints(first: 1, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s"}) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
''' 
one_month = 60* 60 * 24 * 30
one_week = 60 * 60 * 24 * 7
one_day = 60*60*24
half_day = 60*60*12

for data in datas:
    #정상인 경우에는 30일 까지의 TimeStamp를 구한다.
    if(data['is_rugpull'] == False):
        pair = data['id']
        query = mint_query % pair
        result = run_query(query)
        feature_timestamp = int(result['data']['mints'][0]['timestamp']) + one_day
        data['feature_timestamp'] = feature_timestamp
    else:
        data['feature_timestamp'] = data['rugpull_timestamp']

df = pd.DataFrame(datas)
df.to_csv('FalseData_oneDay.csv',encoding='utf-8-sig',index=False)


