import uuid
import random
import urllib.request
import re

import werkzeug
from bs4 import BeautifulSoup

from flask import Flask, render_template, redirect, request

file = open('guess.txt', 'rt')
file_content = file.read()
file.close()

names = file_content.split('\n')

games_store = {}
app = Flask(__name__)


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


def get_random_name(level):
    if level == '1':
        return names[random.randint(0, 10)]
    if level == '2':
        return names[random.randint(0, 50)]
    if level == '3':
        return names[random.randint(0, 99)]


@app.route('/', methods=['GET'])
@app.route('/games', methods=['GET'])
def handle_start():
    return render_template('start.html')


@app.route('/games', methods=['POST'])
def handle_new_game():
    global names
    global games_store

    game_uuid = str(uuid.uuid4())

    games_store[game_uuid] = {
        'level': request.form['level']
    }

    games_store[game_uuid]['answer'] = get_random_name(games_store[game_uuid]['level'])
    games_store[game_uuid]['options'] = [
        get_random_name(games_store[game_uuid]['level']),
        get_random_name(games_store[game_uuid]['level']),
        get_random_name(games_store[game_uuid]['level']),
        get_random_name(games_store[game_uuid]['level'])
    ]

    options_count = len(games_store[game_uuid]['options'])

    games_store[game_uuid]['options'][random.randint(0, options_count - 1)] = games_store[game_uuid]['answer']

    query = '+'.join(games_store[game_uuid]['answer'].split())
    url = "https://www.google.ru/search?site=&tbm=isch&source=hp&biw=1600&bih=1600&q={0}&oq={0}".format(query)
    header = {'User-Agent': 'Mozilla/5.0'}
    soup = get_soup(url, header)

    images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]

    images_count = len(images)

    games_store[game_uuid]['images'] = [
        images[random.randint(0, images_count - 1)],
        images[random.randint(0, images_count - 1)],
        images[random.randint(0, images_count - 1)]
    ]

    return redirect('/games/%s' % game_uuid)


@app.route('/games/<game_uuid>', methods=['GET'])
def handle_game(game_uuid):
    global games_store

    current_game = games_store[game_uuid]
    options = current_game['options']
    images = current_game['images']

    return render_template('game.html', game_uuid=game_uuid, options=options, images=images)


@app.route('/games/<game_uuid>', methods=['POST'])
def handle_game_answer(game_uuid):
    global games_store

    current_game = games_store[game_uuid]
    level = current_game['level']
    options = current_game['options']
    images = current_game['images']
    answer = current_game['answer']

    try:
        user_answer = request.form['answer_choice']
        message = 'Правильно!' if answer == user_answer else 'Неправильно'
    except werkzeug.exceptions.BadRequestKeyError:
        message = 'Выберите вариант ответа'

    return render_template('game.html', game_uuid=game_uuid, options=options, images=images, level=level, message=message)


if __name__ == '__main__':
    app.run(debug=True)
