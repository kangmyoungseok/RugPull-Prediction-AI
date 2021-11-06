from pandas.core.frame import DataFrame
import pandas as pd
import time
from tqdm import tqdm
from multiprocessing import Pool
from multiprocessing import Process
from mylib import *
from TheGraphLib import *
from featureLib import *
import datetime

def switch_file(file_name):
    global datas
    datas = pd.read_csv(file_name).to_dict('records')

def get_feature(data):
    #하나의 데이터 pair에 대해서 피처들 다 추가한다.
    #여기에서 data['feat1'] = feat1 , data['feat2'] = feat2 ... 추가. 각각의 피처를 구하는 함수는 따로 구현
    pair_address = data['id']

    #TheGraph API를 이용해서 하나의 페어에 대한 쌍들을 전부 메모리에 올려놓고. 시작
    mint_data_transaction = call_theGraph_mint(pair_address)
    swap_data_transaction = call_theGraph_swap(pair_address)
    burn_data_transaction = call_theGraph_burn(pair_address)

    #initial_Liquidity 의 이더와 토큰 구하기
    initial_Liquidity_Eth , initial_Liquidity_Token = get_initial_Liquidity(data['token0.symbol'],mint_data_transaction)

    # 각각의 count 구하기
    mint_count = len(mint_data_transaction)
    swap_count = len(swap_data_transaction)
    burn_count = len(burn_data_transaction)

    # Mint/Burn/Swap의 Active Period 상의 분포 
    initial_timestamp = int(mint_data_transaction[0]['timestamp'])
    last_timestamp = get_last_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction)
    active_period = last_timestamp - initial_timestamp
    mint_mean_period = int(get_mint_mean_period(mint_data_transaction,initial_timestamp))
    swap_mean_period = int(get_swap_mean_period(swap_data_transaction,initial_timestamp))
    burn_mean_period = int(get_burn_mean_period(burn_data_transaction,initial_timestamp))
    
    #SwapIn/SwapOut 비율
    swapIn,swapOut = swap_IO_rate(swap_data_transaction,token_index(data))    

    #rugpull timestamp , 러그풀 시점에서 유동성 풀에 있는 이더 변화량(rugpull timestamp / change)
    rugpull_timestamp, rugpull_change, is_rugpull, before_rugpull_Eth, after_rugpull_Eth,rugpull_method = get_rugpull_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction,token_index(data))

    #rugpull 이 시작부터 끝날때까지 경과한 시간
    rugpull_proceeding_time = int(rugpull_timestamp) - int(initial_timestamp)
    if(is_rugpull == False):
        rugpull_proceeding_time = 0
        rugpull_method = ''
        rugpull_timestamp = '0'
        rugpull_change = ''

    #데이터 저장
    data['initial_Liquidity_Eth'] = initial_Liquidity_Eth
    data['initial_Liquidity_Token'] = initial_Liquidity_Token   
    data['last_transaction_timestamp'] = last_timestamp
    data['last_transaction_date'] = datetime.datetime.fromtimestamp(int(last_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    data['mint_count'] = mint_count
    data['swap_count'] = swap_count
    data['burn_count'] = burn_count
    data['mint_mean_period'] = mint_mean_period
    data['swap_mean_period'] = swap_mean_period
    data['burn_mean_period'] = burn_mean_period
    data['swapIn'] = swapIn
    data['swapOut'] = swapOut
    data['active_period'] = active_period
    data['rugpull_method'] = rugpull_method
    data['rugpull_timestamp'] = rugpull_timestamp
    data['rugpull_timestamp_date'] = datetime.datetime.fromtimestamp(int(rugpull_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    data['before_rugpull_Eth'] = before_rugpull_Eth
    data['after_rugpull_Eth'] = after_rugpull_Eth
    data['rugpull_change'] = rugpull_change 
    data['rugpull_proceeding_hour'] = str(rugpull_proceeding_time / 3600) + 'h'
    data['is_rugpull'] = is_rugpull
     
    return data


if __name__=='__main__':
    createFolder('./result')
    file_name = './Pairs_v1.6.csv'
    file_count = split_csv(file_name)
    out_list = []
    out_list = list(input('입력(공백단위) : ').split())

    for i in out_list:         #하나의 파일 단위로 Creator Address 불러오고, 해당 초기 유동성풀 이더값 구해온다.
        file_name = './result/out{}.csv'.format(i)
        switch_file(file_name)
        datas_len = len(datas)
        try:
            p = Pool(1)
            count = 0
            result = []
            for ret in p.imap(get_feature,datas):
                count = count+1
                result.append(ret)
                if(count % 200 == 0):
                    print("Process Rate : {}/{} {}%".format(count,datas_len,int((count/datas_len)*100)))
            p.close()
            p.join()
        except Exception as e:
            print(e)
        print('===================================   finish    =========================================')
        time.sleep(5)
            
        df = pd.DataFrame(result)
        file_name = './result/fout{}.csv'.format(i)
        df.to_csv(file_name,encoding='utf-8-sig',index=False)
        print(file_name + ' complete')
    merge_csv()