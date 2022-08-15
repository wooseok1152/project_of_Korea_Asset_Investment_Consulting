from make_OHLCV_of_delisting_csv import make_OHLCV_of_delisting_csv
from insert import load_data_infile
from datetime import datetime, timedelta
import logger

logger = logger.get_logger("SEC12T")

today      = datetime.today().strftime("%Y%m%d")
end_date   = datetime.today().strftime("%Y%m%d")
start_date = '20110101'

csv_material_file_path = './csv_for_table_insert_material/batch/batch{}_{}_{}.csv'.format(today, start_date, end_date)

try :

    result_log = make_OHLCV_of_delisting_csv(csv_material_file_path, start_date, end_date)
    if result_log[0] == 0 :   # 지난 7일 동안 상장폐지 된 종목이 없다면, csv파일을 만드는 연산과 테이블에 데이터를 insert하는 연산을 수행하지 않고 해당 프로그램을 종료

        logger.info(result_log[1])
        logger.info("batch for inserting data into SEC12T finished(nothing inserted)")
        logger.info(" ")
    
    else :                    # 지난 7일 동안 상장폐지 된 종목이 있다면, 모든 연산을 수행함
    
        logger.info(result_log[1])

        result_log = load_data_infile(csv_material_file_path)
        logger.info("there are {} data in csv file and {} records are loaded in table".format(result_log[0], result_log[1]))

        logger.info("batch for inserting data into SEC12T finished")
        logger.info(" ")

except Exception as e:

    logger.info("processing this program failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")





