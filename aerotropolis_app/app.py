import json
from os.path import expanduser
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from universal.connect_db import news_db, lst_src
import time

app = Flask(__name__)


def get_googlemap_key():
    key_f = expanduser("~/.credentials/googlemapapi")
    with open(key_f) as f:
        key = f.read()
    return key


key = get_googlemap_key().strip()


@app.route('/')
@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('zz_googlemapapi.html', key=key)


@app.route('/')
@app.route('/news', methods=['GET', 'POST'])
def list_all_news():
    news = []
    for src in lst_src:
        news_collections = news_db[src]
        collections = news_collections.find({}).sort("date_released", pymongo.DESCENDING)

        lst = []
        for n in collections:
            d = {
                "date_released": str(n["date_released"].date()), "title": n["title"],
                "source": src, "_id": str(n["_id"])
            }
            if "importance" in n:
                d["importance"] = n["importance"]
            lst.append(d)
        news.extend(lst)

    news.sort(key=lambda doc:doc["date_released"], reverse=True)
    return render_template('index.html', news=news)


@app.route("/news/<string:src>/<string:news_id>/", methods=['GET', 'POST'])
def show_content(src, news_id):
    if request.method == "POST":
        news_collections = news_db[src]
        if "gomap" in request.form:
            return redirect(url_for("gomap", src=src, news_id=news_id))
        else:
            if "kword" in request.form and request.form["kword"]!='':
                news_collections.update(
                    {"_id": ObjectId(news_id)},
                    {"$push": {
                        "keywords": {"keyword": request.form["kword"]}
                    }}
                )
            if "importance" in request.form:
                news_collections.update(
                    {"_id": ObjectId(news_id)},
                    {"$set": {"importance": int(request.form["importance"])}}
                )
            return redirect(url_for('show_content', src=src, news_id=news_id))
    else:
        news_collections = news_db[src]
        d = news_collections.find_one({"_id": ObjectId(news_id)})
        doc = {
            "date_released": str(d["date_released"].date()), "title": d["title"],
            "source": src, "_id": str(d["_id"]), "content":d["content"].replace("<br>", "").strip()
                }
        if "importance" in d:
            doc["importance"] = d["importance"]
        if "keywords" in d:
            doc["keywords"] = d["keywords"]
        else:
            doc["keywords"] = []
        return render_template('news_edit.html', doc=doc)


@app.route("/news/<string:src>/<string:news_id>/map", methods=['GET', 'POST'])
def gomap(src, news_id):
    news_collections = news_db[src]
    doc = news_collections.find_one({"_id": ObjectId(news_id)})
    content = doc["content"].replace("<br>", "").strip()
    kwords = doc["keywords"]

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


@app.route("/news/<string:src>/<string:news_id>/delete/<string:kword>", methods=['POST'])
def delete_keyword(src, news_id, kword):
    if request.method == "POST":
        news_collections = news_db[src]
        print(kword)
        news_collections.update(
            {"_id": ObjectId(news_id)},
            {"$pull":{"keywords":{"keyword":kword}}}
        )

    return redirect(url_for('show_content', src=src, news_id=news_id))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
