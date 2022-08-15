import FinanceDataReader as fdr
import pandas as pd
from pandasql import sqldf
from datetime import date, datetime, timedelta

def df_to_csv(csv_material_file_path : str) :

    today = datetime.today().strftime("%Y%m%d")             # 현재 일자

    df_NYSE = fdr.StockListing('NYSE')
    df_NYSE.rename(columns = {"Symbol" : "네이버종목코드", "Name" : "영문종목명", "Industry" : "산업구분", "IndustryCode" : "산업구분코드"}, inplace = True)
    df_NYSE["기준일자"] = today
    df_NYSE["시장구분"] = 'NYSE'
    df_NYSE = df_NYSE.loc[:, ["기준일자", "네이버종목코드", "시장구분", "영문종목명", "산업구분", "산업구분코드"]]

    df_NASDAQ = fdr.StockListing('NASDAQ')
    df_NASDAQ.rename(columns = {"Symbol" : "네이버종목코드", "Name" : "영문종목명", "Industry" : "산업구분", "IndustryCode" : "산업구분코드"}, inplace = True)
    df_NASDAQ["기준일자"] = today
    df_NASDAQ["시장구분"] = 'NASDAQ'
    df_NASDAQ = df_NASDAQ.loc[:, ["기준일자", "네이버종목코드", "시장구분", "영문종목명", "산업구분", "산업구분코드"]]

    df_AMEX = fdr.StockListing('AMEX')
    df_AMEX.rename(columns = {"Symbol" : "네이버종목코드", "Name" : "영문종목명", "Industry" : "산업구분", "IndustryCode" : "산업구분코드"}, inplace = True)
    df_AMEX["기준일자"] = today
    df_AMEX["시장구분"] = 'AMEX'
    df_AMEX = df_AMEX.loc[:, ["기준일자", "네이버종목코드", "시장구분", "영문종목명", "산업구분", "산업구분코드"]]

    df_US = pd.concat([df_NYSE, df_NASDAQ, df_AMEX])
    
    #  df_target_1 :  '.U'제외, '.*'로 끝나는 레코드의 해당 문자열을 '-*'로 변경
    df_target_1 = sqldf("SELECT 기준일자, REPLACE(네이버종목코드, '.', '-') AS 야후종목코드, 네이버종목코드, 시장구분, 영문종목명, 산업구분, 산업구분코드 FROM df_US WHERE 네이버종목코드 LIKE '%.%' AND 네이버종목코드 NOT LIKE '%.U'")
    #  df_target_2 :  -- '.U'로 끝나는 레코드의 해당 문자열을 '-UN'으로 변경
    df_target_2 = sqldf("SELECT 기준일자, REPLACE(네이버종목코드, '.', '-') || 'N' AS 야후종목코드, 네이버종목코드, 시장구분, 영문종목명, 산업구분, 산업구분코드 FROM df_US WHERE 네이버종목코드 LIKE '%.U'")
    #  df_target_3 : ' PR *'문자열이 들어있는 레코드를 '-P*'로 변경
    df_target_3 = sqldf("SELECT 기준일자, REPLACE(REPLACE(네이버종목코드, ' PR', '-P'), ' ', '') AS 야후종목코드, 네이버종목코드, 시장구분, 영문종목명, 산업구분, 산업구분코드 FROM df_US WHERE 네이버종목코드 LIKE '% PR%'")
    #  df_target_4 : 띄어쓰기나 온점이 들어있지 않는 레코드
    df_target_4 = sqldf("SELECT 기준일자, 네이버종목코드 AS 야후종목코드, 네이버종목코드, 시장구분, 영문종목명, 산업구분, 산업구분코드 FROM df_US WHERE 네이버종목코드 NOT LIKE '%.%' AND 네이버종목코드 NOT LIKE '% %'")
    
    df_US = pd.concat([df_target_1, df_target_2, df_target_3, df_target_4]).loc[:, ["기준일자", "야후종목코드", "시장구분", "네이버종목코드", "영문종목명", "산업구분", "산업구분코드"]]
    
    df_US.to_csv(csv_material_file_path, index = None, encoding="utf-8", na_rep = '\\N')

    return "making a csv file finished"  

