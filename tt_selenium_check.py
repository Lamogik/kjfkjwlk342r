"""from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent

# конфигурация силениума + обход капчи
def get_views_with_selenium(url):
    ua = UserAgent()
    user_agent = ua.random

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")  # браузер в фоновом режиме
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = "/usr/bin/chromium"   # (опционально, строку можно закоментировать), если в закомментированном виде не работает, прописать путь к браузеру

    # нициализация антидетект хром-бразуера
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # ожидание загрузки страницы (5 сек)

        # поиск всех элементов с кол-вом просмотров
        view_elements = driver.find_elements(By.CSS_SELECTOR,
                                                 "strong.video-count.css-dirst9-StrongVideoCount")

        total_views = 0.0
        video_views = [element.text for element in view_elements]
        print(f"url: {url}", video_views)
        for element in video_views:
            element = element.lower()
            if "k" in element:
                total_views += float(element.replace('k', '')) * 1000
            else:
                total_views += float(element)
        print(f"url: {url}, Всего просмотров: {total_views}")
        return int(total_views)

    finally:
        driver.quit()

"""
