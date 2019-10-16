from numpy import genfromtxt
import pandas as pd
import csv
import urllib.request
import datetime

def normalise_line(line):
    words = line.split('"')
    if len(words) > 1:
        return words[0][:-1]+'^'+words[1]+'^'+words[2][1:]
    else:
        words = line.split(',')
        return words[0]+'^'+words[1]+'^'+words[2]

def get_imdb_url(number):
    diff = 7 - len(str(number))
    return 'https://www.imdb.com/title/tt' + ('0' * diff) + str(number)

def get_tmdb_url(number):
    return 'https://www.themoviedb.org/movie/' + str(number)

def get_rank_from_imdb_html(html):
    lines = html.split('\n')
    for line in lines:
        if "<span itemprop=\"ratingValue\">" in line:
            trim_left = line.split('<span itemprop=\"ratingValue\">')[1]
            trim_right = trim_left.split('</')[0]
            return float(trim_right)

def get_rank_from_tmdb_html(html):
    lines = html.split('\n')
    for line in lines:
        if "<span class=\"icon icon-" in line:
            trim_left = line.split('icon icon-r')[1]
            trim_right = trim_left.split('\">')[0]
            return float(trim_right)/10

def get_html_for_url(url):
    try:
       fp = urllib.request.urlopen(url)
    except:
        return None
    mybytes = fp.read()
    result = mybytes.decode("utf8")
    fp.close()
    return result

if __name__ == '__main__':
    # movies = []
    # movies.append({'movieId':1, 'title': dupa, ''})
    # with open('movies.csv') as file:
    #     output_file = open("movies_normalised.csv", "w+")
    #     for line in file:
    #         # print(normalise_line(line))
    #         output_file.write(normalise_line(line))
    # <span itemprop="ratingValue">5.8</span>
    movies_df = pd.read_csv('movies_normalised.csv', sep='^')
    links_df = pd.read_csv('links.csv')
    df = pd.merge(movies_df,
                      links_df,
                      on='movieId')

    print(df['title'])
    print(df['imdbId'])
    print(min(df['imdbId']))
    print(max(df['imdbId']))
    url = get_imdb_url(213)

    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    df['imdbRank'] = 0.0
    df['tmdbRank'] = 0.0
    print(get_rank_from_imdb_html(mystr))
    for i in range(5):
        print(df['title'][i])
        print(get_imdb_url(df['imdbId'][i]))
        my_html = get_html_for_url(get_imdb_url(df['imdbId'][i]))
        imdb_rank = get_rank_from_imdb_html(my_html)
        print(imdb_rank)
        df['imdbRank'][i] = imdb_rank
        my_html = get_html_for_url(get_tmdb_url(df['tmdbId'][i]))
        tmdb_rank = get_rank_from_tmdb_html(my_html)
        print(tmdb_rank)
        df['tmdbRank'][i] = tmdb_rank
        print("---------------------------------")

    print(df[0:5])
    print("That was demo for IMDb, now scrap tmdb")
    begin_time = datetime.datetime.now()
    df_len = len(df['title'])
    for i in range(df_len):
        print("idx: " + str(i))
        print(df['title'][i])
        print(get_tmdb_url(df['tmdbId'][i]))
        my_html = get_html_for_url(get_tmdb_url(df['tmdbId'][i]))
        if(my_html == None):
            tmdb_rank = -1
        else:
            tmdb_rank = get_rank_from_tmdb_html(my_html)
        print(tmdb_rank)
        df['tmdbRank'][i] = tmdb_rank
        now = datetime.datetime.now()
        if i > 0:
            pr = (i*100/df_len)
            time_passed = now-begin_time
            time_left = ((100-pr)*time_passed)/pr
            print("PROGRESS: "+str(i)+"/"+str(df_len)+". It is "+str(pr)+"% of all data. Time passed " + str(time_passed)+". Estimated time left: "+str(time_left))
        print("---------------------------------")

    df.to_csv('movies_with_ratings.csv', sep='^')
