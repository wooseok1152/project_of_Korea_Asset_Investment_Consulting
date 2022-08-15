def get_domestic_etf_info():
    
    import numpy as np
    import pandas as pd
    import pymysql
    
    sec_db = pymysql.connect(user = "sec01", password = "sec01", host = '211.170.143.158', port = 13306, db='sec')
    cursor = sec_db.cursor()

    cursor.execute("""
                    SELECT SHRT_IS_CD,
                           IS_NM_KR
                    FROM   SEC50H
                    WHERE  BASE_DATE = (SELECT MAX(BASE_DATE) FROM SEC50H)
                """)
    
    row = cursor.fetchall()
    
    colname = cursor.description
    col = []
    for i in colname :
        
        col.append(i[0])
    
    df_of_target_issue_basic_info = pd.DataFrame(row, columns=col)
    
    cursor.execute("""  
                        SELECT Y.CLS_PRC, 
                               Y.BASE_DATE, 
                               X.SHRT_IS_CD, 
                               X.IS_NM_KR
                        FROM SEC50H X 
                        LEFT JOIN SEC51T Y
                        ON    X.SHRT_IS_CD = Y.SHRT_IS_CD
                        WHERE X.BASE_DATE = (SELECT MAX(BASE_DATE) FROM SEC50H)
                              AND Y.BASE_DATE >= DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 YEAR),'%Y%m%d')
                   """)
    
    row3 = cursor.fetchall()
    
    colname3 = cursor.description
    col3 = []
    for i in colname3 :
        
        col3.append(i[0])
    
    df_of_price_info = pd.DataFrame(row3, columns=col3)
    
    etf_price = df_of_price_info.pivot(index='BASE_DATE', columns='SHRT_IS_CD', values='CLS_PRC')
    etf_returns = etf_price.pct_change()
    
    return (df_of_target_issue_basic_info, etf_returns)