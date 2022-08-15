import pymysql
import pandas as pd
from pandasql import sqldf

def load_data_infile(csv_material_file_path : str) :

    df_OHLCV_of_delisting = pd.read_csv(csv_material_file_path, encoding = 'utf-8')
    data_cnt_in_csv_material_file = len(df_OHLCV_of_delisting)

    delisting_issue_list = sqldf("SELECT DISTINCT 단축코드 FROM df_OHLCV_of_delisting")["단축코드"].values.tolist()  # delisting_issue_list : 지난 7일 동안 상장폐지 된 종목들을 요소로 가지는 list
    string_for_sql_delete_clause = ''
    for shrt_is_code in delisting_issue_list:

        string_for_sql_delete_clause = string_for_sql_delete_clause + "'" + shrt_is_code + "'" + ","

    string_for_sql_delete_clause = string_for_sql_delete_clause[:-1]  # delisting_issue_list 內 요소들을 합친 문자열 선언
                                                                      # (SEC12T 테이블 內 해당 종목들의 데이터에 대한 DELETE를 수행하기 때문에, 이 문자열 선언이 필요함)
    pymysql.install_as_MySQLdb()

    sec_db = pymysql.connect(user = "", password = "", host = '', port = "", local_infile = True, autocommit = True)
    cursor = sec_db.cursor()
   
    cursor.execute("SET GLOBAL local_infile=1;")

    cursor.execute("DELETE FROM sec.sec12t WHERE SHRT_IS_CD IN ({});".format(string_for_sql_delete_clause))
    result = cursor.execute("""LOAD DATA LOCAL INFILE '{}' INTO TABLE sec.sec12t CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (BASE_DATE,SHRT_IS_CD,OPN_PRC,HIGH_PRC,LOW_PRC,CLS_PRC,VOLUME);""".format(csv_material_file_path))
    print("* {} records loaded in table".format(result), "\n")

    sec_db.close()

    return (data_cnt_in_csv_material_file, result)