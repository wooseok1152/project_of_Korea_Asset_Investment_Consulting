from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd

def df_to_csv(csv_material_file_path : str) :

    today      = datetime.today().strftime("%Y%m%d")

    df_etf_basic_info = stock.get_etf_ticker_name(stock.get_etf_ticker_list()).reset_index()

    df_etf_basic_info["기준일자"] = today
    df_etf_basic_info.rename(columns = {"ticker" : "단축코드", "종목명" : "한글종목명"}, inplace = True)
    df_etf_basic_info = df_etf_basic_info.astype({"단축코드" : "str"})
    df_etf_basic_info["단축코드"] = "A" + df_etf_basic_info["단축코드"]
    df_etf_basic_info = df_etf_basic_info.loc[:, ["기준일자", "단축코드", "한글종목명"]]

    df_etf_basic_info.to_csv(csv_material_file_path, index = None, encoding="utf-8", na_rep = '\\N')

    return "making a csv file finished"  

