
from apps.parser.services import ParsersManager, DBProcessor

parser = ParsersManager().create("records")
data = []
for each in parser.parse(weekly=True):
    data.extend(each)
    print(f"Parsed: {len(data)}", flush=True)

with_img = sum(1 for d in data if d.get("fish_image"))
print(f"WeeklyRecord: {len(data)}, fish_image: {with_img}", flush=True)
DBProcessor.write("WeeklyRecord", data)
print("Written to DB", flush=True)
