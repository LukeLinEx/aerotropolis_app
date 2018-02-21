import json
from os.path import expanduser
from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from universal.connect_db import news_db, lst_src


def get_googlemap_key():
    key_f = expanduser("~/.credentials/googlemapapi")
    with open(key_f) as f:
        key = f.read()
    return key


key = get_googlemap_key().strip()


map_bp = Blueprint("map", __name__)


@map_bp.route("/<string:src>/<string:news_id>", methods=['GET', 'POST'])
def gomap(src, news_id):
    news_collections = news_db[src]
    doc = news_collections.find_one({"_id": ObjectId(news_id)})
    content = doc["content"].replace("<br>", "").strip()
    if "keywords" in doc:
        kwords = doc["keywords"]
    else:
        kwords = []


    all_keywords = []
    for tmp in kwords:
        all_keywords.extend(tmp.values())

    if request.method == "POST":
        tmp = json.loads(request.args['doc'])

        for doc in tmp:
            if doc["keyword"] in all_keywords:
                news_db[src].update(
                    {"_id": ObjectId(news_id), "keywords.keyword":doc["keyword"]},
                    {"$set": {"keywords.$": doc}}
                )
            else:
                news_db[src].update(
                    {"_id": ObjectId(news_id)},
                    {"$push": {"keywords": doc}}
                )
        return redirect(url_for("gomap", src=src, news_id=news_id))
    else:
        return render_template("googlemapapi.html", src=src, new_id=news_id, content=content, key=key, kwords=kwords)