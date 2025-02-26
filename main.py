import base64
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def search_similar_images(image_path):
    # Chrome 옵션 설정 (Headless 모드 활성화)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 브라우저 창 없이 실행
    options.add_argument(
        "--disable-gpu"
    )  # GPU 가속 비활성화 (Linux 환경에서 필요할 수 있음)
    options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화 (일부 환경에서 필요)
    options.add_argument(
        "--disable-dev-shm-usage"
    )  # 공유 메모리 사용 비활성화 (Docker 환경에서 필요할 수 있음)

    # Chrome 드라이버 설정
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    # 구글 이미지 검색 페이지로 이동
    driver.get("https://images.google.com/")

    try:
        time.sleep(1)
        # 카메라 아이콘 버튼을 기다리고 클릭
        camera_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[1]/div[3]/div[4]",
                )
            )
        )
        camera_icon.click()

        time.sleep(0.3)
        # '이미지 업로드' 탭을 기다리고 클릭
        upload_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/c-wiz/div[2]/div/div[2]/div[2]/c-wiz/div[2]/input",
                )
            )
        )
        upload_tab.click()
        upload_tab.send_keys(image_path)

        # '검색' 버튼을 클릭
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/c-wiz/div[2]/div/div[2]/div[2]/c-wiz/div[2]/div",
                )
            )
        )
        search_button.click()

        time.sleep(3)  # 잠시 대기 후 결과 확인

        try:
            # 'dimg'로 시작하는 id를 가진 첫 번째 img 태그 찾기
            first_img = driver.find_element(By.CSS_SELECTOR, "img[id^='dimg']")

            # src 속성 가져오기
            img_src = first_img.get_attribute("src")

            header, encoded = img_src.split(",", 1)

            # Base64 디코딩
            image_data = base64.b64decode(encoded)

            # 파일로 저장
            with open("output.jpg", "wb") as f:
                f.write(image_data)

            print("이미지가 output.jpg로 저장되었습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")

    except Exception as e:
        print(f"오류 발생: {e}")

    driver.quit()


# 사용 예시
image_path = "https://example.com/image.jpg"
search_similar_images(image_path)
