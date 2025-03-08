import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_driver():
    options = Options()
    options.add_argument("--headless")  # 백그라운드에서 실행
    options.add_argument("--disable-gpu")  # GPU 비활성화
    options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
    options.add_argument("start-maximized")  # 브라우저 최대화
    options.add_argument("disable-infobars")  # 정보 표시 비활성화
    options.add_argument("--disable-dev-shm-usage")  # DevShm 사용 비활성화

    # 사용자 에이전트 (일반적인 브라우저처럼 인식되도록 설정)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    return driver


def search_image(url):
    driver = get_driver()

    driver.get("https://www.bing.com/visualsearch")

    paste_area = driver.find_element(By.CLASS_NAME, "pastearea")
    paste_area.click()

    url_input = driver.find_element(By.CLASS_NAME, "imgpst")
    url_input.send_keys(url)
    url_input.send_keys(Keys.ENTER)

    time.sleep(3)

    first_img = driver.find_element(
        By.XPATH, '//*[@id="vs_images"]/div/div/ul/li[1]/div/div/div[1]/div[1]/a/img'
    )
    first_img_url = first_img.get_attribute("src")

    repsonse = requests.get(first_img_url).content

    with open("output.png", "wb") as f:
        f.write(repsonse)


image_url = "https://example.com/example.png"

search_image(image_url)
