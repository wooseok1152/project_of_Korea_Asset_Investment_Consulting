import datetime
import pandas as pd
from kue import kue_cov
import logger

logger = logger.get_logger("makecov")

today = datetime.datetime.today()
nobar_sat = (pd.date_range(end = today, periods = 1, freq = 'W-SAT')[0]).strftime('%Y%m%d')

try : 

    entire_cov_matrix = kue_cov()
    
    cov_file_name = 'entire_cov_matrix_' + str(nobar_sat) + '.csv'
    cov_file_path = './csv_of_cov_matrix/' + str(cov_file_name)
    entire_cov_matrix.to_csv(cov_file_path)

    row_count_of_entire_cov_matrix = len(entire_cov_matrix)
    column_count_of_entire_cov_matrix = len(entire_cov_matrix.columns)

    logger.info("csv of entire cov matrix has been made")
    logger.info("row count : {}".format(row_count_of_entire_cov_matrix))
    logger.info("column count : {}".format(column_count_of_entire_cov_matrix))


except Exception as e :

    logger.info("processing this batch failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")