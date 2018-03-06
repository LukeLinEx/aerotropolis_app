import pymongo
from flask import Blueprint, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from universal.connect_db import news_db, lst_src


news_bp = Blueprint("news", __name__)


@news_bp.route('/', methods=['GET', 'POST'])
def list_all_news():
    news_ = []
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
        news_.extend(lst)

    news_.sort(key=lambda doc:doc["date_released"], reverse=True)
    return render_template('index.html', news=news_ )


@news_bp.route("/<string:src>/<string:news_id>/", methods=['GET', 'POST'])
def show_content(src, news_id):
    if request.method == "POST":
        news_collections = news_db[src]
        if "gomap" in request.form:
            return redirect(url_for("map.gomap", src=src, news_id=news_id))
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
            return redirect(url_for('news.show_content', src=src, news_id=news_id))
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


@news_bp.route("/<string:src>/<string:news_id>/<string:kword>/delete", methods=['POST'])
def delete_keyword(src, news_id, kword):
    if request.method == "POST":
        news_collections = news_db[src]
        news_collections.update(
            {"_id": ObjectId(news_id)},
            {"$pull":{"keywords":{"keyword":kword}}}
        )
    return redirect(url_for('news.show_content', src=src, news_id=news_id))


@news_bp.route("/google6d7dfa23595b00ef.html")
def google_verify():
    return render_template("google6d7dfa23595b00ef.html")