import requests
from datetime import datetime
from decimal import Decimal
import json

#Contract의 Create가 된 시점의 Block Height
query_height='''
{
  ethereum(network: ethereum) {
    transactions {
      creates(txCreates: {is: "%s"}) # token address
      {
        address
      }
      block {
        height
        
      }
    }
  }
}
'''
#주어진 Block Height시점에 Transfer된 토큰의 양
query_create='''
{
    ethereum(network: ethereum) {  
        transfers(
            currency: {is: "%s"}
            height: {is: %s}
        ) {
        amount
        receiver {
            address
        }
        }
    }
}
'''
#해당 TimeStamp 시점에 Burn 된 토큰의 양
query_burn_amount = '''
{
  ethereum(network: ethereum) {
    transfers(time: {since: null, before: "%s"}, amount: {gt: 0}) {
      burned: amount(
        calculate: sum
        receiver: {in: ["0x0000000000000000000000000000000000000000", "0x0000000000000000000000000000000000000001", "0x000000000000000000000000000000000000dead"]}
      )
      currency(currency: {is: "%s"}) {
        address
      }
    }
  }
}
'''

#토큰의 첫번째 Transaction의 TimeStamp를 구한다.
query_token_first_timestamp='''
{
  ethereum {
    transfers(
      options: {asc: "block.timestamp.iso8601", limit: 1}
      amount: {gt: 0}
      currency: {is: "%s"}
    ) {
      block {
        timestamp {
          iso8601
        }
      }
    }
  }
}
'''

#특정 시점에 Creator가 가지고 있는 token의 양
query_creator_token_amount='''
{
  ethereum(network: ethereum) {
    address(address: {is: "%s"}) {
      balances(time: {before: "%s"}, currency: {is: "%s"}) {
        value
      }
    }
  }
}
'''



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

def get_initial_supply(token_address):
  initial_supply = 0
  receiver_list = []


  query = query_height % token_address
  response = bitquery_run(query) #height 값 구해옴
  try:
    block_height = response['data']['ethereum']['transactions'][0]['block']['height']

    query = query_create %(token_address,block_height)
    response = bitquery_run(query)
    transfers = response['data']['ethereum']['transfers'] #list

    for transfer in transfers:
      initial_supply = initial_supply + transfer['amount']
      receiver_list.append(transfer['receiver'])

  except:

    return -1,-1

  return initial_supply,receiver_list

def call_bitquery_burn_amount_func(timestamp,token_address):
    query = query_burn_amount % (timestamp,token_address)
    response = bitquery_run(query)
    try:
        burn_amount = Decimal(response['data']['ethereum']['transfers'][0]['burned'])
    except:
        burn_amount = '0'
    
    return burn_amount

def call_bitquery_creator_token_amount_func(creator_address,timestamp,token_address):
    query = query_creator_token_amount % (creator_address,timestamp,token_address)
    response = bitquery_run(query)
    try:
        # print (result)
        creator_token_amount = Decimal(response['data']['ethereum']['address'][0]['balances'][0]['value'])
    except:
        print('error2')
        creator_token_amount = -1
    
    return creator_token_amount

def call_bitquery_creator_LP_amount_func(LP_creator_address,timestamp,pair_address):
    query = query_creator_token_amount % (LP_creator_address,timestamp,pair_address)
    result = bitquery_run(query)
    try:
       # print (result)
        creator_LP_amount = result['data']['ethereum']['address'][0]['balances'][0]['value']
    except:
        print('error3')
        creator_LP_amount = -1
    
    return creator_LP_amount

def call_etherscan_current_total_supply(token_address,decimals):
    etherscan_api_key = 'VFQIHCD19UDTRRDQUYF19HZK3QS1Y8ZXBF'
    repos_url = 'https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress='+token_address+'&apikey='+etherscan_api_key
    try:
        response = requests.get(repos_url).json()
        current_total_supply =  (float(response['result']) / decimals)
    except:
        current_total_supply = -1
        
    return current_total_supply


    