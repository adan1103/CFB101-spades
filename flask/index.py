from flask import Flask, render_template, url_for, request, jsonify
from flask_pymongo import PyMongo, pymongo
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter
from waitress import serve

# mongodb連線 (mongodb需增加ip才看得到)
mongodb_atlas_account = "account"
mongodb_atlas_password = "password"
client = MongoClient('mongodb+srv://{}:{}@twfruit.i2omj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'.format(mongodb_atlas_account, mongodb_atlas_password))
db = client.TWFruits

app = Flask(__name__, static_url_path='/static', static_folder='./static')

# 模板管理
bootstrap = Bootstrap(app)

# 主頁(一開始進去的)
@app.route('/')
def index():
    return render_template('index.html')

# 主頁(點選主頁後)
@app.route('/main')
def main_page():
    return render_template('index.html')

# 農業新聞
@app.route('/news')
def news():
    news = db.news
    page_index = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10
    all_news = [x for x in news.find().sort('date', pymongo.DESCENDING)]
    news_data = []
    # last_id = all_news[limit*(page_index-1)]['news_id']
    now = limit * (page_index-1)
    for i in range(limit):
        try:
            news_data.append(all_news[now+i])
        except:
            break

    pagination = Pagination(page=page_index, total=len(all_news), per_page_parameter=10, error_out=False, css_framework='bootstrap3')
    return render_template('news.html', posts=news_data, pagination=pagination)


@app.route('/other_link')
def other():
    return render_template('other_link.html')

if __name__ =='__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)   # 0.0.0.0 代表所有人都能訪問
    serve(app, host="0.0.0.0", port=8080)
