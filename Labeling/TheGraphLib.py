import requests

mint_query_template = '''
{
  mints(first: 1000, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" , timestamp_gt:%s  }) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
''' 

swap_query_template = '''
{
  swaps(first: 1000, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" , timestamp_gt:%s }) {
      amount0In
      amount0Out
      amount1In
      amount1Out
      to
      sender
      timestamp
 }
}
''' 


burn_query_template = '''
{
  burns(first: 1000, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" , timestamp_gt:%s }) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
''' 


def run_query(query):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

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

