# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#     return "Hello, World!"
from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
# CORS(app)
from flask import Flask, render_template, request, make_response

import requests, json

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def home():
    trending_movie_url = "https://api.themoviedb.org/3/trending/movie/week?api_key=684641b6b7fea9789754590d86d5f685"
    trending_movie_json = requests.get(trending_movie_url).json()
    trending_movie_data = []
    for i in range(5):
        movie_dict = {'title_date': trending_movie_json["results"][i]['title'] + " (" +
                                    trending_movie_json["results"][i]['release_date'].split("-")[0] + ")",
                      'backdrop_path': 'http://image.tmdb.org/t/p/w780' + trending_movie_json["results"][i][
                          'backdrop_path'],

                      }
        trending_movie_data.append(movie_dict)
    airing_today_tv_url = "https://api.themoviedb.org/3/tv/airing_today?api_key=684641b6b7fea9789754590d86d5f685"
    airing_today_tv_json = requests.get(airing_today_tv_url).json()
    airing_today_tv_data = []
    for i in range(5):
        today_tv_dict = {'name_date': airing_today_tv_json["results"][i]['name'] + " (" +
                                      airing_today_tv_json["results"][i]['first_air_date'].split("-")[0] + ")",
                         'backdrop_path': 'http://image.tmdb.org/t/p/w780' + airing_today_tv_json["results"][i][
                             'backdrop_path'],
                         }
        airing_today_tv_data.append(today_tv_dict)
    if request.method == 'POST':
        keyword = request.form.get('keywordInput')
        category = request.form.get('categoryInput')
        print(keyword)
        print(category)

    return render_template('home.html', trending_movie_data=trending_movie_data,
                           airing_today_tv_data=airing_today_tv_data)


def get_genre(genreUrl):
    genre = requests.get(genreUrl).json()
    genreDict = {}
    for key in genre['genres']:
        genreDict[key['id']] = key['name']
    return genreDict


def get_genre_str(genreDict, genreArr):
    genreStr = ''
    for i in genreArr:
        genreStr += genreDict[i] + ', '
    return genreStr.strip(', ')


def process_data(result_json, category, movieGenreDict, tvGenreDict):
    result = {'result': []}
    if len(result_json['results']) == 0:
        return result
    # print(result_json['results'])
    for key in result_json['results']:

        result_dict = {'id': key['id']}
        if category == 'Movies':
            result_dict['name'] = key['title']
            if key['release_date'] == "":
                result_dict['date'] = 'N/A'
            else:
                result_dict['date'] = key['release_date'].split("-")[0]

            result_dict['catego'] = 'movie'
            genreDict = movieGenreDict
        elif category == 'TVShows':
            result_dict['name'] = key['name']
            if 'first_air_date' not in key.keys():
                result_dict['date'] = 'N/A'
            else:
                result_dict['date'] = key['first_air_date'].split("-")[0]

            result_dict['catego'] = 'tv'
            genreDict = tvGenreDict
        elif category == 'MoviesTV':
            if key['media_type'] == 'movie':
                result_dict['name'] = key['title']
                if 'first_air_date' not in key.keys():
                    result_dict['date'] = 'N/A'
                else:
                    result_dict['date'] = key['first_air_date'].split("-")[0]
                result_dict['catego'] = 'movie'
                genreDict = movieGenreDict
            elif key['media_type'] == 'tv':
                result_dict['name'] = key['name']
                if key['release_date'] == "":
                    result_dict['date'] = 'N/A'
                else:
                    result_dict['date'] = key['release_date'].split("-")[0]
                result_dict['catego'] = 'tv'
                genreDict = tvGenreDict
            else:
                continue

        if len(key['genre_ids']) == 0:
            result_dict['genre'] = 'N/A'
        else:
            result_dict['genre'] = get_genre_str(genreDict, key['genre_ids'])
        result_dict['date_genre'] = result_dict['date'] + ' | ' + result_dict['genre']
        if key['overview'] == "":
            result_dict['overview'] = 'N/A'
        else:
            result_dict['overview'] = key['overview']
        # print(result_dict['poster_path'])
        if key['poster_path'] is None:
            result_dict['poster_path'] = 'https://cinemaone.net/images/movie_placeholder.png'
        else:
            result_dict['poster_path'] = 'http://image.tmdb.org/t/p/w185' + key['poster_path']
        if key['vote_average'] is None:
            result_dict['vote_average'] = 'N/A'
        else:
            result_dict['vote_average'] = str(float(key['vote_average']) / 2) + '/5'
        if key['vote_count'] is None:
            result_dict['vote_count'] = 'N/A'
        else:
            result_dict['vote_count'] = str(key['vote_count']) + ' votes'
        result['result'].append(result_dict)
        # print(result)
    return result


