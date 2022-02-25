import requests

def query_pair(token_address) -> str:
  query1 = '''
  {
  pairs(first: 100, orderBy: createdAtBlockNumber, orderDirection: desc, where:{ token0_contains: "%s"}) {
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
  ''' % token_address
  query2 = '''
  {
  pairs(first: 100, orderBy: createdAtBlockNumber, orderDirection: desc, where:{ token1_contains: "%s"}) {
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
  ''' % token_address
  return query1,query2


query_pairs = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where:{createdAtTimestamp_lt : %s}) {
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

query_pairs = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where:{createdAtTimestamp_lt : %s}) {
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


query_latest = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: asc, where: {createdAtTimestamp_gt:%s}) {
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
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: asc, where: {createdAtTimestamp_gte:"%s"}) {
   id
   reserveETH
   txCount
   createdAtTimestamp
 }
}
''' 

query_scam_iter = '''
{
 pairs(first: 1000, orderBy: createdAtBlockNumber, orderDirection: desc, where: {createdAtTimestamp_lt:%s}) {
   id
   reserveETH
   txCount
   createdAtTimestamp
   createdAtBlockNumber
 }
}
''' 

mint_query_first = '''
{
  mints(first: 1, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" }) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
'''

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
      transaction{
        id
      }
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
      transaction{
        id
      }
 }
}
''' 

def switch_token(result):
    for pair in result['data']['pairs']:
        if (int(pair['token0']['txCount']) > int(pair['token1']['txCount'] )):
            pair['reserve00'] = pair['reserve1']
            pair['token00'] = pair['token1']
        else: 
            pair['reserve00'] = pair['reserve0']
            pair['token00'] = pair['token0']

def run_query(query):
    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

