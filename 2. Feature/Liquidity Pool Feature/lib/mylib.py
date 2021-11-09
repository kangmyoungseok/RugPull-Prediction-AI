import os
import pandas as pd
import glob
from pandas.core.accessor import delegate_names
from pandas.core.frame import DataFrame
import requests

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def split_csv(total_csv):
    rows = pd.read_csv(total_csv,chunksize=5000)
    file_count = 0
    for i, chuck in enumerate(rows):
        chuck.to_csv('./result/out{}.csv'.format(i),encoding='utf-8-sig',index=False)
        file_count = file_count+1 
    return file_count


def merge_csv():
  input_file = r'./result/'
  output_file = r'./result/result'

  allFile_list = glob.glob(os.path.join(input_file, 'fout*')) # glob함수로 sales_로 시작하는 파일들을 모은다
  allFile_list.sort()
  for file in allFile_list:
      output_file = output_file + file[-5] 
  output_file = output_file +'.csv'

  all_Data = []
  for file in allFile_list:
    records = pd.read_csv(file).to_dict('records') 
    all_Data.extend(records)

  DataFrame(all_Data).to_csv(output_file,encoding='utf-8-sig',index=False)
  print("결과물 파일 : " + output_file)


