import pymysql
import pandas as pd
import os

def load_data_infile(csv_material_path) :
    
    """ 

    'csv_for_table_insert_material'디렉토리에 가장 최근에 저장된 csv파일을 dataframe으로 읽기 
    (13행 ~ 21행)
    
    """
    
    file_name_and_time_lst = []
    for f_name in os.listdir(f"{csv_material_path}"):

        modified_time = os.path.getmtime(f"{csv_material_path}{f_name}")
        file_name_and_time_lst.append((f_name, modified_time))

    sorted_file_lst = sorted(file_name_and_time_lst, key=lambda x: x[1], reverse=True)
    recent_file_info = sorted_file_lst[0]
    recent_csv_file_path = csv_material_path + recent_file_info[0]

    data_cnt_in_recent_csv_file = len(pd.read_csv(recent_csv_file_path, encoding = 'utf-8'))

    """ 
    
    MySQL remote connection 
    (30행 ~ 36행)
    
    """

    pymysql.install_as_MySQLdb()

    sec_db = pymysql.connect(user = "", password = "", host = '', port = "", local_infile = True, autocommit = True)
    cursor = sec_db.cursor()
    cursor.execute("SET GLOBAL local_infile=1;")
    result = cursor.execute("""LOAD DATA LOCAL INFILE '{}' INTO TABLE sec.sec01h CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (BASE_DATE,STND_IS_CD,SHRT_IS_CD,IS_NM_KR,IS_NM_SHRT_KR,IS_NM_ENG,LSTD_DATE,MKT_DIV,IS_DIV,AFFILAT,STK_KND,FACE_VL,LSTD_IS_CNT);""".format(recent_csv_file_path))

    sec_db.close()

    return (data_cnt_in_recent_csv_file, result)