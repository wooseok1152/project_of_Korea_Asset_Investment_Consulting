def get_usa_stock_info():

    import numpy as np
    import pandas as pd
    import pymysql
  
    sec_db = pymysql.connect(user = "sec01", password = "sec01", host = '211.170.143.158', port = 13306, db='sec')
    cursor = sec_db.cursor()

    cursor.execute("""
                        SELECT YAHOO_IS_CD,
                               IS_NM_ENG
                        FROM   SEC30H
                        WHERE  BASE_DATE = (SELECT MAX(BASE_DATE) FROM SEC30H)
                   """)
    
    row = cursor.fetchall()
    
    colname = cursor.description
    col = []
    for i in colname :
        
        col.append(i[0])
    
    df_of_target_issue_basic_info = pd.DataFrame(row, columns=col)

    cursor.execute("""  
     
        SELECT  Z.BASE_DATE,
                Z.YAHOO_IS_CD,
                Z.MKT_DIV,
                Z.IS_NM_ENG,
                Z.ADJ_CLS_PRC
        FROM (
            SELECT  Y.BASE_DATE,
                    X.YAHOO_IS_CD, 
                    X.MKT_DIV,
                    X.IS_NM_ENG,
                    Y.ADJ_CLS_PRC,
                    ROW_NUMBER() OVER(PARTITION BY Y.BASE_DATE, X.YAHOO_IS_CD) AS ROWNUMBER
            FROM SEC30H X 
            LEFT JOIN SEC31T Y
            ON   X.YAHOO_IS_CD = Y.YAHOO_IS_CD
            WHERE X.BASE_DATE = (SELECT MAX(BASE_DATE) FROM SEC30H)
                  AND Y.BASE_DATE >= DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 YEAR),'%Y%m%d')
        ) Z
        WHERE Z.ROWNUMBER = 1  
      
                   """)
    
    row2 = cursor.fetchall()
    
    colname2 = cursor.description
    col2 = []
    for i in colname2 :
        
        col2.append(i[0])
    
    df_of_price_info = pd.DataFrame(row2, columns=col2)
    
    usa_price = df_of_price_info.pivot(index='BASE_DATE', columns='YAHOO_IS_CD', values='ADJ_CLS_PRC')
    usa_returns = usa_price.pct_change()
    
    return (df_of_target_issue_basic_info, usa_returns)