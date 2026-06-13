"""Full scrape script - scrape all tables with fish_image support"""
import os, sys, django, logging, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.settings")
django.setup()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

from apps.parser.services import ParsersManager, DBProcessor


def run_task(name, model, weekly=False):
    log.info(f"▶️  Starting {model} (weekly={weekly}) ...")
    start = time.time()

    parser = ParsersManager().create(name)
    data = []
    for each in parser.parse(weekly=weekly):
        data.extend(each)

    elapsed = time.time() - start
    log.info(f"   Parsed {len(data)} records in {elapsed:.1f}s")

    # Check fish_image coverage (for records)
    with_img = sum(1 for d in data if d.get("fish_image"))
    if with_img:
        log.info(f"   ✅ fish_image present on {with_img}/{len(data)} records")
        # Show a sample
        for d in data:
            if d.get("fish_image"):
                log.info(f"   Sample: {d['fish'][:30]} -> {d['fish_image']}")
                break

    # Write to DB
    write_start = time.time()
    DBProcessor.write(model, data)
    write_elapsed = time.time() - write_start
    log.info(f"   Written to {model} in {write_elapsed:.1f}s")

    return len(data)


# 1. Absolute records
total_abs = run_task("records", "AbsoluteRecord", weekly=False)

# 2. Weekly records
total_wk = run_task("records", "WeeklyRecord", weekly=True)

# 3. Ratings
total_ratings = run_task("ratings", "Rating", weekly=False)

# 4. Winners
total_winners = run_task("winners", "Winner", weekly=False)

log.info("=" * 50)
log.info("✅ Scraping complete!")
log.info(f"   AbsoluteRecord: {total_abs}")
log.info(f"   WeeklyRecord:   {total_wk}")
log.info(f"   Rating:         {total_ratings}")
log.info(f"   Winner:         {total_winners}")
log.info(f"   Total:          {total_abs + total_wk + total_ratings + total_winners}")
