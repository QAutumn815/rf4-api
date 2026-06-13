"""Quick test: start Chrome and load rf4game.ru"""
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROMEDRIVER = r"C:\Users\Qiu\.wdm\drivers\chromedriver\win64\148.0.7778.178\chromedriver-win32\chromedriver.exe"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = CHROME_BIN

service = Service(executable_path=CHROMEDRIVER)
try:
    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome started OK")
    driver.get("https://rf4game.ru")
    print("Page title:", driver.title[:80])
    driver.quit()
    print("All OK!")
except WebDriverException as e:
    print(f"WebDriver Error: {e}")
except Exception as e:
    print(f"Error: {e}")
