from logging import raiseExceptions
from lib.Thegraph import *
import json
from bs4 import BeautifulSoup
import re
from math import sqrt
from decimal import Decimal
from difflib import SequenceMatcher
from colorama import Fore


######################## 상수 값들 저장하는 공간 ##########################
proxy_contracts = [
'0x5e5a7b76462e4bdf83aa98795644281bdba80b88',
'0x000000000092c287eb63e8c2c30b4a74787054f8',
'0x0f4676178b5c53ae0a655f1b19a96387e4b8b5f2',
'0xdf65f4e6f2e9436bc1de1e00661c7108290e8bd3',
'0xdb73dde1867843fdca5244258f2fd4b6dc7b154e',
'0xbdb1127bd15e76d7e4d3bc4f6c7801aa493e03f0',
'0x8f84c1d37fa5e21c81a5bf4d3d5f2e718a2d8eb4',
'0x908521c8e53e9bb3b8b9df51e2c6dd3079549382',
'0x85aa7f78bdb2de8f3e0c0010d99ad5853ffcfc63',
'0x909d05f384d0663ed4be59863815ab43b4f347ec',
'0xb4a2810e9d0f1d4d2c0454789be80aaeb9188480',
'0x96fc64f7fe4924546b9204fe22707e3df04be4c8',
'0x226e390751a2e22449d611bac83bd267f2a2caff'
]

Locker_address = [
'0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214',
'0xe2fe530c047f2d85298b07d9333c05737f1435fb',
'0x000000000000000000000000000000000000dead' ]

Burn_address = [
  '0x0000000000000000000000000000000000000000',
  '0x0000000000000000000000000000000000000001',
  '0x0000000000000000000000000000000000000002',
  '0x0000000000000000000000000000000000000003',
  '0x0000000000000000000000000000000000000004',
  '0x0000000000000000000000000000000000000005',
  '0x0000000000000000000000000000000000000006',
  '0x0000000000000000000000000000000000000007',
  '0x0000000000000000000000000000000000000008',
  '0x0000000000000000000000000000000000000009',
  '0x000000000000000000000000000000000000000a',
  '0x000000000000000000000000000000000000000b',
  '0x000000000000000000000000000000000000000c',
  '0x000000000000000000000000000000000000000d',
  '0x000000000000000000000000000000000000000e',
  '0x000000000000000000000000000000000000000f',
  '0x000000000000000000000000000000000000dead',
  '0x000000000000000000000000000000000000DEAD'
]

################################################################################




#################################### 함수들 구현하는 공간 #############################################
# Bit query run 템플릿
def bitquery_run(query):

    # endpoint where you are making the request
    
    headers = {'X-API-KEY': 'BQYgQRzGYhzys0AOlpdpipougQJMH1J8'}
    request = requests.post('https://graphql.bitquery.io/'
                            '',headers=headers,
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        print ('Query failed. return code is {}.      {}'.format(request.status_code, query))


# Locker = '0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214'

locker1_query = '''
{
  ethereum(network: ethereum) {
    arguments(
      argumentType: {is: "uint256"}
      argument: {is: "_unlock_date"}
      smartContractAddress: {is: "0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214"}
      any: {txFrom: {is: "%s"}}
    ) {
      value {
        value
      }
    }
  }
}

'''
#query = locker1_query % '0xd2a9049ca6b66e51c5068414bbbb632bd2c1df9e'
#response = bitquery_run(query)
#arguments = response['data']['ethereum']['arguments']

locker2_query = '''
{
  ethereum(network: ethereum) {
    arguments(
      argumentType: {is: "uint256"}
      argument: {is: "_unlockTime"}
      smartContractAddress: {is: "0xE2fE530C047f2d85298b07D9333C05737f1435fB"}
      any: {txFrom: {is: "%s"}}
    ) {
      value {
        value
      }
    }
  }
}
'''
#query = locker2_query % '0x3598a907ff65a4c952c8f887d25b8ff010304d3e'
#response = bitquery_run(query)
#arguments = response['data']['ethereum']['arguments']

############################## Feature 구하는 함수 #########################################
#
def get_creatorAddress(pair_id,token_id):
    repos_url = 'https://api.ethplorer.io/getAddressInfo/'+token_id+'?apiKey=EK-4L18F-Y2jC1b7-9qC3N'
    response = requests.get(repos_url).text
    repos = json.loads(response)    #json 형태로 token_id에 해당하는 정보를 불러온다.
    
    try:
        creator_address = repos['contractInfo']['creatorAddress']
        if(creator_address == None):
          raise ValueError
    except:     #오류가 나면 이더스캔에서 크롤링
         url = 'https://etherscan.io/address/'+token_id
         try:
             response = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})
             page_soup = BeautifulSoup(response.text, "html.parser")
             Transfers_info_table_1 = str(page_soup.find("a", {"class": "hash-tag text-truncate"}))
             creator_address = re.sub('<.+?>', '', Transfers_info_table_1, 0).strip()
             if(creator_address == 'None'):
                query = mint_query_first % pair_id
                response = run_query(query)
                creator_address = response['data']['mints'][0]['to']
         except Exception as e:  #이더스캔 크롤링까지 에러나면 'Error'로 표시
              print(e)
              creator_address = 'Fail to get Creator Address'
    
    if creator_address in proxy_contracts:
        query = mint_query_first % pair_id
        response = run_query(query)
        creator_address = response['data']['mints'][0]['to']
    
    return creator_address

