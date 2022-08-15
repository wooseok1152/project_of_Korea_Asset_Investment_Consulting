import time
from pykrx import stock
import pandas as pd

def make_exhaustion_rate_df(index : int, base_date : str) :

    try : # KRX에 특정 영업일에 대한 데이터가 아직 존재하지 않으면(장이 열리기 전에는 해당 영업일에 대한 데이터가 존재하지 않음), 해당 영업일에 대해 에러를 발생시킴
          # 토요일 새벽에 배치 프로그램을 실행시키면, 해당 오류가 발생할 가능성이 없음

        print("* {} start. Number is {}".format(base_date, index))
        
        start = time.time()

        df_one_day_exhaustion_rates_in_KOSPI = stock.get_exhaustion_rates_of_foreign_investment(base_date, "KOSPI")
        time.sleep(1)
        df_one_day_exhaustion_rates_in_KOSDAQ = stock.get_exhaustion_rates_of_foreign_investment(base_date, "KOSDAQ")
        time.sleep(1)
        df_one_day_exhaustion_rates = pd.concat([df_one_day_exhaustion_rates_in_KOSDAQ, df_one_day_exhaustion_rates_in_KOSPI]).reset_index()

        df_one_day_exhaustion_rates.rename(columns = {"티커" : "단축코드"}, inplace = True)
        df_one_day_exhaustion_rates["기준일자"] = base_date
        df_one_day_exhaustion_rates = df_one_day_exhaustion_rates.astype({"기준일자" : "str"})
        df_one_day_exhaustion_rates["기준일자"] = df_one_day_exhaustion_rates["기준일자"].str.replace("-", "")
        df_one_day_exhaustion_rates["단축코드"] = 'A' + df_one_day_exhaustion_rates["단축코드"]

        df_one_day_exhaustion_rates = df_one_day_exhaustion_rates.loc[:, ["기준일자", "단축코드", "상장주식수", "보유수량", "지분율", "한도수량", "한도소진률"]]

        print("* {} end. It takes {}sec".format(base_date, time.time() - start), "\n")

        return df_one_day_exhaustion_rates

    except Exception as e :

        print("getting {} data makes error".format(base_date))
        print("Error :")
        print(str(e))
        
        return