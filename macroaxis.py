from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)


def altman_z_score(ticker):
    url = f'https://www.macroaxis.com/invest/ratio/{ticker}/Z-Score'
    driver.get(url)
    try:
        z_score_div = driver.find_element(by=By.XPATH, value='/html/body/div[2]/section/section/div/div[1]/div[2]/table[1]/tbody/tr/td[5]/div')
    except NoSuchElementException:
        print(ticker, 'has no Z score!')
        z_score = None
    else:
        z_score = float(z_score_div.text.strip())
    return z_score
