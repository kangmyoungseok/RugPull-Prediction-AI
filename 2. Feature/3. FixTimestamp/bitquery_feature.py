from lib.BitqueryLib import *
from lib.mylib import *
from datetime import datetime
import pandas as pd
from multiprocessing import Pool

def get_feature(data):
    token_address = data['token00.id']
    creator_address = data['receiver']
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
            
    #오류가 나면 다시 처리하도록
    if( (timestamp_creator_LP_amount == -1) or (timestamp_creator_token_amount == -1 )):
        timestamp_creator_LP_amount = call_bitquery_creator_LP_amount_func(LP_creator_address,timestamp,pair_address)
        timestamp_creator_token_amount = call_bitquery_creator_token_amount_func(creator_address,timestamp,token_address)
    
    #그럼에도 오류가 나면 모아둔다.
    if( (timestamp_creator_LP_amount == -1) or (timestamp_creator_token_amount == -1 )):
        return data, -1

    data['burn_amount'] = burn_amount
    data['timestamp_creator_LP_amount'] = timestamp_creator_LP_amount
    data['timestamp_creator_token_amount'] = timestamp_creator_token_amount
    

    return data,1


if __name__=='__main__':

    file_name = './FalseData_oneDay2.csv'
    datas = pd.read_csv(file_name).to_dict('records')
    error_list = []
    datas_len = len(datas)
    
    try:
        p = Pool(4)
        count = 0
        result = []
        for ret,is_error in p.imap(get_feature,datas):
            if(is_error == -1):
                error_list.append(ret)
                count = count+1
                continue
            count = count+1
            result.append(ret)
            if(count % 100 == 0):
                print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))
        p.close()
        p.join()
    except Exception as e:
        print(e)
    print('===================================   finish    =========================================')
    print('==================================== error_list retry ========================================')
    try:
        p = Pool(1)
        datas_len = len(error_list)
        count = 0
        for ret,is_error in p.imap(get_feature,error_list):
            count = count +1
            result.append(ret)
            if(count % 20 == 0):
                print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))
        p.close()
        p.join()
    except Exception as e:
        print(e)
    print('==================================== error_list retry finish ========================================')
    print('recovery rate : 전체 에러 %d개 중에 %d개 복구 '%(datas_len,count))
    df = pd.DataFrame(result)
    df.to_csv('FalseData_oneDay3.csv',encoding='utf-8-sig',index=False)
    print(file_name + ' complete')
