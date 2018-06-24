import sys
sys.path.append("kairo")

""" This example outlines how to a build a bot that returns comics from xkcd
    
"""
from kairo import Kairo
import random
import urllib2
import json


k = Kairo("app")


@k.command("xkcd")
def random_comic(user):
    info = fetch_info()
    last_comic_id = info["num"]
    random_comic = random.randint(0, last_comic_id)
    comic_data = fetch_info(random_comic)
    return comic_data["img"]


@k.command("xkcd <comic_id>")
def comic_by_id(user, comic_id):
    comic_data = fetch_info(comic_id)
    return comic_data["img"]


# helper methods
def fetch_info(comic_id=None):
    url = "https://xkcd.com/info.0.json" if comic_id is None else "https://xkcd.com/" + str(comic_id) + "/info.0.json"
    data = fetch(url)
    return data


def fetch(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', "kairo-bot")
    resp = urllib2.urlopen(req)
    data = json.loads(resp.read())
    return data


k.start_bot()