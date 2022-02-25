from dataset import Dataset
from lib.Thegraph import *
from lib.FeatureLib import *
from pair import *
import pandas as pd
import time
from colorama import Fore,init
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
import os
import argparse
from datetime import datetime



'''
pair = get_pair("0xb73428a159a02a4b377e940d0919eb5ba91c67e7")
result = is_rugpull_occur(pair)
datetimeobj
'''



def get_pair(token_address) -> Pair:
    query1,query2 = query_pair(token_address)
    result = run_query(query1)
    result['data']['pairs'].extend(run_query(query2)['data']['pairs'])

    for data in result['data']['pairs']:
        if((data['token0']['symbol'] == 'WETH') or (data['token1']['symbol'] =='WETH' )):
            token0 = Token(data['token0'])
            token1 = Token(data['token1'])
            pair = Pair(data,token0,token1)
            pair.setToken00()
            break
        else:
            continue

    try:
        print(Fore.BLUE + "[+] Successfully get information of token {}".format(pair.token00.id))
        return pair
    except NameError:
        print(Fore.RED + """
[-] Failed to get infromation of token {} 
check if this token is in UNISWAP v2 and has pool with WETH""".format(token_address))
        exit(0)


## main ##
def main() -> None:
    init(autoreset=True)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    print(Fore.BLUE + """
[!] RUGPULL PREDICTION AI MODEL (MADE BY BOBAI)
[!] Github repo: https://github.com/kangmyoungseok/RugPull_Prediction_AI
""")

    parser = argparse.ArgumentParser(description='RUGPULL PREDICTION AI MODEL')
    parser.add_argument('--address',
                        metavar='address',
                        type=str,
                        required=True,
                        help='Enter Token Address for RUGPULL CHECK & AI Prediction')

    parser.add_argument('--verbose', '-v', action='count', default=0,help='See detail report for token')
    args = parser.parse_args()

    if not os.path.isfile('ann97.h5'):
        print(Fore.RED + '[-] AI MODEL IS NOT INSTALLED')
        raise SystemExit(1)
    

    # get token data from thegrpah API : https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v2
    pair = get_pair(args.address)
    # Check whether rugpull occurred or not
    result = is_rugpull_occur(pair)
    if(result['is_scam']):
        datetimeobj = datetime.fromtimestamp(int(result['rugpull_timestamp']))
        print()
        print(Fore.MAGENTA + "[*] RUGPULL IS ALREADY OCCRED IN THIS TOKEN")
        print(Fore.MAGENTA + "[*] EVENT TX_ID : " + result['tx_id'])
        print(Fore.MAGENTA + "[*] AT TIME " + datetimeobj.strftime('%Y-%m-%d %H:%M:%S'))
        print(Fore.MAGENTA + "[*] RUGPULL IS DRIVEN BY {} TRANSACTION".format(result['rugpull_method']))
        print(Fore.MAGENTA + "[*] 'WETH' IN LIQUIDITY PULL IS DECREADED BY {}%".format(float(result['rugpull_change'])*100))
        print(Fore.MAGENTA + "[*] Before WETH in Liquidity pool : {}, After WETH : {}".format(result['before_ETH'],result['after_ETH']))        
        print(Fore.RED     + "[*] See : https://etherscan.io/tx/{}".format(result['tx_id']))
        exit(0)

    else:
        print()
        print(Fore.MAGENTA + "[+] RUGPULL IS NOT OCCURED IN THIS TOKEN YET.")
        print(Fore.MAGENTA + "[+] START COLLECING DATA FOR RUGPULL PREDICTION")

    # if rugpull is not occurred yet, then calculate Rugpull prediction AI Score

    # Collect Data to Calculate AI Feature
    token_creator = get_creatorAddress(pair.id,pair.token00.id)

    lp_holders = get_holders(pair.id)
    lp_lock_ratio = get_Lock_ratio(lp_holders)
    lp_avg,lp_std = calc_LP_distribution(lp_holders)
    lp_creator_holding_ratio = get_Creator_ratio(lp_holders,token_creator)

    mint_data_transaction = call_theGraph_mint(pair.id)
    swap_data_transaction = call_theGraph_swap(pair.id)
    burn_data_transaction = call_theGraph_burn(pair.id)

    mint_count = len(mint_data_transaction)
    swap_count = len(swap_data_transaction) 
    burn_count = len(burn_data_transaction)

    initial_timestamp = int(mint_data_transaction[0]['timestamp'])
    last_timestamp = get_last_timestamp(mint_data_transaction,swap_data_transaction,burn_data_transaction)
    active_period = last_timestamp - initial_timestamp

    mint_mean_period = int(get_mint_mean_period(mint_data_transaction,initial_timestamp))
    swap_mean_period = int(get_swap_mean_period(swap_data_transaction,initial_timestamp))
    burn_mean_period = int(get_burn_mean_period(burn_data_transaction,initial_timestamp))

    swap_in,swap_out = swap_IO_rate(swap_data_transaction,token_index(pair))

    token_holders = get_holders(pair.token00.id)   
    token_burn_ratio = get_burn_ratio(token_holders)
    token_creator_holding_ratio = get_creator_ratio(token_holders,token_creator)
    if(lp_lock_ratio > 0):
        unlock_date = get_unlock_date(lp_holders,token_creator)
    else:
        unlock_date = 0

    # if lock is expired or will be expired in 3days, then set lock_ratio to 0.
    current_time = int(time.time())
    if( unlock_date - current_time < 259200):
        print(Fore.RED + '''
[!] Alert!! Token's lock will be expired soon. Be careful regardless of AI Score
[!] Lots of Rugpull occur after Token's Lock is expired
        ''')
        lp_creator_holding_ratio += lp_lock_ratio # if lock is expired, creator will get LP Token back
        lp_lock_ratio = 0

    # print detail information if -v option is specified
    if(args.verbose > 0):
        print(Fore.LIGHTBLUE_EX+'[Pair Info] https://etherscan.io/token/{}'.format(pair.id))
        print(Fore.LIGHTBLUE_EX+'[Pair Info] Uniswap Pair Address : {}'.format(pair.id))
        print(Fore.LIGHTBLUE_EX+'[Pair Info] Liquidity Pool\'s Reserved : {}Eth'.format(float(pair.reserveETH)/2))
        print(Fore.LIGHTBLUE_EX+'[Pair Info] Liquidity Pool\'s Lock Ratio : {}'.format(lp_lock_ratio))
        print(Fore.LIGHTBLUE_EX+'[Pair Info] Liquidity Pool\'s Lock Expiration Date : {}\n'.format(datetime.fromtimestamp(int(unlock_date)).strftime('%Y-%m-%d %H:%M:%S')))

        print(Fore.LIGHTBLUE_EX+'[Token Info] https://etherscan.io/token/{}'.format(pair.token00.id))
        print(Fore.LIGHTBLUE_EX+'[Token Info] Token Creator : {}'.format(token_creator))
        print(Fore.LIGHTBLUE_EX+'[Token Info] Swap In(buy token with Ether) count : {}'.format(swap_in))
        print(Fore.LIGHTBLUE_EX+'[Token Info] Swap Out(Sell Token) count : {}'.format(swap_out))

        



    # insert data into dataset / total 18 features.
    dataset1 = {}
    dataset1['id'] = pair.id
    dataset1['mint_count_per_week'] = mint_count / ((int(active_period) / (60* 60 * 24 * 7)) + 1)
    dataset1['burn_count_per_week'] = burn_count / ((int(active_period) / (60* 60 * 24 * 7)) + 1)
    dataset1['mint_ratio'] = mint_count / (mint_count + burn_count + swap_count)
    dataset1['swap_ratio'] = swap_count/ (mint_count + burn_count + swap_count)
    dataset1['burn_ratio'] = burn_count / (mint_count + burn_count + swap_count)
    dataset1['mint_mean_period'] = mint_mean_period / active_period
    dataset1['swap_mean_period'] = swap_mean_period / active_period
    dataset1['burn_mean_period'] = burn_mean_period / active_period
    dataset1['swap_in_per_week'] = swap_in /((int(active_period) / (60* 60 * 24 * 7)) + 1)
    dataset1['swap_out_per_week'] = swap_out / ((int(active_period) / (60* 60 * 24 * 7)) + 1)
    dataset1['swap_rate'] = swap_in / (swap_out + 1)
    dataset1['lp_avg'] = lp_avg 
    dataset1['lp_std'] = lp_std
    dataset1['lp_creator_holding_ratio'] = lp_creator_holding_ratio
    dataset1['lp_lock_ratio'] = lp_lock_ratio
    dataset1['token_burn_ratio'] = token_burn_ratio
    dataset1['token_creator_holding_ratio'] = token_creator_holding_ratio
    dataset1['number_of_token_creation_of_creator'] = 1


    # Calcalate AI Score
    train = pd.read_csv('Dataset_v1.9.csv').drop(columns=['Label']).to_dict('records')
    train.append(dataset1)

    dataset = pd.DataFrame(train)
    origin = dataset

    dataset = dataset.drop(columns=['id'])
    dataset = dataset.dropna(how='any', axis=0)

    # Normalizaion
    scaler = MinMaxScaler()
    dataset[ : ] = scaler.fit_transform(dataset[ : ])

    model = keras.models.load_model('ann97.h5')
    #model.summary()
    
    result = model.predict(dataset)
    origin['predict'] = result
    
    result = origin.to_dict('records')[-1]['predict']
    

    if(result < 0.5):
        print(Fore.GREEN+'[+] Probabiliy of Rugpull is : {}%'.format(round(result*100,2)))
        print(Fore.GREEN+'[+] Our AI indicate this token is Safe')
    else:
        print(Fore.YELLOW+'[+] Probabiliy of Rugpull is : {}%'.format(round(result*100,2)))
        print(Fore.YELLOW+'[+] Our AI indicate this token is Dangerous')




if __name__ == "__main__":
    main()
