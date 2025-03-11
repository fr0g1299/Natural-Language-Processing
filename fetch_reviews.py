import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait


def fetch_reviews(url):
    """Fetches reviews from IMDb, including loading all available reviews."""

    driver = webdriver.Chrome()
    driver.get(url)

    total_reviews = 0
    title = ""

    try:
        # Get the title of the movie/TV show
        title_element = driver.find_element(By.XPATH, "//h2[@data-testid='subtitle']")
        title = title_element.text
    except:
        return []  # Return an empty list if no title is found

    try:
        # Get the total number of reviews
        total_reviews_element = driver.find_element(By.XPATH, "//div[@data-testid='tturv-total-reviews']")
        total_reviews_text = total_reviews_element.text.replace(',', '')  # Remove commas from the number
        total_reviews = int(total_reviews_text.split()[0])
        # print(f"Total reviews: {total_reviews}")
    except:
        return []  # Return an empty list if no reviews are found
    
    # If there are more than 25 reviews, expand all reviews
    if total_reviews > 25:
        try:
                time.sleep(3)
                button = driver.find_element(By.XPATH, "//span[contains(@class, 'ipc-see-more__text') and text()='All']/ancestor::button")
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)
                button.click()
                time.sleep(1)

                # Wait until all reviews are loaded or a timeout occurs
                WebDriverWait(driver, 60).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, 'article.sc-7d2e5b85-1.cvfQlw.user-review-item')) >= total_reviews or len(d.find_elements(By.CSS_SELECTOR, 'article.sc-7d2e5b85-1.cvfQlw.user-review-item')) >= 1000)
        except Exception as e:
            print("Could not find or click the 'All' button:", e)
    
    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    reviews = [review.get_text(strip=True) for review in soup.find_all('article', class_='sc-7d2e5b85-1 cvfQlw user-review-item')]
    return reviews, title
