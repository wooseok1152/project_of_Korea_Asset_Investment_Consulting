import pymysql
import pandas as pd

def load_data_infile(csv_material_file_path : str) :

    data_cnt_in_csv_material_file = len(pd.read_csv(csv_material_file_path, encoding = 'utf-8'))

    pymysql.install_as_MySQLdb()

    sec_db = pymysql.connect(user = "root", password = "@realdata1!", host = '211.170.143.158', port = 13306, local_infile = True, autocommit = True)
    
    cursor = sec_db.cursor()
    cursor.execute("SET GLOBAL local_infile=1;")
    
    result = cursor.execute("""LOAD DATA LOCAL INFILE '{}' INTO TABLE sec.sec10h CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (BASE_DATE,SHRT_IS_CD,SEQ_NO,STND_IS_CD,IS_NM_KR,IS_NM_SHRT_KR,IS_NM_ENG,LSTD_DATE,MKT_DIV,IS_DIV,AFFILAT,STK_KND,FACE_VL,LSTD_IS_CNT,DELISTING_DATE,DELISTING_RESN,IS_LSTD);""".format(csv_material_file_path))

    sec_db.close()

    return (data_cnt_in_csv_material_file, result)