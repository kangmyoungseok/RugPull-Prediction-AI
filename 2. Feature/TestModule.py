import pandas as pd

datas = pd.read_csv('Labeling_v1.1.csv').to_dict('records')
if(int(datas[32]['validation']) == 1):
    print(1)
result_data =[]
for data in datas:
    if(data['is_rugpull'] == True):
        result_data.append(data)
    else:
        try:
            if(int(data['validation']) == 1 ):
                result_data.append(data)
        except:
            print(data['token0.name'])
            if(data['token1.symbol'] == 'SURF'):
                result_data.append(data)

df = pd.DataFrame(result_data)
df.to_csv('Labeling_v1.2.csv',encoding='utf-8-sig',index=False)