def get_holders(token_id):
    repos_url = 'https://api.ethplorer.io/getTopTokenHolders/'+token_id+'?apiKey=EK-4L18F-Y2jC1b7-9qC3N&limit=100'
    response = requests.get(repos_url)
    if(response.status_code == 400):
        return []
    repos = json.loads(response.text)    #json 형태로 token_id에 해당하는 정보를 불러온다.
    return repos['holders']

def calc_LP_distribution(holders):
    count = 0
    for holder in holders:
        if(holder['share'] < 0.01 ):
            break
        count = count +1

    LP_avg = 100 / count
    var = 0
    for i in range(count):
        var = var + (holders[i]['share'] - LP_avg) ** 2
    
    LP_stdev = sqrt(var)

    return LP_avg,LP_stdev

def get_Lock_ratio(holders):
    for holder in holders:
        if(holder['address'] in Locker_address):
          return holder['share']
    return 0    

def get_unlock_date(holders,creator):
    for holder in holders:
      if(holder['address'] == '0xe2fe530c047f2d85298b07d9333c05737f1435fb' ):
        query = locker2_query % creator        
      if(holder['address'] == '0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214'):
        query = locker1_query % creator
      if(holder['address'] == '0x000000000000000000000000000000000000dead'):
        return 9999999999 
      try:
        response = bitquery_run(query)
        arguments = response['data']['ethereum']['arguments']
        return int(arguments[-1]['value']['value'])
      except Exception as e:
        print(Fore.LIGHTYELLOW_EX +'[!] Failed to get Liquidity pool\'s lock Expiration date')
        print(Fore.LIGHTYELLOW_EX +'[!] check manually whether token lock expired soon or not')
        return 9999999999 

    
def get_Creator_ratio(holders,creator_address):
    for holder in holders:
        if(holder['address'] == creator_address):
            return holder['share']
    return 0

def call_theGraph_mint(pair_id):
    mint_array = [] 
    timestamp = 0
    try:
      while(True):
        query = mint_query_template % (pair_id,timestamp)
        result = run_query(query)

        if(len(result['data']['mints']) < 1000): # 1000개 미만이니까 끝낸다.
          mint_array.extend(result['data']['mints'])
          break

        mint_array.extend(result['data']['mints'])
        timestamp = result['data']['mints'][999]['timestamp']      
    except Exception as e:
      print('error in theGraph_swap')
      print(e)
      
    return mint_array

def call_theGraph_swap(pair_id):
    swap_array = [] 
    timestamp = 0
    try:
      while(True):
        query = swap_query_template % (pair_id,timestamp)
        result = run_query(query)

        if(len(result['data']['swaps']) < 1000): # 1000개 미만이니까 끝낸다.
          swap_array.extend(result['data']['swaps'])
          break

        swap_array.extend(result['data']['swaps'])
        timestamp = result['data']['swaps'][999]['timestamp']      
    except Exception as e:
      print('error in theGraph_swap')
      print(e)
      
    return swap_array

