import requests


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


def run_query(query):

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
  response = run_query(query) #height 값 구해옴
  try:
    block_height = response['data']['ethereum']['transactions'][0]['block']['height']

    query = query_create %(token_address,block_height)
    response = run_query(query)
    transfers = response['data']['ethereum']['transfers'] #list

    for transfer in transfers:
      initial_supply = initial_supply + transfer['amount']
      receiver_list.append(transfer['receiver'])

  except:

    return -1,-1

  return initial_supply,receiver_list

