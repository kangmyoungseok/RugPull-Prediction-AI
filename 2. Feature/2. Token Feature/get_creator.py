import requests
import pandas as pd
from tqdm import tqdm
import json
from bs4 import BeautifulSoup
import re
mint_query_template = '''
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
def run_query(query):

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


def get_creatorAddress(data):
    token_id = data['token00.id']
    repos_url = 'https://api.ethplorer.io/getAddressInfo/'+token_id+'?apiKey=EK-4L18F-Y2jC1b7-9qC3N'
    response = requests.get(repos_url).text
    repos = json.loads(response)    #json 형태로 token_id에 해당하는 정보를 불러온다.
    
    try:
        creator_address = repos['contractInfo']['creatorAddress']
        print('find by ethplorer : ' + token_id)
    except:     #오류가 나면 이더스캔에서 크롤링
        url = 'https://etherscan.io/address/'+token_id
        response = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'})
        page_soup = BeautifulSoup(response.text, "html.parser")
        Transfers_info_table_1 = str(page_soup.find("a", {"class": "hash-tag text-truncate"}))
        creator_address = re.sub('<.+?>', '', Transfers_info_table_1, 0).strip()
        print('find by etherscan : ' + token_id)
        print('result : ' + creator_address)
         

    data['creator_address'] = creator_address
    return data

datas = pd.read_csv('Creator_list_v1.2.csv',encoding='utf-8-sig').to_dict('records')
len(datas)

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




for data in tqdm(datas,desc="개발자 찾기:"):
        if(data['creator_address'] in proxy_contracts):
            query = mint_query_template % data['id']
            response = run_query(query)
            creator_address = response['data']['mints'][0]['to']
            data['creator_address'] = creator_address        



pd.DataFrame(datas).to_csv('Creator_list_v1.2.csv',encoding='utf-8-sig',index=False)

