
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

def get_movie_titles(doc):
    movie_title_tags = doc.find_all('a', class_ ='text--bold palewhite title')
    movie_titles = []
    for tag in movie_title_tags:
        movie_titles.append(tag.text)
    return movie_titles


def get_movie_years(doc):
    movie_year_tags = doc.find_all('span', class_ = 'text--gray year')
    movie_years =[]
    for tag in movie_year_tags:
        movie_years.append(tag.text)
    return movie_years


def get_movie_genres(doc):
    genre_tags = doc.find_all('h4', class_ = 'genre')
    movie_genres = []
    for tag in genre_tags:
        movie_genres.append(tag.text)
    return movie_genres


def get_movie_ratings(doc):
    rating_tags= doc.find_all('h4', class_ = 'rating')
    movie_ratings = []
    for tag in rating_tags:
        movie_ratings.append(tag.text)
    return movie_ratings


def get_movie_urls(doc):
    try:
        movie_url_tags = doc.find_all('a', class_ ='text--bold palewhite title')
        movie_urls = []
        base_url = 'https://yts.rs'
        for tag in movie_url_tags:
            movie_urls.append(base_url + tag['href'])
        return movie_urls
    except Exception as e:
        print(e)
        return ['']


def get_synopsis(tags):
    synopses =[]
    for div_tag in tags:
        try:
            p_tags = div_tag[0].find_all('p')
            synopsis = p_tags[0].text
            synopses.append(synopsis)
        except Exception as e:
            print(e)
            print(f'Error while extracting synopses')
            synopses.append('')
    return synopses


def get_tags(urls):
    tags = []
    for url in urls:
        try:
            movie_doc = get_doc(url)
            div_tag = movie_doc.find_all('div', class_ = 'synopsis col-sm-10 col-md-13 col-lg-12')
            tags.append(div_tag)
        except Exception as e:
            print(e)
            print('Error while collecting div tags')
            tags.append(None)
    return tags

def get_downloaded(tags):
    downloadeds = []
    for div_tag in tags:
        try:
            if not div_tag:
                downloadeds.append('')
                continue
            p_tags = div_tag[0].find_all('p')
            em_tag = p_tags[1].find_all('em')
            download = em_tag[0].text
            regex = re.compile('[^0-9]')
            downloaded = regex.sub('',download)
            downloadeds.append(downloaded)
        except Exception as e:
            print(e)
            print(f'Error while extracting downloads')
            downloadeds.append('')
    return downloadeds


def get_doc(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc


def scrap_page(url):
    doc = get_doc(url)
    movies,years,genres,ratings,urls,synopses,downloadeds=[],[],[],[],[],[],[]
    movies = get_movie_titles(doc)
    years = get_movie_years(doc)
    genres = get_movie_genres(doc)
    ratings = get_movie_ratings(doc)
    urls = get_movie_urls(doc)
    tags = get_tags(urls)
    synopses = get_synopsis(tags)
    downloadeds = get_downloaded(tags)
    return movies,years,genres,ratings,urls,synopses,downloadeds


def get_start():
    try:
        read_status_file = open('status.txt', 'r')
        text = read_status_file.read()
        read_status_file.close()
        start = int(text)
        return start
    except Exception as e:
        print(e)
        return 0

def save_end(i):
    try:
        status_file = open('status.txt', 'w')
        status_file.seek(0)
        status_file.write(f'{i}\n')
        print(f'Scraping {i}')
        status_file.close()
    except Exception as e:
        print(e)


def website_scrap():
    all_movies,all_years,all_genres,all_ratings,all_urls,all_synopses,all_downloadeds = [],[],[],[],[],[],[]
    start = get_start()
    for i in range(start + 1, start + 50):
        save_end(i)
        url = 'https://yts.rs/browse-movies?page={}'.format(i)
        try:
            movies,years,genres,ratings,urls,synopses,downloadeds = scrap_page(url)
            movies_dict = {
                'Movie': movies,
                'Year': years,
                'Genre': genres,
                'Rating': ratings,
                'Url': urls,
                'Synopsis': synopses,
                'Downloads': downloadeds
            }
            movies_df = pd.DataFrame(movies_dict, index = None) # Creates a dataframe from the dictionary and saves it to 'movies_df'
            movies_df.to_csv(f'movies_data_{i}.csv') # Converts the Dataframe file 'movies_df' to a csv file and saves it in .csv format
        except Exception as e:
            print(e)
            print(f'Page {i} could not be scraped')


website_scrap()
