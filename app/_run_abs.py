"""AbsoluteRecord scrape - iterate page by page with per-page error handling"""
import traceback
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings')
django.setup()

from django.apps import apps
from django.db import transaction
from apps.parser.services import WebDriver, URLsManager
from apps.parser.services.data import RecordsFetcher, RecordsParser
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException

model = apps.get_model("core.AbsoluteRecord")

# Get all URLs
um = URLsManager()
urls = um.records_urls(weekly=False)

# Count total pages
total_pages = sum(len(cats) if isinstance(cats, dict) else 1 for cats in urls.values())
print(f"Total pages to scrape: {total_pages}", flush=True)

driver = WebDriver()
parser = RecordsParser(fetcher=RecordsFetcher(driver, um))

total = 0
errors = 0
page_num = 0

for region, categories in urls.items():
    for category, url in (categories.items() if isinstance(categories, dict) else [('records', categories)]):
        page_num += 1
        try:
            html = driver.fetch_raw_html(url, "records_wrapper")
            batch = parser._parse_data(html, region, category=category)
            if batch:
                with transaction.atomic():
                    model.objects.bulk_create([model(**each) for each in batch])
                total += len(batch)
                images = sum(1 for x in batch if x.get("fish_image"))
                print(f"[{page_num}/{total_pages}] {region}/{category}: {len(batch)} records, {images} images (total: {total})", flush=True)
            else:
                print(f"[{page_num}/{total_pages}] {region}/{category}: 0 records (empty)", flush=True)
        except (TimeoutException, WebDriverException) as e:
            errors += 1
            print(f"[{page_num}/{total_pages}] {region}/{category}: ERROR - {e}", flush=True)
            if errors >= 10:
                print("Too many consecutive errors, stopping", flush=True)
                break
        except Exception as e:
            errors += 1
            print(f"[{page_num}/{total_pages}] {region}/{category}: UNEXPECTED ERROR - {e}", flush=True)
            traceback.print_exc()
            if errors >= 5:
                break

driver.quit()
print(f"\nDone: {total} records, {errors} errors", flush=True)
print(f"Final DB count: {model.objects.count()}", flush=True)
