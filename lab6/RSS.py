# Простой RSS reader
#
# При добавлении ленты (например https://habrahabr.ru/rss/interesting/)
# записи из добавленной ленты сканируются и заносятся в базу (например sqlite)
#
# При нажатии на кнопку обновить - новое сканирование и добавление новых записей (без дублрования существующих)
#
# Отображение ленты начиная с самых свежих записей с пагинацией (несколько записей на странице)
#
# Записи из разных лент хранить и показывать отдельно (по названию ленты).
#
# Вгимание:
# После сдачи и визирования отчета принести его на лекцию (за 5 мин до начала)
# + Продублировать отчет и исходник(.zip, github и т.п.) письмом на isu

# https://habrahabr.ru/rss/interesting/

from datetime import datetime

import feedparser

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from flask import Flask, render_template, redirect, request

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/rss-parser"

mongo = PyMongo(app)

tapes_collection = mongo.db.tapes


@app.route('/', methods=['GET'])
@app.route('/tapes', methods=['GET'])
def handle_tapes():
    tapes = tapes_collection.find()

    return render_template('tapes.html', tapes=tapes)


@app.route('/tapes', methods=['POST'])
def handle_updating_tape():
    title = request.form['title']
    url = request.form['url']

    tape = {'title': title, 'url': url}

    if tapes_collection.find_one({'url': url}) is None:
        tape_id = tapes_collection.insert_one(tape).inserted_id
        update_records(tape_id)

    return redirect('/tapes')


@app.route('/tapes/<tape_id>/records', methods=['GET'])
def handle_records(tape_id):
    tape = tapes_collection.find_one({"_id": ObjectId(tape_id)})

    page = int(request.args.get('page')) if request.args.get('page') is not None else 0
    size = int(request.args.get('size')) if request.args.get('size') is not None else 10

    records = []
    pagination = {
        'page': page,
        'size': size,
        'total': 0
    }
    pages = []

    if tape is not None and 'records' in tape:
        records = tape['records']
        total = len(records)
        records = records if (page * size > total) else records[(page * size):(page * size + size)]
        pagination = {
            'page': page,
            'size': size,
            'total': total
        }

        i = 0
        page = 0
        while True:
            pages.append(page)
            page += 1
            i += size
            if i >= total:
                break

    return render_template('records.html', tape=tape, records=records, pagination=pagination, pages=pages)


@app.route('/tapes/<tape_id>/records', methods=['POST'])
def handle_records_updating(tape_id):
    update_records(tape_id)

    return redirect('/tapes/%s/records' % tape_id)


def update_records(tape_id):
    tape = tapes_collection.find_one({"_id": ObjectId(tape_id)})

    if tape is not None:
        feed = feedparser.parse(tape['url'])

        local_records = tape['records'] if 'records' in tape else []
        remote_records = feed['entries'] if 'entries' in feed else []

        merged_records_dict = {}

        for local_record in local_records:
            merged_records_dict[local_record['id']] = local_record
        for remote_record in remote_records:
            merged_records_dict[remote_record['id']] = remote_record

        merged_records = list(merged_records_dict.values())

        merged_records.sort(key=lambda record: datetime.strptime(record['published'], '%a, %d %b %Y %H:%M:%S %Z'),
                            reverse=True)

        tapes_collection.find_one_and_update(
            {"_id": ObjectId(tape_id)},
            {
                '$set': {
                    'records': merged_records
                }
            }
        )


if __name__ == '__main__':
    app.run(debug=True)
