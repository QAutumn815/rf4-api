"""Debug Chrome startup issue"""
import subprocess, sys, time

CHROMEDRIVER = r"C:\Users\Qiu\.wdm\drivers\chromedriver\win64\148.0.7778.178\chromedriver-win32\chromedriver.exe"

# Test 1: Can chromedriver start?
print("=== Test 1: Starting chromedriver ===")
proc = subprocess.Popen(
    [CHROMEDRIVER, "--version"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
out, err = proc.communicate(timeout=10)
print(f"chromedriver --version: {out.strip()}")
if err:
    print(f"stderr: {err.strip()}")

# Test 2: Start Chrome with chromedriver
print("\n=== Test 2: Start Chrome via Selenium with timeout ===")
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.binary_location = CHROME_BIN

service = Service(executable_path=CHROMEDRIVER, service_args=["--verbose"])

try:
    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome started!")
    driver.get("https://rf4game.ru/records/abs/GL/records")
    print(f"Title: {driver.title}")
    driver.quit()
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    # Check if any error logs from chromedriver
    if service.process:
        print(f"Chromedriver return code: {service.process.poll()}")
