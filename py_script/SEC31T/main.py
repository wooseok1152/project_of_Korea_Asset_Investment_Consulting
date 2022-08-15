# from make_OHLCV_df_using_fdr import make_OHLCV_df
from make_OHLCV_df_using_yfinance import make_OHLCV_df
from make_OHLCV_df_for_failed_list_using_yfinance import make_OHLCV_df_for_failed_list_using_yfinance
from df_to_csv import df_to_csv
from insert import load_data_infile
from insert_for_failed import load_data_infile_for_failed
from datetime import datetime, timedelta
import pandas as pd
import logger

logger = logger.get_logger("SEC31T")

today      = datetime.today().strftime("%Y%m%d")
end_date   = datetime.today().strftime("%Y%m%d")
start_date = (datetime.today() - timedelta(365)).strftime("%Y%m%d")[:4] + '0101'

csv_material_file_path = './csv_for_table_insert_material/batch/batch_{}_{}_{}.csv'.format(today, start_date, end_date)
csv_material_file_path_for_failed = './csv_for_table_insert_material/batch/batch_{}_{}_{}_failed.csv'.format(today, start_date, end_date)

try :

    # df_OHLCV_by_base_date_and_is, is_making_error = make_OHLCV_df(start_date, end_date) # fdr 모듈을 사용할 때
    df_OHLCV_by_base_date_and_is, failed_list_not_making_error, failed_list_making_error = make_OHLCV_df(start_date) # yfinance 모듈을 사용할 때
    logger.info("making df_OHLCV_by_base_date_and_is finished")
    logger.info("failed list not making error :")
    logger.info(failed_list_not_making_error)
    logger.info("failed list making error :")
    logger.info(failed_list_making_error)

    result_log = df_to_csv(df_OHLCV_by_base_date_and_is, csv_material_file_path)
    logger.info(result_log)

    result_log = load_data_infile(csv_material_file_path)
    logger.info("there are {} data in csv file and {} records are loaded in table".format(result_log[0], result_log[1]))

    logger.info("batch for inserting data into SEC31T finished")
    
    logger.info("start for double checking failed list")
    
    failed_list = failed_list_not_making_error + failed_list_making_error
    df_OHLCV_by_base_date_and_is_for_failed, failed_list_not_making_error_twice, failed_list_making_error_twice = make_OHLCV_df_for_failed_list_using_yfinance(failed_list, start_date)
    logger.info("making df_OHLCV_by_base_date_and_is_for_failed finished")
    logger.info("failed list not making error twice :")
    logger.info(failed_list_not_making_error_twice)
    logger.info("failed list making error twice :")
    logger.info(failed_list_making_error_twice)

    if df_OHLCV_by_base_date_and_is_for_failed.size == 0 :

        logger.info("there is no data in df_OHLCV_by_base_date_and_is_for_failed")
        logger.info(" ")

    else :

        result_log = df_to_csv(df_OHLCV_by_base_date_and_is_for_failed, csv_material_file_path_for_failed)
        logger.info(result_log)

        result_log = load_data_infile_for_failed(csv_material_file_path_for_failed)
        logger.info("there are {} data in csv file and {} records are loaded in table".format(result_log[0], result_log[1]))
        logger.info(" ")

except Exception as e:

    logger.info("processing this batch failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")





