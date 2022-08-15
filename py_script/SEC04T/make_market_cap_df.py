import time
from pykrx import stock
import pandas as pd

def make_market_cap_df(index : int, base_date : str) :
    
    try : # KRX에 특정 영업일에 대한 데이터가 아직 존재하지 않으면(장이 열리기 전에는 해당 영업일에 대한 데이터가 존재하지 않음), 해당 영업일에 대해 에러를 발생시킴
          # 토요일 새벽에 배치 프로그램을 실행시키면, 해당 오류가 발생할 가능성이 없음
        
        print("* {} start. Number is {}".format(base_date, index))
        
        start = time.time()

        df_one_day_market_cap_in_KOSDAQ = stock.get_market_cap(base_date, market = 'KOSDAQ')
        time.sleep(1)
        df_one_day_market_cap_in_KOSPI = stock.get_market_cap(base_date, market = 'KOSPI')
        time.sleep(0.5)
        df_one_day_market_cap = pd.concat([df_one_day_market_cap_in_KOSDAQ, df_one_day_market_cap_in_KOSPI]).reset_index()

        df_one_day_market_cap.rename(columns = {"티커" : "단축코드"}, inplace = True)
        df_one_day_market_cap["기준일자"] = base_date
        df_one_day_market_cap = df_one_day_market_cap.astype({"기준일자" : "str"})
        df_one_day_market_cap["기준일자"] = df_one_day_market_cap["기준일자"].str.replace("-", "")
        df_one_day_market_cap = df_one_day_market_cap.loc[:, ["기준일자", "단축코드", "시가총액", "거래량", "거래대금", "상장주식수"]]
        df_one_day_market_cap["단축코드"] = 'A' + df_one_day_market_cap["단축코드"]

        print("* {} end. It takes {}sec".format(base_date, time.time() - start), "\n")

        return df_one_day_market_cap

    except Exception as e :

        print("getting {} data makes error".format(base_date))
        print("Error :")
        print(str(e))
        
        return
