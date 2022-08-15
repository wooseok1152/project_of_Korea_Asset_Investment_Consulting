import time
from pykrx import stock
import pandas as pd
from pandasql import sqldf

def make_market_trading_value_and_volume_df(index : int, base_date : str) :

    try : # KRX에 특정 영업일에 대한 데이터가 아직 존재하지 않으면(장이 열리기 전에는 해당 영업일에 대한 데이터가 존재하지 않음), 해당 영업일에 대해 에러를 발생시킴
        # 토요일 새벽에 배치 프로그램을 실행시키면, 해당 오류가 발생할 가능성이 없음

        print("* {} start. Number is {}".format(base_date, index))
        
        start = time.time()

        investor_list = ["개인", "기관합계", "외국인", "기타외국인", "기타법인", "금융투자", "보험", "투신", "사모", "은행", "기타금융", "연기금", "전체"]
        df_one_day_market_trading_value_and_volume_by_investor = pd.DataFrame()

        for i, investor in enumerate(investor_list) :
        
            df_market_trading_value_and_volume_in_KOSDDQ = stock.get_market_net_purchases_of_equities(base_date, base_date, "KOSDAQ", investor)
            df_market_trading_value_and_volume_in_KOSPI = stock.get_market_net_purchases_of_equities(base_date, base_date, "KOSPI", investor)
            df_market_trading_value_and_volume = pd.concat([df_market_trading_value_and_volume_in_KOSDDQ, df_market_trading_value_and_volume_in_KOSPI]).reset_index()

            df_market_trading_value_and_volume.rename(columns = {"티커" : "단축코드"}, inplace = True)
            df_market_trading_value_and_volume["투자자코드"] = str(i+1)
            df_market_trading_value_and_volume["기준일자"] = base_date
            df_market_trading_value_and_volume = df_market_trading_value_and_volume.astype({"기준일자" : "str"})
            df_market_trading_value_and_volume["기준일자"] = df_market_trading_value_and_volume["기준일자"].str.replace("-", "")
            df_market_trading_value_and_volume["단축코드"] = "A" + df_market_trading_value_and_volume["단축코드"]

            df_market_trading_value_and_volume = df_market_trading_value_and_volume.loc[:, ["기준일자", "단축코드", "투자자코드", "매도거래량", "매수거래량", "순매수거래량", "매도거래대금", "매수거래대금", "순매수거래대금"]]

            df_one_day_market_trading_value_and_volume_by_investor = pd.concat([df_one_day_market_trading_value_and_volume_by_investor, df_market_trading_value_and_volume])

        df_one_day_market_trading_value_and_volume_by_investor = sqldf("SELECT * FROM df_one_day_market_trading_value_and_volume_by_investor ORDER BY 기준일자, 단축코드, 투자자코드")

        print("* {} end. It takes {}sec".format(base_date, time.time() - start), "\n")

        return df_one_day_market_trading_value_and_volume_by_investor
        
    except Exception as e :

        print("getting {} data makes error".format(base_date))
        print("Error :")
        print(str(e))
        
        return        
