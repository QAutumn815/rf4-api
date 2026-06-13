"""Re-scrape all regions and categories for records, test fish_image extraction"""
import os, sys, django, logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.settings")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))
django.setup()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

from apps.parser.services import ParsersManager, DBProcessor

REGIONS = ["gl", "ru", "de", "us", "fr", "cn", "pl", "kr", "jp", "en"]
CATEGORIES = ["records", "ultralight", "telestick"]

# Test: scrape ONE region/category first to verify fish_image extraction
log.info("=== Testing fish_image extraction with single scrape ===")
parser = ParsersManager().create("records")
data = []
for each in parser.parse(weekly=False):
    data.extend(each)

# Check if fish_image was extracted
total = len(data)
with_image = sum(1 for d in data if d.get("fish_image"))
sample = [d for d in data if d.get("fish_image")][:5]

log.info(f"Total records scraped: {total}")
log.info(f"Records with fish_image: {with_image}")
log.info(f"Sample fish URLs:")
for d in sample:
    log.info(f"  {d['fish']}: {d['fish_image']}")

if with_image > 0:
    log.info("✅ Fish image extraction works!")
else:
    log.warning("⚠️ No fish images extracted - check parser logic")
    # Debug: show sample raw data
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver

    CHROMEDRIVER = r"C:\Users\Qiu\.wdm\drivers\chromedriver\win64\148.0.7778.178\chromedriver-win32\chromedriver.exe"
    CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = CHROME_BIN

    service = Service(executable_path=CHROMEDRIVER)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://rf4game.ru/records/abs/GL/records")

    import time
    time.sleep(5)

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    item_icons = soup.find_all("div", class_="item_icon")
    log.info(f"Total item_icon divs on page: {len(item_icons)}")
    if item_icons:
        log.info(f"First item_icon style: {item_icons[0].get('style', '')[:200]}")

    rows_containers = soup.find_all(attrs={"class": "rows"})
    log.info(f"Total .rows containers: {len(rows_containers)}")

    # Check first few fish blocks
    for i, container in enumerate(rows_containers[:5]):
        icon = container.find("div", class_="item_icon")
        log.info(f"  Fish block {i}: item_icon={icon is not None}")
        if icon:
            log.info(f"    style={icon.get('style', '')[:150]}")

    driver.quit()
