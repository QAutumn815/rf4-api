"""Full scrape: all tables, all regions/categories, with fish image caching"""
import os, sys, logging, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.settings")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath("."))

# Configure Django
import django
django.setup()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

from apps.parser.services import ParsersManager, DBProcessor


def run_task(name, model, weekly=False, label=""):
    log.info("%s Starting %s (weekly=%s) ...", label, model, weekly)
    start = time.time()

    parser = ParsersManager().create(name)
    data = []
    for each in parser.parse(weekly=weekly):
        data.extend(each)

    elapsed = time.time() - start
    log.info("%s Parsed %d records in %.1fs", label, len(data), elapsed)

    with_img = sum(1 for d in data if d.get("fish_image"))
    if with_img:
        log.info("%s fish_image on %d/%d records", label, with_img, len(data))

    # Check disk cache
    cache_dir = os.path.join("media", "fish")
    cached = len(os.listdir(cache_dir)) if os.path.isdir(cache_dir) else 0
    log.info("%s Cached fish images on disk: %d", label, cached)

    write_start = time.time()
    DBProcessor.write(model, data)
    log.info("%s Written to %s in %.1fs", label, model, time.time() - write_start)

    return len(data)


# 1. Absolute records
total_abs = run_task("records", "AbsoluteRecord", label="[ABS]")

# 2. Weekly records
total_wk = run_task("records", "WeeklyRecord", weekly=True, label="[WK]")

# 3. Ratings
total_ratings = run_task("ratings", "Rating", label="[RATING]")

# 4. Winners
total_winners = run_task("winners", "Winner", label="[WINNER]")

# Summary
cache_dir = os.path.join("media", "fish")
total_cached = len(os.listdir(cache_dir)) if os.path.isdir(cache_dir) else 0

log.info("=" * 50)
log.info("DONE!")
log.info("  AbsoluteRecord: %d", total_abs)
log.info("  WeeklyRecord:   %d", total_wk)
log.info("  Rating:         %d", total_ratings)
log.info("  Winner:         %d", total_winners)
log.info("  Total:          %d", total_abs + total_wk + total_ratings + total_winners)
log.info("  Fish images:    %d", total_cached)
