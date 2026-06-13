"""Run this with: python manage.py shell < run_parse.py"""
import logging, time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

from apps.parser.services import ParsersManager, DBProcessor


def run_task(name, model, weekly=False, label=""):
    log.info(f"{label} Starting {model} (weekly={weekly}) ...")
    start = time.time()

    parser = ParsersManager().create(name)
    data = []
    for each in parser.parse(weekly=weekly):
        data.extend(each)

    elapsed = time.time() - start
    log.info(f"{label} Parsed {len(data)} records in {elapsed:.1f}s")

    with_img = sum(1 for d in data if d.get("fish_image"))
    if with_img:
        log.info(f"{label} ✅ fish_image present on {with_img}/{len(data)} records")
        for d in data:
            if d.get("fish_image"):
                log.info(f"{label} Sample: {str(d['fish'])[:30]} -> {d['fish_image']}")
                break

    write_start = time.time()
    DBProcessor.write(model, data)
    log.info(f"{label} Written to {model} in {time.time()-write_start:.1f}s")
    return len(data)


total_abs = run_task("records", "AbsoluteRecord", label="[ABS]")
total_wk = run_task("records", "WeeklyRecord", weekly=True, label="[WK]")
total_ratings = run_task("ratings", "Rating", label="[RATING]")
total_winners = run_task("winners", "Winner", label="[WINNER]")

log.info("=" * 50)
log.info(f"DONE! Total: {total_abs + total_wk + total_ratings + total_winners}")