@app.route('/search', methods=['post', 'get'])
def search():
    # print("Fetching data...")
    keywordInput = request.args.get('keywordInput')
    categoryInput = request.args.get('categoryInput')
    # print(keywordInput, categoryInput)
    movieGenreDict = get_genre(
        'https://api.themoviedb.org/3/genre/movie/list?api_key=684641b6b7fea9789754590d86d5f685&language=en-US')
    tvGenreDict = get_genre(
        'https://api.themoviedb.org/3/genre/tv/list?api_key=684641b6b7fea9789754590d86d5f685&language=en-US')

    if categoryInput == 'Movies':
        searchUrl = 'https://api.themoviedb.org/3/search/movie?api_key=684641b6b7fea9789754590d86d5f685&query=' + keywordInput + '&lan guage=en-US&page=1&include_adult=false'
        result_json = json.loads(requests.get(searchUrl).content)
        # print(result_json)
        result = process_data(result_json, 'Movies', movieGenreDict, tvGenreDict)

    elif categoryInput == 'TVShows':
        searchUrl = 'https://api.themoviedb.org/3/search/tv?api_key=684641b6b7fea9789754590d86d5f685&language=en-US&page=1&query=' + keywordInput + '&include_adult=false'
        result_json = json.loads(requests.get(searchUrl).content)
        result = process_data(result_json, 'TVShows', movieGenreDict, tvGenreDict)
    elif categoryInput == 'MoviesTV':
        searchUrl = 'https://api.themoviedb.org/3/search/multi?api_key=684641b6b7fea9789754590d86d5f685&language=en-US&query=' + keywordInput + '&page=1&include_adult=false'
        result_json = json.loads(requests.get(searchUrl).content)
        result = process_data(result_json, 'MoviesTV', movieGenreDict, tvGenreDict)
    # print(result)
    return json.dumps(result)


