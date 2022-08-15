from get_bsnss_date import get_bsnss_date
from df_to_csv import df_to_csv
from insert import load_data_infile
from datetime import datetime, timedelta
import pandas as pd
import logger

logger = logger.get_logger("SEC13H")

today      = datetime.today().strftime("%Y%m%d")
end_date   = datetime.today().strftime("%Y%m%d")
start_date = (datetime.today() - timedelta(7)).strftime("%Y%m%d") 

csv_material_file_path = './csv_for_table_insert_material/batch/batch_{}_{}_{}.csv'.format(today, start_date, end_date)

try :

    df_bsnss_date = get_bsnss_date(start_date, end_date)
    logger.info("making df_bsnss_date finished")

    result_log = df_to_csv(df_bsnss_date, csv_material_file_path)
    logger.info(result_log)

    result_log = load_data_infile(csv_material_file_path, start_date, end_date)
    logger.info("there are {} data in csv file and {} records are loaded in table".format(result_log[0], result_log[1]))

    logger.info("batch for inserting data into SEC13H finished")
    logger.info(" ")

except Exception as e:

    logger.info("processing this batch failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")





