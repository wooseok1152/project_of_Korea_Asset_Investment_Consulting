import pandas as pd
from datetime import datetime, timedelta
from get_df import get_sec01h_df
from get_df import get_sec08h_df
from modify_df import modify_sec01h_df
from modify_df import modify_sec08h_df
from df_to_csv import df_to_csv
from insert import load_data_infile
import logger

logger = logger.get_logger("SEC10H")

today = datetime.today().strftime("%Y%m%d")
csv_material_file_path = './csv_for_table_insert_material/SEC10H_{}.csv'.format(today)

try : 

    df_sec01h = get_sec01h_df(today)
    df_sec08h = get_sec08h_df(today)
    logger.info("getting df_sec01h and df_sec08h finished")

    modified_df_sec01h = modify_sec01h_df(df_sec01h)
    modified_df_sec08h = modify_sec08h_df(df_sec08h)
    logger.info("modifing df_sec01h and df_sec08h finished")

    df_sec10h = pd.concat([modified_df_sec01h, modified_df_sec08h])
    logger.info("making df_sec10h finished")

    result_log = df_to_csv(df_sec10h, csv_material_file_path)
    logger.info(result_log)

    result_log = load_data_infile(csv_material_file_path)
    logger.info("there are {} data in csv file and {} records are loaded in table".format(result_log[0], result_log[1]))

    logger.info("batch for inserting data into SEC10H finished")
    logger.info(" ")

except Exception as e:

    logger.info("processing this batch failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")