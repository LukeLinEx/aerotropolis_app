import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template
from universal.connect_db import udn, tycg

app = Flask(__name__)


@app.route('/')
@app.route('/news')
def list_all_news():
    news = tycg.find({}).sort("date_released", pymongo.DESCENDING)

    lst = []
    for n in news:
        d = {
            "date_released": str(n["date_released"].date()), "title": n["title"]
        }
        lst.append(d)

    return render_template('index.html', items=lst)


@app.route("/news/<string:news_id>/")
def show_contest(news_id):
    news = udn.find_one({"_id": ObjectId(news_id)})
    return news["content"]


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
