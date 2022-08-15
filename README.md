# 개발환경
- 언어 : python
- DB &nbsp;&nbsp;&nbsp;: MySQL
- IDE &nbsp;&nbsp;: Visual Studio Code, MySQL Workbench  

# DB SCHEMA 설계
 
- 'pykrx'패키지에 대한 document를 참고하여, ERD 제작  
(pykrx document : https://github.com/sharebook-kr/pykrx) 

* ERD 목록(physical)
  * 국내주식 : 
  * 국내ETF&nbsp;&nbsp; :
  * 해외주식 : 
<br/><br/>

* 테이블 정의서(logical)
  * 테이블 정의서 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:
  * 테이블 상세 정의서 :


# Python Script에 대한 개요
* SECXXH('이력성'테이블에 insert를 실시하는 프로그램)
  * 공통으로 사용되는 스크립트
    * main.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: batch file에 의해 실행되는 스크립트
    * logger.py &nbsp;&nbsp;&nbsp;&nbsp;: log 파일을 생성하는 스크립트
    * df_to_csv.py : DataFrame을 CSV로 저장하는 스크립트
    * insert.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: 'LOAD DATA INFILE'문법을 활용하여, 저장된 CSV파일을 테이블에 INSERT하는 스크립트
  * 고유하게 사용되는 스크립트
    * domestic_issue_download.py(SEC01H) : 'KRX 정보시스템'사이트 접속하여, 국내주식 기본정보를 다운받는 스크립트
    * get_df.py(SEC10H) : 'SEC01H', 'SEC08H'에 의해 생성된 CSV파일을 DataFrame으로 불러오는 스크립트
    * modify_df.py(SEC10H) : 'get_df.py'를 통해 불러온 DataFrame을 해당 테이블(SEC10H)의 SCHEMA에 맞춰 수정하는 스크립트
    * get_bsnss_date.py(SEC13H) : 한 주 내 평일을 조회하는 스크립트
<br/><br/>

* SECXXT('거래성'테이블에 insert를 실시하는 프로그램)
  * 공통으로 사용되는 스크립트
    * main.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: batch file에 의해 실행되는 스크립트
    * logger.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: log 파일을 생성하는 스크립트
    * df_to_csv.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: DataFrame을 CSV로 저장하는 스크립트
    * insert.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: 'LOAD DATA INFILE'문법을 활용하여, 저장된 CSV파일을 테이블에 INSERT하는 스크립트
    * make_XXXXX_df.py : 'pykrx'패키지를 활용하여 원하는 증권 데이터를 수집하고, 수집된 데이터를 DataFrame으로 선언하는 스크립트
  * 고유하게 사용되는 스크립트
    * make_OHLCV_df_for_failed_list_using_yfinance.py(SEC31T) : 'make_OHLCV_df_using_yfinance.py'로부터 주가 데이터 수집을 실패한 종목들에 대해 해당 데이터 수집을 재시도를 하는 스크립트
    * insert_for_failed.py(SEC31T) : 데이터 수집 재시도를 성공한 종목들의 주가 데이터를 insert하는 스크립트
<br/><br/>

* make_cov_matrix(증권별 주가 데이터에 대한 Covariance Matrix를 생성하는 프로그램)
  *  main.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: batch file에 의해 실행되는 스크립트
  *  domestic_stock.py : 국내 주식 종목별 1년 동안의 일별 수익률을 산출하고, 이를 DataFrame으로 선언하는 스크립트
  *  domestic_etf.py &nbsp;&nbsp;&nbsp;&nbsp;: 국내 ETF 종목별 1년 동안의 일별 수익률을 산출하고, 이를 DataFrame으로 선언하는 스크립트
  *  usa_stock.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: 미국 주식 종목별 1년 동안의 일별 수익률을 산출하고, 이를 DataFrame으로 선언하는 스크립트
  *  kue.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: 증권별 1년 동안의 일별 수익률 DataFrame(3개의 DataFrame)을 합친 후, Covariance Matrix를 산출하여 CSV파일로 저장하는 스크립트
