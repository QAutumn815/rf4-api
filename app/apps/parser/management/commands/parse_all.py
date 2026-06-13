from django.core.management.base import BaseCommand

from apps.parser.tasks.task_data_process import process_data


class Command(BaseCommand):
    help = "Dispatch Celery tasks to parse all data (records, ratings, winners)"

    def handle(self, *args, **options):
        tasks = [
            ("records", "AbsoluteRecord", False),
            ("records", "WeeklyRecord", True),
            ("ratings", "Rating", False),
            ("winners", "Winner", False),
        ]

        for parser_name, model_name, weekly in tasks:
            result = process_data.delay(parser_name, model_name, weekly=weekly)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Dispatched {parser_name}/{model_name} (weekly={weekly}) "
                    f"→ task id: {result.id}"
                )
            )
