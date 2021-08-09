import os
import requests
import re 
import yake
from flask import Flask, request



gMap = {
    "Acoustic Blues":1210,
    "Chicago Blues": 1007,
    "Blues": 2,
    "Rap": 18,
}

search_baseUrl ='http://api.musixmatch.com/ws/1.1/track.search?'
lyrics_baseURL = 'http://api.musixmatch.com/ws/1.1/track.lyrics.get?'

def get_five_words(lyrics,language):
    max_ngram_size = 3
    deduplication_threshold = 0.9
    numOfKeywords = 5
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(lyrics)
    return [x[0] for x in keywords]

def get_tracks(category,songno,alreadyplayed,token):
    if songno == 0:
        response = requests.get(
            search_baseUrl+ f'f_has_lyrics=1&f_music_genre_id={gMap[category]}&page=1&page_size=2&apikey={token}'
        ).json()
        return response
    else:
        tries = 0
        track_ids = alreadyplayed[0].split(',')
        lyrics = requests.get(
            lyrics_baseURL+ f'track_id={track_ids[-1]}&apikey={token}'
        ).json().get('message').get('body').get('lyrics')
        keywords = get_five_words(lyrics.get('lyrics_body'),lyrics.get('lyrics_language','en'))

        while tries > 3:
            response = requests.get(
                search_baseUrl+ f'f_has_lyrics=1&f_music_genre_id={gMap[category]}&page=1&page_size=1&q_lyrics={keywords}&apikey={token}'
            ).json()
            print(response.get('message').get('body').get("track_list")[0].get("track_id") )
            if response.get('message').get('body').get("track_list")[0].get("track_id") in track_ids:
                tries+=1
            else:
                return response
        return "Run out of Tracks", 400
    

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/playlist', methods=['GET'])
    def get_songs():
        if request.method == 'GET':
            category = request.args.get('category', default = '*', type = str)
            songno = request.args.get('songno', default = 0, type = int)
            alreadyplayed = request.args.getlist("alreadyplayed")
            token = request.args.get('token', default = '*' ,type = str)
            return get_tracks(category,songno,alreadyplayed,token)
        else:
            return "Bad Request", 400

    return app