
from apps.parser.services import ParsersManager, DBProcessor

parser = ParsersManager().create("records")
data = []
for each in parser.parse(weekly=False):
    data.extend(each)
    print(f'Parsed: {len(data)} total records')
with_img = sum(1 for d in data if d.get("fish_image"))
print(f'fish_image: {with_img}/{len(data)}')

DBProcessor.write("AbsoluteRecord", data)
print("Written to DB")
