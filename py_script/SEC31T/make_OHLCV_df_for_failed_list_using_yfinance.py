import time
import pandas as pd
from pandasql import sqldf
from datetime import datetime, timedelta
# import FinanceDataReader as fdr
import yfinance as yf

def make_OHLCV_df_for_failed_list_using_yfinance(failed_list : list, start_date : str) :

    stock_code_list = failed_list
    print("* stock_code_list length :", len(stock_code_list))

    df_OHLCV_by_base_date_and_is_for_failed = pd.DataFrame()
    
    failed_list_not_making_error_twice = []
    failed_list_making_error_twice = []

    for i, stk in enumerate(stock_code_list) :

        try : 

            start = time.time()

            print("\n" + "* {} start. Number is {}".format(stk, i))
            df_one_stock_by_base_date= yf.download(stk, start = start_date[:4] + '-' + start_date[4:6] + '-' + start_date[6:]).reset_index()
            
            if df_one_stock_by_base_date.size == 0:

                failed_list_not_making_error_twice.append(stk)
                print("* {} failed. It dosen't have any OHLCV".format(stk), "\n")
                time.sleep(1)
                continue

            df_one_stock_by_base_date.rename(columns = {"Date" : "기준일자", "Close" : "종가", "Open" : "시가", "High" : "고가", "Low" : "저가", "Volume" : "거래량", "Adj Close" : "수정종가"}, inplace = True)
            df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"기준일자" : "str"})
            df_one_stock_by_base_date["기준일자"] = df_one_stock_by_base_date["기준일자"].str.replace("-", "")
            df_one_stock_by_base_date["야후종목코드"] = stk
            df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"거래량" : "int"})
            
            df_one_stock_by_base_date = df_one_stock_by_base_date.loc[:, ['기준일자', '야후종목코드', '시가', '고가', '저가', '종가', '수정종가', '거래량']]
            df_OHLCV_by_base_date_and_is_for_failed = pd.concat([df_OHLCV_by_base_date_and_is_for_failed, df_one_stock_by_base_date])

            print("* {} finished. It takes {}sec".format(stk, time.time() - start), "\n")
            time.sleep(1)
        
        except Exception as e :

            failed_list_making_error_twice.append(stk)
            print("* {} makes error.".format(stk))
            print("* Error :")
            print("* {}".format(str(e)), "\n")
            time.sleep(1)

    if df_OHLCV_by_base_date_and_is_for_failed.size == 0 :

        return (df_OHLCV_by_base_date_and_is_for_failed, failed_list_not_making_error_twice, failed_list_making_error_twice)
    
    else :
    
        df_OHLCV_by_base_date_and_is_for_failed = sqldf("SELECT 기준일자, 야후종목코드, 시가, 고가, 저가, 종가, 수정종가, 거래량 FROM df_OHLCV_by_base_date_and_is_for_failed ORDER BY 기준일자, 야후종목코드")
        return (df_OHLCV_by_base_date_and_is_for_failed, failed_list_not_making_error_twice, failed_list_making_error_twice)