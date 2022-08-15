import time
from pykrx import stock
import pandas as pd
from pandasql import sqldf
from datetime import datetime, timedelta
from get_weekday import date_range

def make_etf_OHLCV_df(index : int, base_date : str) :

    try : # KRX에 특정 영업일에 대한 데이터가 아직 존재하지 않으면(장이 열리기 전에는 해당 영업일에 대한 데이터가 존재하지 않음), 해당 영업일에 대해 에러를 발생시킴
          # 토요일 새벽에 배치 프로그램을 실행시키면, 해당 오류가 발생할 가능성이 없음

        print("* {} start. Number is {}".format(base_date, index))
        
        start = time.time()

        df_one_day_etf_OHLCV = stock.get_etf_ohlcv_by_ticker(base_date).reset_index()
        time.sleep(1)

        df_one_day_etf_OHLCV["기준일자"] = base_date
        df_one_day_etf_OHLCV.rename(columns = {"티커" : "단축코드"}, inplace = True)
        df_one_day_etf_OHLCV = df_one_day_etf_OHLCV.astype({"단축코드" : "str"})
        df_one_day_etf_OHLCV["단축코드"] = "A" + df_one_day_etf_OHLCV["단축코드"]
        df_one_day_etf_OHLCV = df_one_day_etf_OHLCV.loc[:, ["기준일자", "단축코드", "시가", "고가", "저가", "종가", "NAV", "거래량", "거래대금", "기초지수"]]

        print("* {} end. It takes {}sec".format(base_date, time.time() - start), "\n")

        return df_one_day_etf_OHLCV

    except Exception as e:

        print("getting {} data makes error".format(base_date))
        print("Error :")
        print(str(e))
    
        return