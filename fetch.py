
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome()
driver.get('https://www.imdb.com/title/tt13406094/reviews/?ref_=tt_ururv_sm')

total_reviews = 0

total_reviews_element = driver.find_element(By.XPATH, "//div[@data-testid='tturv-total-reviews']")
total_reviews_text = total_reviews_element.text.replace(',', '')
total_reviews = int(total_reviews_text.split()[0])

print(f"Total reviews: {total_reviews}")

if total_reviews > 25:
    try:
            time.sleep(3)
            button = driver.find_element(By.XPATH, "//span[contains(@class, 'ipc-see-more__text') and text()='All']/ancestor::button")
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button.click()
            time.sleep(1)

            WebDriverWait(driver, 60).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, 'article.sc-7d2e5b85-1.cvfQlw.user-review-item')) >= total_reviews)
    except Exception as e:
        print(e)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

reviews = [review.get_text(strip=True) for review in soup.find_all('article', class_='sc-7d2e5b85-1 cvfQlw user-review-item')]

print(f"Total reviews: {len(reviews)}")
