from apps.parser.services import ParsersManager, DBProcessor

parser = ParsersManager().create("ratings")
data = []
for each in parser.parse(weekly=False):
    data.extend(each)
    print(f"Rating: Parsed {len(data)}", flush=True)
print(f"Rating total: {len(data)}", flush=True)
DBProcessor.write("Rating", data)
print("Rating written to DB", flush=True)
