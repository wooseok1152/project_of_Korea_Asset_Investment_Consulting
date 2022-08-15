from domestic_issue_download import listing_stock_download
from csv_to_df import load_is_dataset
from csv_to_df import pre_process_df
from insert import load_data_infile
from df_to_csv import df_to_csv
import logger
import time

logger = logger.get_logger("SEC01H")

csv_material_file_path = './csv_for_table_insert_material/SEC01H_{}.csv'.format(time.strftime("%Y%m%d"))

try : 

    result_log = listing_stock_download(r"D:\20.share\BHRC\py_script\py\SEC01H\crawling\downloads")
    # result_log = listing_stock_download(r"D:\20.share\한국자산투자컨설팅\50_Git\investing_property_index\py_script\py\SEC01H\crawling\downloads")
    logger.info(result_log)

    df, path_of_recent_csv_file_downloaded_from_krx_webpage = load_is_dataset("./crawling/downloads/")
    logger.info("path of recent csv file downloaded from krx webpage : " + path_of_recent_csv_file_downloaded_from_krx_webpage)

    df_domestic_is_basic_info = pre_process_df(df)
    result_log = df_to_csv(df_domestic_is_basic_info, csv_material_file_path)
    logger.info(result_log)

    result_log = load_data_infile("./csv_for_table_insert_material/")
    logger.info("there are {} data in csv file and {} records are loaded in table".format(result_log[0], result_log[1]))
    logger.info("batch for inserting data into SEC01H finished")
    logger.info(" ")

except Exception as e :

    logger.info("processing this batch failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")
