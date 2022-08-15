import time
from pykrx import stock
import pandas as pd
from pandasql import sqldf
from datetime import datetime, timedelta

def make_OHLCV_df(start_date : str, end_date : str) :

    today = datetime.today().strftime("%Y%m%d")

    # stock_code_list : SEC10H에 존재하는 종목 리스트('단축속성코드'제거 로직 적용, 중복된 '단축코드'값 제거 로직 적용)
    stock_code_list = list(set([stk[1:] for stk in pd.read_csv('../SEC10H/csv_for_table_insert_material/SEC10H_{}.csv'.format(today), encoding='utf-8')['단축코드'].values.tolist()])) 
    print("* stock_code_list length :", len(stock_code_list))

    df_OHLCV_by_base_date_and_is = pd.DataFrame()
    
    for i, stk in enumerate(stock_code_list) :

        start = time.time()

        print("\n" + "* {} start. Number is {}".format(stk, i))
        df_one_stock_by_base_date = stock.get_market_ohlcv_by_date(fromdate = start_date, todate = end_date, ticker = stk).reset_index()
        
        if df_one_stock_by_base_date.size == 0: # 아무런 데이터를 수신받지 않았을 때, 데이터 셋의 size는 '0'임

            print("* {} finished. It dosen't have any OHLCV. It takes {}sec".format(stk, time.time() - start), "\n")
            time.sleep(1)
            continue

        df_one_stock_by_base_date.rename(columns = {"날짜" : "기준일자"}, inplace = True)
        df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"기준일자" : "str"})
        df_one_stock_by_base_date["기준일자"] = df_one_stock_by_base_date["기준일자"].str.replace("-", "")
        df_one_stock_by_base_date['단축코드'] = stk
        df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"단축코드" : "str"})
        df_one_stock_by_base_date["단축코드"] = "A" + df_one_stock_by_base_date["단축코드"]
        
        df_one_stock_by_base_date = df_one_stock_by_base_date.loc[:, ['기준일자', '단축코드', '시가', '고가', '저가', '종가', '거래량']]
        df_OHLCV_by_base_date_and_is = pd.concat([df_OHLCV_by_base_date_and_is, df_one_stock_by_base_date])

        print("* {} finished. It takes {}sec".format(stk, time.time() - start), "\n")
        time.sleep(1)

    df_OHLCV_by_base_date_and_is = sqldf("SELECT 기준일자, 단축코드, 시가, 고가, 저가, 종가, 거래량 FROM df_OHLCV_by_base_date_and_is ORDER BY 기준일자, 단축코드")
    
    return df_OHLCV_by_base_date_and_is