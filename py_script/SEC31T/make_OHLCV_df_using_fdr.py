import time
import pandas as pd
from pandasql import sqldf
from datetime import datetime, timedelta
import FinanceDataReader as fdr

def make_OHLCV_df(start_date : str, end_date : str) :

    today = datetime.today().strftime("%Y%m%d")

    # stock_code_list : SEC30H에 존재하는 종목 리스트(중복된 '종목코드'값 제거 로직 적용)
    stock_code_list = list(set(pd.read_csv('../SEC30H/csv_for_table_insert_material/SEC30H_{}.csv'.format(today), encoding='utf-8')['종목코드'].values.tolist()))
    print("* stock_code_list length :", len(stock_code_list))

    df_OHLCV_by_base_date_and_is = pd.DataFrame()
    is_making_error = []

    for i, stk in enumerate(stock_code_list) :

        try : 

            start = time.time()

            print("\n" + "* {} start. Number is {}".format(stk, i))
            df_one_stock_by_base_date= fdr.DataReader(stk, start_date[:4] + '-' + start_date[4:6] + '-' + start_date[6:], end_date[:4] + '-' + end_date[4:6] + '-' + end_date[6:]).reset_index()
            
            if df_one_stock_by_base_date.size == 0:

                print("* {} finished. It dosen't have any OHLCV. It takes {}sec".format(stk, time.time() - start), "\n")
                time.sleep(1)
                continue

            df_one_stock_by_base_date.rename(columns = {"Date" : "기준일자", "Close" : "종가", "Open" : "시가", "High" : "고가", "Low" : "저가", "Volume" : "거래량", "Change" : "등락률"}, inplace = True)
            df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"기준일자" : "str"})
            df_one_stock_by_base_date["기준일자"] = df_one_stock_by_base_date["기준일자"].str.replace("-", "")
            df_one_stock_by_base_date["종목코드"] = stk
            df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"거래량" : "int"})
            
            df_one_stock_by_base_date = df_one_stock_by_base_date.loc[:, ['기준일자', '종목코드', '시가', '고가', '저가', '종가', '거래량', '등락률']]
            df_OHLCV_by_base_date_and_is = pd.concat([df_OHLCV_by_base_date_and_is, df_one_stock_by_base_date])

            print("* {} finished. It takes {}sec".format(stk, time.time() - start), "\n")
            time.sleep(1)
        
        except Exception as e :

            is_making_error.append(stk)
            print("* {} makes error.")
            print("* Error :")
            print("* {}".format(str(e)), "\n")

    df_OHLCV_by_base_date_and_is = sqldf("SELECT 기준일자, 종목코드, 시가, 고가, 저가, 종가, 거래량, 등락률 FROM df_OHLCV_by_base_date_and_is ORDER BY 기준일자, 종목코드")

    return (df_OHLCV_by_base_date_and_is, is_making_error)