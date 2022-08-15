from datetime import datetime, timedelta
import exchange_calendars as ecals
import pandas as pd 

def get_bsnss_date(start : str, end : str):        # 범위 내 평일에 해당하는 일자만 조회한 후, 해당 일자를 요소로 가지는 list 반환

    XKRX = ecals.get_calendar("XKRX") # 한국 코드 
    
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    bsnss_dates = [j[0].strftime("%Y%m%d") for j in [((start + timedelta(days=i)), (start + timedelta(days=i)).weekday()) for i in range((end-start).days+1)] if j[1] <= 4 and XKRX.is_session(j[0])]
    df_bsnss_dates = pd.DataFrame({"영업일자" : bsnss_dates})

    return df_bsnss_dates