def call_theGraph_burn(pair_id):
    burn_array = [] 
    timestamp = 0
    try:
      while(True):
        query = burn_query_template % (pair_id,timestamp)
        result = run_query(query)

        if(len(result['data']['burns']) < 1000): # 1000개 미만이니까 끝낸다.
          burn_array.extend(result['data']['burns'])
          break

        burn_array.extend(result['data']['burns'])
        timestamp = result['data']['burns'][999]['timestamp']      
    except Exception as e:
      print('error in theGraph_burn')
      print(e)
      
    return burn_array


def get_mint_mean_period(mint_data_transaction,initial_timestamp):
    count = len(mint_data_transaction)
    if(count == 0):
      return 0
    mint_time_add = 0
    for transaction in mint_data_transaction:
      mint_time_add = mint_time_add + int(transaction['timestamp']) - initial_timestamp
    return mint_time_add / count

def get_swap_mean_period(swap_data_transaction,initial_timestamp):
    count = len(swap_data_transaction)
    if(count == 0):
      return 0
    swap_time_add = 0
    for transaction in swap_data_transaction:
      swap_time_add = swap_time_add +  int(transaction['timestamp']) - initial_timestamp
    return swap_time_add / count

def get_burn_mean_period(burn_data_transaction,initial_timestamp):
    count = len(burn_data_transaction)
    if(count == 0):
      return 0
    burn_time_add = 0
    for transaction in burn_data_transaction:
      burn_time_add = burn_time_add + int(transaction['timestamp']) - initial_timestamp
    return burn_time_add / count

def swap_IO_rate(swap_data_transaction,index):
  swapIn = 0
  swapOut = 0
  if(index == 1): #amount0이 이더.
    for data in swap_data_transaction:
      if(data['amount0In'] == '0'): #amount0Out이 0이 아니란 말. 
        swapOut = swapOut + 1
      else:   
        swapIn = swapIn + 1
  else:         #amount1이 이더
    for data in swap_data_transaction:
      if(data['amount1In'] == '0'):
        swapOut = swapOut + 1
      else:
        swapIn = swapIn +1
  
  return swapIn,swapOut 

