import time
from pykrx import stock
import pandas as pd

def make_index_OHLCV_df(start_date : str, end_date : str) :

    try : # KRX에 특정 영업일에 대한 데이터가 아직 존재하지 않으면(장이 열리기 전에는 해당 영업일에 대한 데이터가 존재하지 않음), 해당 영업일에 대해 에러를 발생시킴
          # 토요일 새벽에 배치 프로그램을 실행시키면, 해당 오류가 발생할 가능성이 없음
        
        start = time.time()
        
        df_OHLCV_in_KOSPI_by_base_date = stock.get_index_ohlcv(start_date, end_date, "1001")
        df_OHLCV_in_KOSPI_by_base_date['시장구분'] = 'KOSPI'
        
        df_OHLCV_in_KOSDAQ_by_base_date = stock.get_index_ohlcv(start_date, end_date, "2001")
        df_OHLCV_in_KOSDAQ_by_base_date['시장구분'] = 'KOSDAQ'
        
        df_OHLCV_by_base_date_and_mkt = pd.concat([df_OHLCV_in_KOSPI_by_base_date, df_OHLCV_in_KOSDAQ_by_base_date]).reset_index()
        df_OHLCV_by_base_date_and_mkt = df_OHLCV_by_base_date_and_mkt[['날짜', '시장구분', '시가', '고가', '저가', '종가', '거래량']]
        df_OHLCV_by_base_date_and_mkt = df_OHLCV_by_base_date_and_mkt.astype({"날짜" : "str"})
        df_OHLCV_by_base_date_and_mkt["날짜"] = df_OHLCV_by_base_date_and_mkt["날짜"].str.replace("-", "")

        print("* It takes {}sec".format(time.time()-start), "\n")

        return df_OHLCV_by_base_date_and_mkt

    except Exception as e :

        print("making df_OHLCV_by_base_date_and_mkt makes error")
        print("Error :")
        print(str(e))
        
        return