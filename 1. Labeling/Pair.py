from pprint import pprint
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import json
from bs4 import BeautifulSoup
import re # 추가
from urllib.request import urlopen
import requests
import time

# swap function makes scam token to token0
def switch_token(result):
    for pair in result['data']['pairs']:
        if (int(pair['token0']['txCount']) > int(pair['token1']['txCount'] )):
            pair['reserve00'] = pair['reserve1']
            pair['token00'] = pair['token1']
        else:
            pair['reserve00'] = pair['reserve0']
            pair['token00'] = pair['token0']
    
# function to use requests.post to make an API call to the subgraph url
def run_query(query):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


query_init = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
 }
}
''' 


query_iter = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where: {createdAtBlockNumber_lt:initial}) {
   id
   token0{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   token1{
    id
    symbol
    name
    txCount
    totalLiquidity
    decimals
  }
   reserve0
   reserve1
   totalSupply
   reserveUSD
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
 }
}
''' 

pair_frame = [] # 쿼리의 결과를 여기에 List 형태로 담을 것. 50000개

##### 맨 처음 쿼리. 반복문 불가####
query = query_init
result = run_query(query)
switch_token(result)
for pair in result['data']['pairs']:
    if((pair['token0']['symbol'] != 'WETH') and (pair['token1']['symbol'] !='WETH' )):
      continue
    if((pair['token00']['txCount'] == 0) or (pair['token00']['txCount'] == '0') or (pair['txCount'] == '0')):
      continue
    year = time.gmtime(int(pair['createdAtTimestamp'])).tm_year
    month = time.gmtime(int(pair['createdAtTimestamp'])).tm_mon
    day = time.gmtime(int(pair['createdAtTimestamp'])).tm_mday
    pair['createdAtDate'] = str(year) + '-' + str(month) + '-' + str(day)
    pair_frame.append(pair)

last_block = result['data']['pairs'][999]['createdAtBlockNumber']
query_iter = query_iter.replace('initial',last_block)
query = query_iter

try:
    while(1):
        result = run_query(query_iter)
        switch_token(result)
        for pair in result['data']['pairs']:
            if((pair['token0']['symbol'] != 'WETH') & (pair['token1']['symbol'] !='WETH' )):
              continue
            if((pair['token00']['txCount'] == 0) or (pair['token00']['txCount'] == '0') or (pair['txCount'] == '0')):
              continue
            year = time.gmtime(int(pair['createdAtTimestamp'])).tm_year
            month = time.gmtime(int(pair['createdAtTimestamp'])).tm_mon
            day = time.gmtime(int(pair['createdAtTimestamp'])).tm_mday
            pair['createdAtTDate'] = str(year) + '-' + str(month) + '-' + str(day)
            pair_frame.append(pair)
        query_iter = query_iter.replace(last_block,result['data']['pairs'][999]['createdAtBlockNumber'])
        if( int(result['data']['pairs'][999]['createdAtTimestamp'])  < 10966879):
          break
        last_block = result['data']['pairs'][999]['createdAtBlockNumber']
        print(last_block)
        

except Exception as e:
    try:
      print(result['errors'])
    except:
      print(e)
    df = pd.json_normalize(pair_frame)
    df.to_csv('Pairs_v2.1.csv',encoding='utf-8-sig',index=False)



