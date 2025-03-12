import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import pandas as pd


def get_etf_trading_reference_rates():
    def get_etf_trading_reference_rates_per_page(driver) -> dict:
        try:
            tbody_wait = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tbody"))
            )
            WebDriverWait(tbody_wait, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tr"))
            )

            trs = driver.find_elements(By.CLASS_NAME, 'tr')
            tbody_data = []
            for tr in trs:
                tr_data = [td.text for td in tr.find_elements(By.CLASS_NAME, 'td')]
                tbody_data.append(tr_data)

            etf_trading_reference_rates_per_page = pd.DataFrame(tbody_data)
            etf_trading_reference_rates_per_page.columns = etf_trading_reference_rates_per_page.iloc[0]
            etf_trading_reference_rates_per_page = etf_trading_reference_rates_per_page.drop(0)
            etf_trading_reference_rates_per_page = etf_trading_reference_rates_per_page.to_dict()
            etf_trading_reference_rates_per_page['資料時間'] = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'date'))
            ).text
            etf_trading_reference_rates_per_page['message'] = "success"
            return etf_trading_reference_rates_per_page
        except Exception as e:
            print(e)
            return {'message': "元素未能及時加載，跳過此頁"}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options
    )

    try:
        driver.get("https://www.yuantaetfs.com/TradeInfo/rate")
        tbody_wait = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tbody"))
        )
        WebDriverWait(tbody_wait, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tr"))
        )
    except TimeoutException:
        driver.quit()
        return {'message': "整個網頁加載失敗，請檢查伺服器網絡或網站狀況"}

    buttons = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "btnEach"))
    ).find_elements(By.CSS_SELECTOR, ".btnEach button")

    payload = {}
    for button in buttons:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(button)).click()
            payload[button.text] = get_etf_trading_reference_rates_per_page(driver)
        except (TimeoutException, WebDriverException) as e:
            payload[button.text] = {'message': f"頁面加載失敗，跳過 {button.text} 頁"}

    driver.quit()
    return payload