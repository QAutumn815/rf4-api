from apps.parser.services import ParsersManager, DBProcessor

parser = ParsersManager().create("winners")
data = []
for each in parser.parse(weekly=False):
    data.extend(each)
    print(f"Winner: Parsed {len(data)}", flush=True)
print(f"Winner total: {len(data)}", flush=True)
DBProcessor.write("Winner", data)
print("Winner written to DB", flush=True)
