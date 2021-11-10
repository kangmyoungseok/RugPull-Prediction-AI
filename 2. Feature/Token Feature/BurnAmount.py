from lib.BitqueryLib import *
from lib.mylib import *
from datetime import datetime
import pandas as pd
from multiprocessing import Pool

def switch_file(file_name):
    global datas
    datas = pd.read_csv(file_name).to_dict('records')

token_address = '0xd45740ab9ec920bedbd9bab2e863519e59731941'
timestamp = (datetime.fromtimestamp(int('1627962950')).isoformat())
burn_amount

def get_feature(data):
    token_address = data['token00.id']
    timestamp = (datetime.fromtimestamp(int(data['feature_timestamp'])).isoformat())


    #Token의 Burn
    burn_amount = call_bitquery_burn_amount_func(timestamp,token_address)
    data['burn_amount'] = burn_amount

    return data


if __name__=='__main__':
    createFolder('./data')
    createFolder('./result')
    file_name = './Labeling_v1.6.csv'
    file_count = split_csv(file_name)
    out_list = []
    out_list = list(input('입력(공백단위) : ').split())


    for i in out_list:         #하나의 파일 단위로 Creator Address 불러오고, 해당 초기 유동성풀 이더값 구해온다.
        file_name = './data/out{}.csv'.format(i)
        switch_file(file_name)
        datas_len = len(datas)
        try:
            p = Pool(4)
            count = 0
            result = []
            for ret in p.imap(get_feature,datas):
                count = count+1
                result.append(ret)
                if(count % 100 == 0):
                    print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))
            p.close()
            p.join()
        except Exception as e:
            print(e)
        print('===================================   finish    =========================================')
       
        df = pd.DataFrame(result)
        file_name = './drive/MyDrive/fout{}.csv'.format(i)
        df.to_csv(file_name,encoding='utf-8-sig',index=False)
        print(file_name + ' complete')
    merge_csv()