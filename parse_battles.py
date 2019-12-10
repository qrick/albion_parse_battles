import requests
import json
import time
import os
import logging
from collections import defaultdict

limit = 50
max_offset = 1000

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

api_template = "https://gameinfo.albiononline.com/api/gameinfo/events?limit={}&offset={}"

while True:
    try:
        fp = open("items.json", 'r')
        items = json.load(fp)
        fp.close()
    except (IOError, json.decoder.JSONDecodeError):
        items = defaultdict(dict)
    open("items.json.lock", 'a').close()
    logging.info("File Locked")
    for offset in range(0, max_offset, limit):
        s = requests.get(api_template.format(limit, offset))
        if s.status_code != 200:
            continue
        for event in s.json():
            event_id = event["EventId"]
            if event_id not in items:
                items[event_id] = dict()
                items[event_id]['timestamp'] = event['TimeStamp']
                items[event_id]['items'] = defaultdict(int)
                for k, item in event["Victim"]["Equipment"].items():
                    if item:
                        items[event_id]['items'][item["Type"]] += 1
    with open("items.json", 'w') as fp:
        json.dump(items, fp)
    os.remove("items.json.lock")
    logging.info("File unlocked. Sleeping 60s")

    time.sleep(60)

