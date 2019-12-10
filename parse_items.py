import json
import os.path
import time
import logging
from collections import defaultdict

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

while os.path.exists("items.json.lock"):
    logging.info("File locked. Sleeping 10s")
    time.sleep(10)
with open("items.json", 'r') as fp:
    items = json.load(fp)

dropped_items = defaultdict(int)

for _, event in items.items():
    if event:
        for key, item_list in event.items():
            if key != "timestamp":
                for item, count in item_list.items():
                    dropped_items[item] += count

for item, count in dropped_items.items():
    print(item, count)