@app.route('/show', methods=['post', 'get'])
def show_more_movie():
    html = ''
    result = {}
    category = request.args.get('category')
    id = str(request.args.get('id'))
    showUrl = 'https://api.themoviedb.org/3/' + category + '/' + id + '?api_key=684641b6b7fea9789754590d86d5f685&language=en-US'
    # print(showUrl)
    showJson = json.loads(requests.get(showUrl).content)
    showCastUrl = 'https://api.themoviedb.org/3/' + category + '/' + id + '/credits?api_key=684641b6b7fea9789754590d86d5f685&language=en-US'
    showCastJson = json.loads(requests.get(showCastUrl).content)
    showReviewUrl = 'https://api.themoviedb.org/3/' + category + '/' + id + '/reviews?api_key=684641b6b7fea9789754590d86d5f685&language=en-US&page=1'
    showReviewJson = json.loads(requests.get(showReviewUrl).content)
    # print(showJson)
    result['id'] = showJson['id']
    if category == 'movie':
        result['title'] = showJson['title']
        if showJson['release_date'] == "":
            result['date'] = 'N/A'
        else:
            result['date'] = showJson['release_date'].split("-")[0]
    else:
        result['title'] = showJson['name']
        if showJson['first_air_date'] == "":
            result['date'] = 'N/A'
        else:
            result['date'] = showJson['first_air_date'].split("-")[0]
    if showJson['overview'] == "":
        result['overview'] = 'N/A'
    else:
        result['overview'] = showJson['overview']
    if len(showJson['spoken_languages']) == 0:
        result['spoken_languages'] = 'N/A'
    else:
        result['spoken_languages'] = showJson['spoken_languages'][0]['english_name']
    if showJson['vote_average'] is None:
        result['vote_average'] = 'N/A'
    else:
        result['vote_average'] = str(float(showJson['vote_average']) / 2) + '/5'
    if showJson['vote_count'] is None:
        result['vote_count'] = 'N/A'
    else:
        result['vote_count'] = str(showJson['vote_count']) + ' votes'
    # result['poster_path'] = showJson['poster_path']
    if showJson['backdrop_path'] is None:
        result['backdrop_path'] = 'https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/movie-placeholder.jpg'
    else:
        result['backdrop_path'] = 'http://image.tmdb.org/t/p/w780' + showJson['backdrop_path']
    if len(showJson['genres']) == 0:
        result['genres'] = 'N/A'
    else:
        strgen = ''
        for key in showJson['genres']:
            strgen += key['name'] + ','
        result['genres'] = strgen.strip(', ')
    result['url'] = 'https://www.themoviedb.org/' + category + '/' + id
    html += '<div id="popInfo">'

    html += '  <div id="largeImg"><img src="' + result[
        'backdrop_path'] + '"></div><div id="popTitle"><div id="popTitleInfo">'
    html += result['title']
    html += '</div><div id="popTitleLink"><a href="' + result['url'] + '" target=_blank>&#9432;</a>'
    html += '</div></div><div id="popDateType">' + result['date'] + ' | ' + result['genres']
    html += '</div><div id="popRateVote"><div id="popRate">&#9733;' + result['vote_average']
    html += '</div><div id="popVote">' + result['vote_count']
    html += '</div></div><div id="popTntro">'
    html += result['overview']
    html += '</div><div id="speakLanguage">Spoken Languages:' + result['spoken_languages']
    html += '</div></div>'
    html += '<div id="popCast"><div id="castWord">Cast</div>'
    i = 0
    # print(len(showCastJson['cast']))
    while (i < 8) and (i < len(showCastJson['cast'])):
        # print("================in================")
        key = showCastJson['cast'][i]
        if key['profile_path'] is None:
            casturl = 'https://bytes.usc.edu/cs571/s21_JSwasm00/hw/HW6/imgs/person-placeholder.png'
        else:
            casturl = 'http://image.tmdb.org/t/p/w185' + key['profile_path']
        html += '<div class="actor"><div class="actorImg"><img src="' + casturl + '"></div><div class ="actorName">'
        html += key['original_name'] + '</div><div class ="as"> AS </div> <div class ="actorRole">' + key[
            'character'] + '</div></div>'
        i += 1
    html += '</div> <div id="popReview"> <div id="popReviewTitle">Reviews</div>'
    j = 0
    # print(html)
    while (j < 5) and (j < len(showReviewJson['results'])):
        k = showReviewJson['results'][j]
        username = k["author_details"]['username']

        created_at = k['created_at'].split("-")[1] + '/' + k['created_at'].split("-")[2][:2] + '/' + \
                     k['created_at'].split("-")[0]
        content = k['content']

        if 'rating' not in k.keys():
            rating = ''
        else:
            rating = str(float(k['rating']) / 2) + '/5'
        html += '<div class="review"> <div class="reviewrNameDate"><b>' + username + '</b>' + ' on ' + created_at + '</div>'
        if rating != '':
            html += '<div class="reviewRate">&#9733;' + rating + '</div>'
        html += '<div class="reviewContent">' + content + '</div><div class="greyLine"></div></div>'
        j += 1
    html += '</div>'
    # print(html)
    return html


if __name__ == '__main__':
    app.run(debug=True)
