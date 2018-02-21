from flask import Flask, render_template
from news.news import news_bp
from map.map import map_bp


app = Flask(__name__)


app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(map_bp, url_prefix='/map')




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
