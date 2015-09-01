#!/usr/bin/python2.7

from functools import partial

import requests
from urlparse import urljoin
import logging
import dateutil.parser

import mongo

logger = logging.getLogger("events")
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logging.fatal("HEI")

access_token = ""

API="https://graph.facebook.com/v2.4/"

def graph_verb(verb, endpoint, **kwargs):
    auth = {'access_token': access_token}
    for x in ['params', 'data']:
        if x not in kwargs:
            kwargs[x] = auth
        else:
            kwargs[x].update(auth)
    return verb(urljoin(API, endpoint), **kwargs).json()


graph_get = partial(graph_verb, requests.get)

def get_events(pageid):
    res = graph_get(pageid + "/events")
    logger.debug(res)
    return res["data"]

def get_event_image(eventid):
    try:
        return graph_get(eventid, params={"fields":"cover"})["cover"]["source"]
    except KeyError:
        return "no picture"

if __name__ == "__main__":
    import sys
    if "--clean" in sys.argv:
        mongo.clean()

    for fbpage in ["hurra.is", "KexHostel", "nyjagamlabio", "mengiiceland"]:
        events = get_events(fbpage)
        for event in events:
            event["cover"] = get_event_image(event["id"])
            event["start_time"] = dateutil.parser.parse(event["start_time"])
        mongo.insert_many_events(events)


        
