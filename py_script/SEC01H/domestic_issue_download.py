from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def listing_stock_download(path: str):                                           # 'data.krx.co.krx'에서 '주식기본정보' csv 파일을 다운받는 함수
                                                                                 # path 매개변수는 절대경로를 인자로 받음(상대경로 입력 시, 해당 경로에 다운되지 않음)

    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    # op.add_argument('--start-fullscreen')
    op.add_experimental_option("prefs", {"download.default_directory": path})    

    chromedriver = './crawling/chromedriver.exe'
    driver = webdriver.Chrome(chromedriver, chrome_options=op)

    url = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201"
    driver.get(url)
    time.sleep(3)                                                                # 업로드 시간 기다리기

    download_box = driver.find_element(
        By.CSS_SELECTOR, "#MDCSTAT019_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > button.CI-MDI-UNIT-DOWNLOAD")
    download_box.click()                                                         # 다운로드 박스 클릭
    time.sleep(3)

    
    csv_down = driver.find_element(                                              # csv 다운로드 박스 위치 지정
        By.CSS_SELECTOR, '#ui-id-1 > div > div:nth-child(2) > a')
    csv_down.send_keys('\n')                                                     # 해당 csv 다운로드 박스에 '키보드 엔터'입력을 전달
    time.sleep(3)
    driver.quit()

    return "downloading a csv file is finished"