# Absolute records scrape - run via: python manage.py shell -c "exec(open('scrape_abs.py').read())"
from apps.parser.services import ParsersManager, DBProcessor

parser = ParsersManager().create("records")
data = []
for each in parser.parse(weekly=False):
    data.extend(each)
print(f"AbsoluteRecord: {len(data)} records")
with_img = sum(1 for d in data if d.get("fish_image"))
print(f"  fish_image: {with_img}")
DBProcessor.write("AbsoluteRecord", data)
print("  written to DB")
