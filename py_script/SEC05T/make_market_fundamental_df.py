import time
from pykrx import stock
import pandas as pd

def make_market_fundamental_df(index : int, base_date : str) :
    
    try : # KRX에 특정 영업일에 대한 데이터가 아직 존재하지 않으면(장이 열리기 전에는 해당 영업일에 대한 데이터가 존재하지 않음), 해당 영업일에 대해 에러를 발생시킴
          # 토요일 새벽에 배치 프로그램을 실행시키면, 해당 오류가 발생할 가능성이 없음
        
        print("* {} start. Number is {}".format(base_date, index))
        
        start = time.time()

        df_one_day_market_fundamental_in_KOSDAQ = stock.get_market_fundamental(base_date, market = 'KOSDAQ')
        time.sleep(1)
        df_one_day_market_fundamental_in_KOSPI = stock.get_market_fundamental(base_date, market = 'KOSPI')
        time.sleep(0.5)
        df_one_day_market_fundamental = pd.concat([df_one_day_market_fundamental_in_KOSDAQ, df_one_day_market_fundamental_in_KOSPI]).reset_index()

        df_one_day_market_fundamental.rename(columns = {"티커" : "단축코드", "DIV" : "DIV_"}, inplace = True)
        df_one_day_market_fundamental["기준일자"] = base_date
        df_one_day_market_fundamental = df_one_day_market_fundamental.astype({"기준일자" : "str"})
        df_one_day_market_fundamental["기준일자"] = df_one_day_market_fundamental["기준일자"].str.replace("-", "")
        df_one_day_market_fundamental = df_one_day_market_fundamental.loc[:, ["기준일자", "단축코드", "BPS", "PER", "PBR", "EPS", "DIV_", "DPS"]]
        df_one_day_market_fundamental["단축코드"] = "A" + df_one_day_market_fundamental["단축코드"]

        print("* {} end. It takes {}sec".format(base_date, time.time() - start), "\n")

        return df_one_day_market_fundamental

    except Exception as e :

        print("getting {} data makes error".format(base_date))
        print("Error :")
        print(str(e))
        
        return
