from lib.BitqueryLib import *
import pandas as pd
from multiprocessing import Pool



def get_feature(data):
    token_address = data['token00.id']
    decimals = 10 ** int(data['token00.decimals'])
            
    #현재 Total Supply (그 시점의 토탈 Supply 대체)
    current_token_total_supply = call_etherscan_current_total_supply(token_address,decimals) 
    data['current_token_total_supply'] = current_token_total_supply
    

    return data


if __name__=='__main__':
    datas = pd.read_csv('retry_etherscan.csv').to_dict('records')
    result = []
    p = Pool(1)
    for ret in p.imap(get_feature,datas):
        result.append(ret)
    
    p.close()
    p.join()
    df = pd.DataFrame(result)
    file_name = 'fin.csv'
    df.to_csv(file_name,encoding='utf-8-sig',index=False)
