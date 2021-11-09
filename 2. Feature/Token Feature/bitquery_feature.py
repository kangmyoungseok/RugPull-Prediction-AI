from lib.BitqueryLib import *
from lib.mylib import *
import datetime
import pandas as pd
from multiprocessing import Pool

def switch_file(file_name):
    global datas
    datas = pd.read_csv(file_name).to_dict('records')

def get_feature(data):
    token_address = data['token00.id']
    creator_address = data['token00_creator_address']
    LP_creator_address = data['LP_Creator_address']
    pair_address = data['id']
    timestamp = (datetime.fromtimestamp(int(data['feature_timestamp'])).isoformat())
    decimals = 10 ** int(data['token00.decimals'])

    #Token의 Burn
    burn_amount = call_bitquery_burn_amount_func(timestamp,token_address)

    #LP Creator가 TimeStamp 직전에 가지고 있는 LP의 양
    timestamp_creator_LP_amount = call_bitquery_creator_LP_amount_func(LP_creator_address,timestamp,pair_address)
    
    #Token Creator가 Timestamp 직전에 가지고 있는 Token의 양
    timestamp_creator_token_amount = call_bitquery_creator_token_amount_func(creator_address,timestamp,token_address)
            
    #현재 Total Supply (그 시점의 토탈 Supply 대체)
    current_token_total_supply = call_etherscan_current_total_supply(token_address,decimals)
    

    data['burn_amount'] = burn_amount
    data['timestamp_creator_LP_amount'] = timestamp_creator_LP_amount
    data['timestamp_creator_token_amount'] = timestamp_creator_token_amount
    data['current_token_total_supply'] = current_token_total_supply

    return data

if __name__=='__main__':
    createFolder('./data')
    createFolder('./result')
    file_name = './sample.csv'
    file_count = split_csv(file_name)
    out_list = []
    out_list = list(input('입력(공백단위) : ').split())
    error_list = []

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
        file_name = './result/fout{}.csv'.format(i)
        df.to_csv(file_name,encoding='utf-8-sig',index=False)
        print(file_name + ' complete')
    merge_csv()