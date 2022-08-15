import pandas as pd

def df_to_csv(df, csv_material_file_path : str) :
    
    df.to_csv(csv_material_file_path, index = None, encoding="utf-8", na_rep = '\\N')

    return "making material csv file finished"