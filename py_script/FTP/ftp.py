import ftplib 
import datetime
from dateutil.relativedelta import relativedelta
import logger

logger = logger.get_logger("ftp")

def find_sat_day():
    start_day = datetime.datetime.now().date()
    while start_day.weekday() != 5:
        start_day = start_day - relativedelta(days=1)
    
    # date -> datetime 으로 변환
    start_day = datetime.datetime.combine(start_day, datetime.datetime.min.time())
    
    return start_day

std_date = find_sat_day()
std_date = std_date - relativedelta(days=1)
std_date = str(std_date.date())
std_date = std_date.replace('-', '')

try:
    
    ip = ""
    ftp = ftplib.FTP()
    ftp.encoding = 'utf-8'
    ftp.set_pasv(False)
    ftp.connect(host=ip, port=21)   # 두 번째 인자는 port number
    ftp.login(user="", passwd="")   # FTP 서버에 접속 

    filename = f'result_KOSPI_{std_date}.csv'

    myfile = open(f'./csv_to_send/result_KOSPI_{std_date}.csv', 'rb')                         # binary = rb, ASCII = r
    ftp.storbinary('STOR ' + filename, myfile)
    myfile.close()  

    filename = f'result_KOSDAQ_{std_date}.csv'
    myfile = open(f'./csv_to_send/result_KOSDAQ_{std_date}.csv', 'rb')                         # binary = rb, ASCII = r

    ftp.storbinary('STOR ' + filename, myfile)

    myfile.close()

    ftp.quit()
    
    logger.info("processing this ftp batch succeeded")

except Exception as e :

    logger.info("processing this ftp batch failed")
    logger.info("Error :")
    logger.info(str(e))
    logger.info(" ")