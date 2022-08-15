from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from pandasql import sqldf

def listing_stock_download():

    op = webdriver.ChromeOptions()
    # op.add_argument('headless')
    op.add_argument('--start-fullscreen')
    op.add_experimental_option("prefs", {"download.default_directory": "D:\\20.share\\한국자산투자컨설팅\\30_거래정지예측모형\\2022\\py\\download"})

    chromedriver = 'D:/20.share/한국자산투자컨설팅/30_거래정지예측모형/2022/py/chromedriver.exe'
    driver = webdriver.Chrome(chromedriver, chrome_options=op)

    url = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201"
    driver.get(url)
    time.sleep(3)  # 업로드 시간 기다리기

    # 다운로드 박스 클릭
    download_box = driver.find_element(By.CSS_SELECTOR, "#MDCSTAT019_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > button.CI-MDI-UNIT-DOWNLOAD")
    download_box.click()
    time.sleep(1)

    # csv 다운로드 박스 클릭
    csv_down = driver.find_element(By.CSS_SELECTOR, '#ui-id-1 > div > div:nth-child(2) > a')
    csv_down.send_keys('\n')  # 해당 링크/명령어에 엔터를 실행하도록
    time.sleep(5)
    driver.quit()
    
    return 

def listing_etf_download():
    chromedriver = 'C:/Users/analysis1/Desktop/Project/chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    url = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201"
    driver.get(url)
    time.sleep(3)  # 업로드 시간 기다리기

    # 다운로드 박스 클릭
    download_box = driver.find_element(By.CSS_SELECTOR, "#MDCSTAT019_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > button.CI-MDI-UNIT-DOWNLOAD")
    download_box.click()
    time.sleep(1)

    # csv 다운로드 박스 클릭
    csv_down = driver.find_element(By.CSS_SELECTOR, '#ui-id-1 > div > div:nth-child(2) > a')
    csv_down.send_keys('\n')  # 해당 링크/명령어에 엔터를 실행하도록
    time.sleep(1)
    driver.quit()

    return

listing_stock_download()