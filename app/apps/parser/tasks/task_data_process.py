from selenium.common.exceptions import TimeoutException, WebDriverException

from apps.parser.services import ParsersManager, DBProcessor
from worker               import app


@app.task(
    autoretry_for = (TimeoutException, WebDriverException, OSError, ConnectionError),
    retry_kwargs  = {"max_retries": 3, "countdown": 10},
    default_retry_delay = 30,
)
def process_data(parser_name, model_name: str, *args, **kwargs) -> None:
    parser = ParsersManager().create(parser_name)
    data   = []

    # Parse and unpack data
    for each in parser.parse(weekly = kwargs.get("weekly", False)):
        data.extend(each)

    # Write data to db
    DBProcessor.write(
        model_name,
        data
    )


# process_data.delay("records", "AbsoluteRecord")
# process_data.delay("records", "WeeklyRecord", weekly = True)
# process_data.delay("ratings", "Rating")
# process_data.delay("winners", "Winner")