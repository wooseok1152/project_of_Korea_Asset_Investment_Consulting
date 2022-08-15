import time
from pykrx import stock
import pandas as pd

def make_shorting_balance_df(index : int, base_date : str) :

    print("* {} start. Number is {}".format(base_date, index))
    
    start = time.time()

    try :  # 배치 프로그램 시작 일자 기준, 2전 영업일까지의 공매도 데이터는 pykrx에 준비되지 않음

        df_one_day_shorting_balance_in_KOSPI = stock.get_shorting_balance_by_ticker(base_date, market = 'KOSPI')
        time.sleep(1)
        df_one_day_shorting_balance_in_KOSDAQ = stock.get_shorting_balance_by_ticker(base_date, "KOSDAQ")
        time.sleep(0.5)

        df_one_day_shorting_balance = pd.concat([df_one_day_shorting_balance_in_KOSPI, df_one_day_shorting_balance_in_KOSDAQ]).reset_index()

        df_one_day_shorting_balance.rename(columns = {"티커" : "단축코드"}, inplace = True)
        df_one_day_shorting_balance["기준일자"] = base_date
        df_one_day_shorting_balance = df_one_day_shorting_balance.astype({"기준일자" : "str"})
        df_one_day_shorting_balance["기준일자"] = df_one_day_shorting_balance["기준일자"].str.replace("-", "")
        df_one_day_shorting_balance = df_one_day_shorting_balance.loc[:, ["기준일자", "단축코드", "공매도잔고", "상장주식수", "공매도금액", "시가총액", "비중"]]
        df_one_day_shorting_balance["단축코드"] = "A" + df_one_day_shorting_balance["단축코드"]

        print("* {} end. It takes {}sec".format(base_date, time.time() - start), "\n")

        return df_one_day_shorting_balance
    
    except Exception as e :

        print("* {} data is not ready in KRX website. It takes {}sec".format(base_date, time.time() - start))
        print("* Error :")
        print("* {}".format(str(e)), "\n")

        return

