import FinanceDataReader as fdr
import pandas as pd
from pandasql import sqldf
from datetime import date, datetime, timedelta

def df_to_csv(csv_material_file_path : str) :

    df_delisted_is = fdr.StockListing('KRX-DELISTING')
    df_delisted_is = df_delisted_is.astype({"ListingDate" : "str", "DelistingDate" : "str"})
    df_delisted_is["ListingDate"] = df_delisted_is["ListingDate"].str.replace("-", "")
    df_delisted_is["DelistingDate"] = df_delisted_is["DelistingDate"].str.replace("-", "")
    df_delisted_is["기준일자"] = datetime.today().strftime("%Y%m%d")

    df_delisted_is.rename(columns = {"Symbol" : "단축코드", "Name" : "한글종목약명", "Market" : "시장구분", "SecuGroup" : "증권구분", "Kind" : "주식종류", "ListingDate" : "상장일", "DelistingDate" : "상장폐지일", "Reason" : "폐지사유"}, inplace = True)
    df_delisted_is = df_delisted_is.loc[:, ["기준일자", "단축코드", "한글종목약명", "시장구분", "증권구분", "주식종류", "상장일", "상장폐지일", "폐지사유"]] 
   
    df_delisted_is = sqldf("SELECT 기준일자, CASE WHEN 증권구분 IN ('신주인수권증권', '신주인수권증서') THEN 'J' || 단축코드 WHEN 증권구분 = '수익증권' THEN 'F' || 단축코드 ELSE 'A' || 단축코드 END AS 단축코드, 한글종목약명, 시장구분, 증권구분, 주식종류, 상장일, 상장폐지일, 폐지사유 FROM df_delisted_is")
    df_delisted_is = sqldf("SELECT 기준일자, 단축코드, ROW_NUMBER() OVER(PARTITION BY 기준일자, 단축코드) AS 회차번호, 한글종목약명, 시장구분, 증권구분, 주식종류, 상장일, 상장폐지일, 폐지사유 FROM df_delisted_is")
    
    df_delisted_is.to_csv(csv_material_file_path, index = None, encoding="utf-8", na_rep = '\\N')

    return "making a csv file finished"  




