import pandas as pd
from pandasql import sqldf

def modify_sec01h_df(df : pd.DataFrame) :
    
    df.rename(columns = {"한글 종목명" : "한글종목명", "한글 종목약명" : "한글종목약명", "영문 종목명" : "영문종목명"}, inplace = True)
    df = sqldf("SELECT 기준일자, 단축코드, ROW_NUMBER() OVER(PARTITION BY 기준일자, 단축코드) AS 회차번호, 표준코드, 한글종목명, 한글종목약명, 영문종목명, 상장일, 시장구분, 증권구분, 소속부, 주식종류, 액면가, 상장주식수, NULL AS 상장폐지일, NULL AS 폐지사유, 1 AS 상장여부 FROM df WHERE 시장구분 != 'KONEX'")

    return df

def modify_sec08h_df(df : pd.DataFrame) :
    
    df = sqldf("SELECT 기준일자, 단축코드, 회차번호, NULL AS 표준코드, NULL AS 한글종목명, 한글종목약명, NULL AS 영문종목명, 상장일, 시장구분, 증권구분, NULL AS 소속부, 주식종류, NULL AS 액면가, NULL AS 상장주식수, 상장폐지일, 폐지사유, 0 AS 상장여부 FROM df WHERE LENGTH(단축코드) = 7 AND 단축코드 LIKE 'A%' AND 상장폐지일 >= '20110101' AND 시장구분 != 'KONEX'")

    return df