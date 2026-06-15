"""Synchronous full scrape command.
Usage: python manage.py scrape_all
"""
import logging
import time

from django.core.management.base import BaseCommand

from apps.parser.services import ParsersManager, DBProcessor

logger = logging.getLogger(__name__)


def run_task(parser_name, model_name, weekly=False, label=""):
    logger.info("%s Starting %s (weekly=%s) ...", label, model_name, weekly)
    start = time.time()

    parser = ParsersManager().create(parser_name)
    data = []
    for each in parser.parse(weekly=weekly):
        data.extend(each)

    elapsed = time.time() - start
    logger.info("%s Parsed %d records in %.1fs", label, len(data), elapsed)

    with_img = sum(1 for d in data if d.get("fish_image"))
    if with_img:
        logger.info("%s fish_image on %d/%d records", label, with_img, len(data))

    write_start = time.time()
    DBProcessor.write(model_name, data)
    logger.info("%s Written to DB in %.1fs", label, time.time() - write_start)

    return len(data)


class Command(BaseCommand):
    help = "Scrape all tables synchronously with fish image caching"

    def handle(self, *args, **options):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )

        tasks = [
            ("records", "AbsoluteRecord", False, "[ABS]"),
            ("records", "WeeklyRecord", True, "[WK]"),
            ("ratings", "Rating", False, "[RATING]"),
            ("winners", "Winner", False, "[WINNER]"),
        ]

        totals = {}
        for args in tasks:
            totals[args[1]] = run_task(*args)
            logger.info("---")

        import os
        cache_dir = "media/fish"
        total_cached = len(os.listdir(cache_dir)) if os.path.isdir(cache_dir) else 0

        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS("SCRAPE COMPLETE"))
        for name, count in totals.items():
            self.stdout.write(f"  {name}: {count}")
        self.stdout.write(f"  Fish images cached: {total_cached}")
        self.stdout.write(f"  Grand total: {sum(totals.values())}")
