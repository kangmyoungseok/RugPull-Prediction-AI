from lib.BitqueryLib import *
from lib.mylib import *
from datetime import datetime
import pandas as pd
from multiprocessing import Pool


def get_feature(data):
    if(str(data['is_rugpull']) != 'False'):
        return data,1
    token_address = data['token00.id']
    decimals = 10 ** int(data['token00.decimals'])
            
    #현재 Total Supply (그 시점의 토탈 Supply 대체)
    current_token_total_supply = call_etherscan_current_total_supply(token_address,decimals)
    if(current_token_total_supply == -1):
        data['current_token_total_supply'] = -1
        return data,-1
    print('id : %s,before : %s, after : %s'%(token_address,data['current_token_total_supply'],current_token_total_supply))
    data['current_token_total_supply'] = current_token_total_supply
    
    return data,1




if __name__=='__main__':

    file_name = './Labeling_v2.7.csv'
    error_list = []

    datas = pd.read_csv(file_name).to_dict('records')
    datas_len = len(datas)
    try:
        p = Pool(1)
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
    df.to_csv('Labeling_v2.7.1.csv',encoding='utf-8-sig',index=False)
    print(file_name + ' complete')