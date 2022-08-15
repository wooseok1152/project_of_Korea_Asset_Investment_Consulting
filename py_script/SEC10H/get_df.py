import pandas as pd

def get_sec01h_df(base_date) :

    return pd.read_csv('../SEC01H/csv_for_table_insert_material/SEC01H_{}.csv'.format(base_date), encoding='utf-8')

def get_sec08h_df(base_date) :

    return pd.read_csv('../SEC08H/csv_for_table_insert_material/SEC08H_{}.csv'.format(base_date), encoding='utf-8')