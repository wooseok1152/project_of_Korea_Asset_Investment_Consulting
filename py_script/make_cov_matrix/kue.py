import pandas as pd
from domestic_stock import get_domestic_stock_info
from usa_stock import get_usa_stock_info
from domestic_etf import get_domestic_etf_info

def kue_cov():

    
    kor_returns = get_domestic_stock_info()[1]
    usa_returns = get_usa_stock_info()[1]
    etf_returns = get_domestic_etf_info()[1]

    kue_returns = pd.concat([kor_returns, usa_returns, etf_returns], axis=1)
    kue_cov = kue_returns.astype(float).cov()
    
    return kue_cov