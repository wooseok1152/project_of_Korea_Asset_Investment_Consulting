def get_domestic_stock_info():

    import pandas as pd
    import pymysql

    sec_db = pymysql.connect(user = "sec01", password = "sec01", host = '211.170.143.158', port = 13306, db='sec')
    
    cursor = sec_db.cursor()

    cursor.execute("""
                        SELECT SHRT_IS_CD,
                               IS_NM_SHRT_KR
                        FROM   SEC10H
                        WHERE  BASE_DATE = (SELECT MAX(BASE_DATE) FROM SEC10H)
                               AND IS_LSTD = '1'
                   """)
    
    row = cursor.fetchall()
    
    colname = cursor.description
    col = []
    for i in colname :
        
        col.append(i[0])
    
    df_of_target_issue_basic_info = pd.DataFrame(row, columns=col)

    cursor.execute("""  
                        SELECT  Z.BASE_DATE,
                                Z.SHRT_IS_CD,
                                Z.IS_NM_SHRT_KR,
                                Z.CLS_PRC,
                                Z.ONE_YEAR_GNL_RETURN
                        FROM (
                                SELECT  Y.BASE_DATE,
                                        X.SHRT_IS_CD, 
                                        X.IS_NM_SHRT_KR,
                                        Y.CLS_PRC,
                                        (Y.CLS_PRC / LAG(Y.CLS_PRC) OVER(PARTITION BY X.SHRT_IS_CD ORDER BY Y.BASE_DATE)) - 1 AS ONE_YEAR_GNL_RETURN,
                                        MIN(Y.BASE_DATE) OVER(PARTITION BY X.SHRT_IS_CD) AS MIN_BASE_DATE
                                FROM SEC10H X
                                LEFT JOIN SEC03T Y
                                ON   X.SHRT_IS_CD = Y.SHRT_IS_CD
                                WHERE   X.BASE_DATE = (SELECT MAX(BASE_DATE) FROM SEC10H)
                                        AND X.IS_LSTD = '1'
                                        AND Y.BASE_DATE >= DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 YEAR),'%Y%m%d')
                        ) Z;
                   """)
    
    row = cursor.fetchall()
    
    colname = cursor.description
    col = []
    for i in colname :
        
        col.append(i[0])
    
    df_of_price_and_return_info = pd.DataFrame(row, columns=col)
    
    entire_returns = df_of_price_and_return_info.pivot(index='BASE_DATE', columns='SHRT_IS_CD', values='ONE_YEAR_GNL_RETURN')
    
    return (df_of_target_issue_basic_info, entire_returns)