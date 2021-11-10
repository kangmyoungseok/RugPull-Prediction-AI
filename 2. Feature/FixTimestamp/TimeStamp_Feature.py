#라벨링된 데이터 파일에 대해서 주어진 타임스탬프시점의 Feature를 구한다.
#TheGraph API에서 얻을 수 있는 정보들에 한해서.
'''
    1. (M/B/S) Count            : 유동성 변화 이벤트 갯수
    2. (M/B/S) / Active Period  : 유동성 변화 이벤트 발생 분포
    3. (M/B/S) Count / total_Count : 유동성 변화 이벤트 비율
    4. Swap In/Out 비율[(SwapIN/SwapOUT+1)로 지표를 활용]
    5. 유동성 풀의 지분 분포도 : 해당 시점에 LP 토큰 보유 비율에 대한 표준편차, 평균
    6. 해당 시점에 LP Token Total Supply(분모)
'''

#1705개
from pandas.core.frame import DataFrame
import pandas as pd
import time
from multiprocessing import Pool
from lib.mylib import *
from lib.TheGraphLib import *
from lib.featureLib import *
import datetime

def switch_file(file_name):
    global datas
    datas = pd.read_csv(file_name).to_dict('records')

'''
pair_address = '0x9b533f1ceaa5ceb7e5b8994ef16499e47a66312d'
limit_timestamp = '1592420710'

mint_data_transaction
burn_data_transaction
swap_data_transaction
mint_count
burn_count
swap_count
active_period
swapIn =0
swapOut=0
''' 
def get_feature(data):
    try:
        #print("start pair : %s"%data['id'])
        pair_address = data['id']
        limit_timestamp = data['feature_timestamp']
        

        #TheGraph API를 이용해서 하나의 페어에 대해 해당 Timestamp까지의 트랜잭션을 모두 배열로 저장
        mint_data_transaction = call_theGraph_mint(pair_address,limit_timestamp)
        swap_data_transaction = call_theGraph_swap(pair_address,limit_timestamp)
        burn_data_transaction = call_theGraph_burn(pair_address,limit_timestamp)
        
        # 각각의 count 구하기
        mint_count = len(mint_data_transaction)
        swap_count = len(swap_data_transaction)
        burn_count = len(burn_data_transaction)
        total_count = mint_count + swap_count + burn_count

        # Mint/Burn/Swap의 Active Period 상의 분포 
        initial_timestamp = int(mint_data_transaction[0]['timestamp'])
        last_timestamp = get_last_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction)
        active_period = last_timestamp - initial_timestamp
        mint_mean_period = int(get_mint_mean_period(mint_data_transaction,initial_timestamp)) / active_period
        swap_mean_period = int(get_swap_mean_period(swap_data_transaction,initial_timestamp)) / active_period
        burn_mean_period = int(get_burn_mean_period(burn_data_transaction,initial_timestamp)) / active_period

        #SwapIn/SwapOut 비율    
        swapIn,swapOut = swap_IO_rate(swap_data_transaction,token_index(data))    

        # 유동성 풀 분석
        LP_Creator = mint_data_transaction[0]['to']
        #mint/burn을 분석해서 해당 시점에 LP홀더들의 보유량을 dictionary로 만든다.
        LP_Holders = calc_LPToken_Holders(mint_data_transaction,burn_data_transaction)
        LP_stdev, LP_avg, total_LP_amount = get_LP_stdev(LP_Holders)
        try:
            LP_Creator_amount = LP_Holders[LP_Creator] #해당시점에 LP초기 제공자가 가지고 있는 양
        except:
            LP_Creator_amount = 0

        
        #데이터 저장
        data['mint_count'] = mint_count
        data['swap_count'] = swap_count
        data['burn_count'] = burn_count
        data['mint_ratio'] = mint_count / total_count 
        data['swap_ratio'] = swap_count / total_count
        data['burn_ratio'] = burn_count / total_count
        data['mint_mean_period'] = mint_mean_period
        data['swap_mean_period'] = swap_mean_period
        data['burn_mean_period'] = burn_mean_period
        data['swapIn'] = swapIn
        data['swapOut'] = swapOut
        data['swap_rate'] = swapIn/(swapOut +1)
        data['active_period'] = active_period
        data['LP_Creator_amount'] = LP_Creator_amount
        data['LP_Creator_address'] = LP_Creator 
        data['LP_avg'] = LP_avg
        data['LP_stdev'] = LP_stdev
        data['total_LP_amount'] = total_LP_amount
#        print("finish pair : %s"%data['id'])
    except Exception as e:
        print(data['id'])
        return data,-1
        
    return data,1


if __name__=='__main__':

    file_name = './FalseData_oneDay.csv'
    datas = pd.read_csv(file_name).to_dict('records')
    datas_len = len(datas)
    error_list = []
    try:
        p = Pool(2)
        count = 0
        result = []
        for ret,is_error in p.imap(get_feature,datas):
                if(is_error == -1):
                    error_list.append(ret)
                    continue
                count = count+1
                result.append(ret)
                if(count % 200 == 0):
                    print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))
        p.close()
        p.join()
    except Exception as e:
        print(e)
    print('===================================   finish    =========================================')
    time.sleep(3)

    p = Pool(2)
    for ret,is_error in p.imap(get_feature,error_list):
        if(is_error == -1):
            continue
        result.append(ret)
    
    p.close()
    p.join()
    df = pd.DataFrame(result)
    file_name = './FalseData_oneDay2.csv'
    df.to_csv(file_name,encoding='utf-8-sig',index=False)
    print(file_name + ' complete')
    

