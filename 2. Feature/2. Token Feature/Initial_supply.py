from os import error
from lib.BitqueryLib import *
from lib.mylib import *
import pandas as pd
from multiprocessing import Pool
import time
def switch_file(file_name):
    global datas
    datas = pd.read_csv(file_name).to_dict('records')


def get_feature(data):
    try:
        token_address = data['token00.id']
        initial_supply,receiver_list = get_initial_supply(token_address)
        if(initial_supply == -1):
          initial_supply,receiver_list = get_initial_supply(token_address)
          if(initial_supply == -1):
              return data,-1
        if(initial_supply == 0):
          return data,0
        data['initial_supply'] = initial_supply
        data['receiver_list'] = receiver_list

    except Exception as e:
        print(e)
        return data,-1
        
    return data,1
if __name__=='__main__':
    createFolder('./result')
    createFolder('./data')
    file_name = './Labeling_v2.1.csv'
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
            for ret,is_error in p.imap(get_feature,datas):
                if(is_error == -1):
                  error_list.append(ret)
                  continue
                if(is_error == 0):
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
        print('==================================== error_list retry ========================================')
        try:
          p = Pool(4)
          datas_len = len(error_list)
          count = 0
          for ret,is_error in p.imap(get_feature,error_list):
            if(is_error == -1 or is_error == 0):
              continue
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
        file_name = './drive/MyDrive/fout{}.csv'.format(i)
        #file_name = './result/fout{}.csv'.format(i)
        df.to_csv(file_name,encoding='utf-8-sig',index=False)
        print(file_name + ' complete')
#    merge_csv()





####################### 테스트 코드 작성 라인 ########################
'''
result
result['data']['ethereum']['transfers']
line = '0x4783724b23f3665057ec66ec0c8da8125ca3dabe'
token_address = '0x291fa2725d153bcc6c7e1c304bcad47fdef1ef84'
query
response
'''

####################################################################