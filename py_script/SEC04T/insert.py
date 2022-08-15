import pymysql
import pandas as pd

def load_data_infile(csv_material_file_path : str, start_date : str, end_date : str) :

    data_cnt_in_csv_material_file = len(pd.read_csv(csv_material_file_path, encoding = 'utf-8'))

    pymysql.install_as_MySQLdb()

    sec_db = pymysql.connect(user = "root", password = "@realdata1!", host = '211.170.143.158', port = 13306, local_infile = True, autocommit = True)
    
    cursor = sec_db.cursor()
    cursor.execute("SET GLOBAL local_infile=1;")
    
    cursor.execute("""DELETE FROM sec.sec04t WHERE base_date >= '{}' and base_date <= '{}';""".format(start_date, end_date))
    result = cursor.execute("""LOAD DATA LOCAL INFILE '{}' INTO TABLE sec.sec04t CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (BASE_DATE,SHRT_IS_CD,MKT_CAP,VOLUME,TRANSAC_AMT,LSTD_IS_CNT);""".format(csv_material_file_path))

    sec_db.close()

    return (data_cnt_in_csv_material_file, result)