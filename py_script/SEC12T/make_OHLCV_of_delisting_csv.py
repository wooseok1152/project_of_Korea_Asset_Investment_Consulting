import time
from pykrx import stock
import pandas as pd
from pandasql import sqldf
import pymysql

def make_OHLCV_of_delisting_csv(csv_material_file_path : str, start_date : str, end_date : str) :
    
    pymysql.install_as_MySQLdb()

    sec_db = pymysql.connect(user = "root", password = "@realdata1!", host = '211.170.143.158', port = 13306, local_infile = True, autocommit = True)
    cursor = sec_db.cursor()
    cursor.execute(""" 

                    SELECT   X.SHRT_IS_CD,
                             X.IS_NM_SHRT_KR,
                             X.MKT_DIV,
                             X.DELISTING_DATE
                    FROM    SEC.SEC10H X
                    WHERE   X.IS_LSTD = '0'
                            AND X.BASE_DATE = (SELECT MAX(BASE_DATE) FROM SEC.SEC10H)
                            AND X.DELISTING_DATE >= '20120101'
                            AND (X.DELISTING_DATE >= DATE_FORMAT(DATE_ADD((SELECT MAX(BASE_DATE) FROM SEC.SEC10H), INTERVAL -7 DAY), '%Y%m%d') AND X.DELISTING_DATE <= (SELECT MAX(BASE_DATE) FROM SEC.SEC10H))
                            AND X.STK_KND = '보통주'
                            AND X.IS_NM_SHRT_KR NOT LIKE '%스팩%'
                            AND X.DELISTING_RESN NOT REGEXP('완전자회사|신청|유가증권시장|증권거래소|피흡수|자진등록취소|이전상장')
                            AND X.SEQ_NO = 1;
    
                   """)
    print("* run completed", "\n")

    row = cursor.fetchall()
    print("* fetch completed", "\n")

    colname = cursor.description
    col = []
    for i in colname :
        
        col.append(i[0])

    df_delisting = pd.DataFrame(row, columns=col)
    print("* making df_delisting finished", "\n")
    sec_db.close()

    if df_delisting.size == 0: # 지난 7일 동안 상장폐지 된 종목이 없을 때, 데이터 셋의 size는 '0'임

        existence_flag = 0
        return (existence_flag, "there is no delisting issue")
    
    else :

        existence_flag = 1
        
        stock_code_list = list(set([stk[1:] for stk in df_delisting['SHRT_IS_CD'].values.tolist()])) # stock_code_list : SEC10H에서 조회한 상장폐지 종목 리스트('단축속성코드'제거 로직 적용, 혹시 모를 중복된 '단축코드'값 제거 로직 적용)
        print("* stock_code_list length :", len(stock_code_list), "\n")

        df_OHLCV_of_delisting_by_base_date_and_is = pd.DataFrame()
        for i, stk in enumerate(stock_code_list) :

            start = time.time()

            print("\n" + "* {} start. Number is {}".format(stk, i))
            df_one_stock_by_base_date = stock.get_market_ohlcv_by_date(fromdate = start_date, todate = end_date, ticker = stk).reset_index()
            if df_one_stock_by_base_date.size == 0:

                print("* {} finished. It dosen't have any OHLCV. It takes {}sec".format(stk, time.time() - start), "\n")
                time.sleep(1)
                continue

            df_one_stock_by_base_date.rename(columns = {"날짜" : "기준일자"}, inplace = True)
            df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"기준일자" : "str"})
            df_one_stock_by_base_date["기준일자"] = df_one_stock_by_base_date["기준일자"].str.replace("-", "")
            df_one_stock_by_base_date['단축코드'] = stk
            df_one_stock_by_base_date = df_one_stock_by_base_date.astype({"단축코드" : "str"})
            df_one_stock_by_base_date["단축코드"] = "A" + df_one_stock_by_base_date["단축코드"]

            df_one_stock_by_base_date = df_one_stock_by_base_date.loc[:, ['기준일자', '단축코드', '시가', '고가', '저가', '종가', '거래량']]
            df_OHLCV_of_delisting_by_base_date_and_is = pd.concat([df_OHLCV_of_delisting_by_base_date_and_is, df_one_stock_by_base_date])

            print("* {} finished. It takes {}sec".format(stk, time.time() - start), "\n")
            time.sleep(1)

        df_OHLCV_of_delisting_by_base_date_and_is = sqldf("SELECT 기준일자, 단축코드, 시가, 고가, 저가, 종가, 거래량 FROM df_OHLCV_of_delisting_by_base_date_and_is ORDER BY 기준일자, 단축코드")
        df_OHLCV_of_delisting_by_base_date_and_is.to_csv(csv_material_file_path, index = None, encoding="utf-8", na_rep = '\\N')

        return (existence_flag, "making csv material file finished")