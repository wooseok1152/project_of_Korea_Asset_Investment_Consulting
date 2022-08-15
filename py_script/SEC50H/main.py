from datetime import datetime
from insert import load_data_infile
from df_to_csv import df_to_csv
import logger

logger = logger.get_logger("SEC50H")

try : 

    today = datetime.today().strftime("%Y%m%d")
    csv_material_file_path = './csv_for_table_insert_material/SEC50H_{}.csv'.format(today)
    csv_material_directory_path = './csv_for_table_insert_material/'

    result_log = df_to_csv(csv_material_file_path)
    logger.info(result_log)

    result_log = load_data_infile(csv_material_directory_path)
    logger.info("there are {} data in csv file and {} records are loaded in table".format(result_log[0], result_log[1]))
    logger.info("batch for inserting data into SEC50H finished")
    logger.info(" ")

except Exception as e :

    logger.info("processing this batch failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")