def get_last_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction):
  #mint_data_transaction은 0일 수가 없다. 
  swap_len = len(swap_data_transaction)
  burn_len = len(burn_data_transaction)
  #Case 1 Swap / Burn 전부 0 인경우
  if(swap_len == 0 and burn_len == 0):
    return int(mint_data_transaction[-1]['timestamp'])
  #Case 2 Swap_transaction이 0 인경우
  if(swap_len == 0):
    return int(max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp']))
  #Case 3 Burn Transaction이 0 인경우
  if(burn_len == 0):
    return int(max(mint_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']))
  #Case 4 전부다 있는 경우
  return int(max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']))


def token_index(pair):
  if(pair.token0.name == 'Wrapped Ether'):
    return 1
  else:
    return 0
    # if(data['token0.name'] == 'Wrapped Ether'):
    #     return 1
    # else:
    #     return 0

def get_burn_ratio(holders):
  for holder in holders:
    if(holder['address'] in Burn_address):
      return holder['share']
    
  return 0

def get_creator_ratio(holders,creator_address):
  for holder in holders:
    if(holder['address'] == creator_address):
      return holder['share']
  
  return 0


#### 스캠 토큰 판별 관련 함수
def get_initial_Liquidity_token(mint_data_transaction,index):
  if(index == 1):
    return Decimal(mint_data_transaction[0]['amount1'])
  else:
    return Decimal(mint_data_transaction[0]['amount0'])


def get_last_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction):
  #mint_data_transaction은 0일 수가 없다. 
  swap_len = len(swap_data_transaction)
  burn_len = len(burn_data_transaction)
  #Case 1 Swap / Burn 전부 0 인경우
  if(swap_len == 0 and burn_len == 0):
    return int(mint_data_transaction[-1]['timestamp'])
  #Case 2 Swap_transaction이 0 인경우
  if(swap_len == 0):
    return int(max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp']))
  #Case 3 Burn Transaction이 0 인경우
  if(burn_len == 0):
    return int(max(mint_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']))
  #Case 4 전부다 있는 경우
  return int(max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']))
  
def get_swap_amount(swap_data_transaction,j,eth_amountIn,eth_amountOut):
  if(swap_data_transaction[j][eth_amountIn] == '0'): #amountIn이 0 이면 out이라는 거지.
    return Decimal(swap_data_transaction[j][eth_amountOut]) * (-1)
  else:
    return Decimal(swap_data_transaction[j][eth_amountIn])

def get_swap_token(swap_data_transaction,j,index):
  if(index == 1):
    swap_amount = Decimal(swap_data_transaction[j]['amount1In'])
    swap_amount = Decimal(swap_amount) - Decimal(swap_data_transaction[j]['amount1Out'])
  else:
    swap_amount = Decimal(swap_data_transaction[j]['amount0In'])
    swap_amount = Decimal(swap_amount) - Decimal(swap_data_transaction[j]['amount0Out'])

  return swap_amount  

def get_timestamp(data_transaction,index):
  try:
    return data_transaction[index]['timestamp']
  except:
    return '99999999999'

def check_rugpull(before_transaction_Eth, current_Eth):
  if ( abs(Decimal(current_Eth) / Decimal(before_transaction_Eth)) <= 0.01 ):
    if( Decimal(before_transaction_Eth) < 0 or Decimal(current_Eth) < 0): #순서가 바뀐 경우에 의해서 풀의 이더가 음수인 경우 그냥 exit
      return False
    else:
      return True
  else:
    return False

def is_MEV(initial_Liquidity_token, swapIn_token):
  if(swapIn_token > initial_Liquidity_token * 5): #초기 공급 토큰의 양보다 5배가 많은 양이 스왑이 들어오면 swap rugpull로 판단
    return False    #얘는 진짜 러그풀인 경우
  else:
    return True     #얘는 MEV애들 때문에 발생한 RugPull 오탐인 경우


def get_rugpull_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction,index):
    if(index == 1):
      eth_amount = 'amount0'
      eth_amountIn = 'amount0In'
      eth_amountOut = 'amount0Out'
    else:
      eth_amount = 'amount1'
      eth_amountIn = 'amount1In'
      eth_amountOut = 'amount1Out'
    
    #각각 배열의 길이를 구해서 반복문 끝 조절
    swap_count = len(swap_data_transaction)
    burn_count = len(burn_data_transaction)

    
    #유동성에 남아있는 이더를 지속적으로 보면서 러그풀이 언제 발생하는지 탐지
    current_Liquidity_Eth = Decimal(mint_data_transaction[0][eth_amount]) # mint[0]의 값으로 초기화
    initial_Liquidity_token = get_initial_Liquidity_token(mint_data_transaction,index)
    i,j,k = 1,0,0   #mint,swap,burn 배열의 인덱스
    
    while True:
      try:  
        next_timestamp = min(get_timestamp(mint_data_transaction,i),get_timestamp(burn_data_transaction,k))
        #swap 인 경우 current_Eth 더하는 로직 / 러그풀 타임스탬프 체크
        while(get_timestamp(swap_data_transaction,j) <= next_timestamp ):
          if(get_timestamp(swap_data_transaction,j) == '99999999999'):
            break

          #swap이 제일 타임스탬프가 작은 경우니까 스왑에 맞게 amount +-를 하면 된다.
          before_transaction_Eth = current_Liquidity_Eth
          current_Liquidity_Eth = current_Liquidity_Eth + get_swap_amount(swap_data_transaction,j,eth_amountIn,eth_amountOut)
          #print("swap {before : %s swap_amount : %s"%(str(before_transaction_Eth),str(current_Liquidity_Eth-before_transaction_Eth)))

          if( check_rugpull(before_transaction_Eth,current_Liquidity_Eth) ):  #러그풀 탐지 로직에 의해 탐지가 되고
              if( is_MEV(initial_Liquidity_token,get_swap_token(swap_data_transaction,j,index)) == False ):  #MEV검사 까지 해서 아니면 진짜 러그풀인 것
          #      print("swap rugpull : initial token = %s / before Eth = %s / after Eth = %s swapIn_token_amount = %s"%(initial_Liquidity_token,str(before_transaction_Eth),str(current_Liquidity_Eth),get_swap_token(swap_data_transaction,j,index)))
                return get_timestamp(swap_data_transaction,j), Decimal(current_Liquidity_Eth / before_transaction_Eth) -1, True, before_transaction_Eth,current_Liquidity_Eth,'swap',swap_data_transaction[j]['transaction']['id']      
          j = j+1

        #mint 인 경우 curruent_Eth 더하는 로직
        if(next_timestamp == get_timestamp(mint_data_transaction,i)): #mint가 최소라면, + 한다.
          if(next_timestamp == '99999999999'):  #이건 rugpull이 없는 경우
            try:
                #여기까지 온거면 rugpull이 없는 경우인데 이때 네가지 케이스에 대한 예외케이스를 정의 해야한다.
                #Case 1 Swap/Burn이 없는 경우
                if(swap_count == 0 and burn_count == 0):
                    return mint_data_transaction[-1]['timestamp'],0, False, 0,0,'',-1
                #Case 2 Swap이 없는 경우 
                if(swap_count == 0):
                    return max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp']),0,False, 0,0,'',-1
                #Case 3 Burn이 없는 경우
                if(burn_count == 0):
                    return max(mint_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']),0,False, 0,0,'',-1
                #Case 4 Mint/Swap/Burn이 다 있지만, Rugpull이 아닌 경우
                return max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']),0,False, 0,0,'',-1
            except:
              return 'Error occur',100.0,False,1,1,'',-1
          before_transaction_Eth = current_Liquidity_Eth
          current_Liquidity_Eth = current_Liquidity_Eth + Decimal(mint_data_transaction[i][eth_amount])
          #print("mint {before : %s burn_amount : %s"%(str(before_transaction_Eth),str(current_Liquidity_Eth-before_transaction_Eth))) 
          i = i+1

        #burn 인 경우 current_Eth 빼는 로직 / 러그풀 타임스탬프 체
        else:
          before_transaction_Eth = current_Liquidity_Eth
          current_Liquidity_Eth = current_Liquidity_Eth - Decimal(burn_data_transaction[k][eth_amount])
          #print("burn {before : %s burn_amount : %s"%(str(before_transaction_Eth),str(current_Liquidity_Eth-before_transaction_Eth)))
          if(check_rugpull(before_transaction_Eth,current_Liquidity_Eth)):
            return get_timestamp(burn_data_transaction,k), Decimal(current_Liquidity_Eth / before_transaction_Eth) -1, True, before_transaction_Eth,current_Liquidity_Eth,'burn',burn_data_transaction[k]['transaction']['id']
          k = k+1
      except Exception as e:
        print(e)
        print('Critical Error Occur')
        return '1',0,False,1,1,'Error',-1


def is_rugpull_occur(pair):
  try:
    pair_address = pair.id
    token_id = pair.token00.id
    mint_data_transaction = call_theGraph_mint(pair_address)
    swap_data_transaction = call_theGraph_swap(pair_address)
    burn_data_transaction = call_theGraph_burn(pair_address)
    
    rugpull_timestamp, rugpull_change, is_rugpull, before_rugpull_Eth, after_rugpull_Eth,rugpull_method,tx_id = get_rugpull_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction,token_index(pair))

    if(is_rugpull == True):
      return {'is_scam' : True,
       'token_id' : token_id,
       'tx_id' : tx_id,
       'rugpull_timestamp' : rugpull_timestamp,
       'before_ETH' : before_rugpull_Eth,
       'after_ETH' : after_rugpull_Eth,
       'rugpull_method' : rugpull_method,
       'rugpull_change' : rugpull_change
       }
    else:
      return {'is_scam' : False}
  except Exception as e:
      print('Exception in is_rugpull()',e)
      return {'is_scam' : False}
      

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def check_similarity(scam_contracts,token_id):
  try:
    repos_url = 'https://api.etherscan.io/api?module=contract&action=getsourcecode&address='+token_id+'&apiKey=A78Z2CZPJI82R1QCSCDX61P4HF9KQXGX8D'
    response = requests.get(repos_url).text
    result = json.loads(response)
    sourcecode = result["result"][0]["SourceCode"]
    abi = result["result"][0]['ABI']

    # abi를 통해서 verified 되었는지 확인
    if 'Contract source code not verified' in abi :
      verified = 0
      return verified,'0x0000',0
    else:
      verified = 1
    
    # scam_contracts에서 유사도 검증을 통해서 가장 유사한 컨트랙트와, 유사도 점수를 구해서 리턴
    max_simratio = 0
    for scam_contract in scam_contracts:
      groupcode = scam_contract['groupcode']
      address = scam_contract['address']
      simratio = similar(sourcecode, groupcode)
      if(simratio > max_simratio):
        max_simratio = simratio
        max_address = address
        
    return verified,max_address,max_simratio

  except Exception as e:
    print("Error in check_similarity method")
    print(e)