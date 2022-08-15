import os
import pandas as pd
import numpy as np
import time

def load_is_dataset(download_directory_path : str) :
    
    """ 

    'downloads'디렉토리에 가장 최근에 저장된 csv파일을 dataframe으로 읽기 
    (14행 ~ 22행)
    
    """
    
    file_name_and_time_lst = []
    for f_name in os.listdir(f"{download_directory_path}"):

        modified_time = os.path.getmtime(f"{download_directory_path}{f_name}")
        file_name_and_time_lst.append((f_name, modified_time))

    sorted_file_lst = sorted(file_name_and_time_lst, key=lambda x: x[1], reverse=True)
    recent_file_info = sorted_file_lst[0]
    recent_csv_file_path = download_directory_path + recent_file_info[0]

    df = pd.read_csv(recent_csv_file_path, encoding='euc-kr')

    return (df, recent_csv_file_path)

def pre_process_df(df) :

    df["기준일자"] = time.strftime("%Y%m%d")
    df["상장일"] = df["상장일"].str.replace("/", "")
    df["액면가"] = df["액면가"].replace("무액면", np.NaN)
    df["단축코드"] = 'A' + df["단축코드"]
    
    df = df.loc[:, ["기준일자", "표준코드", "단축코드", "한글 종목명", "한글 종목약명", "영문 종목명", "상장일", "시장구분", "증권구분", "소속부", "주식종류", "액면가", "상장주식수"]]

    return df

    