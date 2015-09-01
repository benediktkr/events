#coding: utf-8

import pymongo
import logging
import datetime
import locale

logger = logging.getLogger("events")
locale.setlocale(locale.LC_TIME, "is_IS.UTF8")

client = pymongo.MongoClient()
db = client.events

db.event.ensure_index([("start_time", pymongo.DESCENDING)])

def clean():
    db.event.remove()

def insert_many_events(events):
    for event in events:
        event["_id"] = event["id"]
        weekday = event["start_time"].strftime("%A")[:-2] + "inn"
        event["pretty_date"] = weekday + event["start_time"].strftime(" þann %d. %b")
        event["pretty_time"] = event["start_time"].strftime("%H:%M")
        try:
            db.event.insert_one(event)
            logger.debug(u"Inserted event: {0}".format(event["name"]))
        except pymongo.errors.DuplicateKeyError:
            logger.info(u"Duplicate event: {0}".format(event["name"]))


def get_events(n=20):
    now = datetime.datetime.now()
    a = db.event.find({"start_time": {"$gt": now}}).sort("start_time", pymongo.ASCENDING).limit(n)
     
    return a
