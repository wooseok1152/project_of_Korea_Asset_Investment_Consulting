import pandas as pd

def df_to_csv(df : pd.DataFrame, csv_material_file_path : str) :

    df.to_csv(csv_material_file_path, index = None, encoding="utf-8", na_rep = '\\N')
    
    return "making a csv file finished"