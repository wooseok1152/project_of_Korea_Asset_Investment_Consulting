import os
import pymysql
import pandas as pd

def load_data_infile(csv_material_directory_path : str) :

    file_name_and_time_lst = []
    for f_name in os.listdir(f"{csv_material_directory_path}"):

        modified_time = os.path.getmtime(f"{csv_material_directory_path}{f_name}")
        file_name_and_time_lst.append((f_name, modified_time))

    sorted_file_lst = sorted(file_name_and_time_lst, key=lambda x: x[1], reverse=True)
    recent_file_info = sorted_file_lst[0]
    recent_csv_file_path = csv_material_directory_path + recent_file_info[0]
    print("* path of csv file downloaded recently :", recent_csv_file_path, "\n")

    data_cnt_in_recent_csv_file = len(pd.read_csv(recent_csv_file_path, encoding = 'utf-8'))

    """ 

    MySQL remote connection 

    """

    pymysql.install_as_MySQLdb()

    sec_db = pymysql.connect(user = "", password = "", host = '', port = "", local_infile = True, autocommit = True)
    cursor = sec_db.cursor()
    cursor.execute("SET GLOBAL local_infile=1;")
    result = cursor.execute("""LOAD DATA LOCAL INFILE '{}' INTO TABLE sec.sec08h CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (BASE_DATE,SHRT_IS_CD,SEQ_NO,IS_NM_SHRT_KR,MKT_DIV,IS_DIV,STK_KND,LSTD_DATE,DELISTING_DATE,DELISTING_RESN);""".format(recent_csv_file_path))

    sec_db.close()

    return (data_cnt_in_recent_csv_file, result)