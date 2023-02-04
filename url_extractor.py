# -*- coding: utf-8 -*-
import sys
import requests
from threading import Thread
from bs4 import BeautifulSoup
from pprint import pprint
import concurrent.futures
from retrying import retry

# band_url = sys.argv[1]


def get_page(url):
    response = requests
    page = response.get(url).content.decode('utf-8')
    if response.status_codes == 404:
        print("Site %s does not exist" % url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup


albums = get_page('http://www.darklyrics.com/h/helloween.html').findAll(
    "div", {"class": "album"})
albums_link_list = []
for album in albums:
    albums_link_list.append(album.a['href'].replace('..',
                                                    '').replace('#1', ''))

albums_urls = []
for album_link in albums_link_list:
    albums_urls.append('http://www.darklyrics.com' + album_link)


def retry_if_connection_error(exception):
    """ Specify an exception you need. or just True"""
    #return True
    return isinstance(exception, ConnectionError)


excluded_chars = [
    "[", "]", "HELLOWEEN LYRICS", ": guitar", ": bass", "Produced on",
    "Executive producer", ": drums", "for correcting track",
    "corrections are welcomed", "@darklyrics", "lead guitar"
]


@retry(retry_on_exception=retry_if_connection_error, wait_fixed=2000)
def write_files(album_link):
    print(album_link)
    response = requests
    page = response.get(album_link).content.decode('utf-8')
    print(page)
    # soup = BeautifulSoup(page, 'html.parser')
    # lyrics = soup.select('.lyrics')
    # for lyric in lyrics:
    #     lyric_lines = lyric.text.split("\n")
    #     filtered_lyric_lines = [
    #         s for s in lyric_lines
    #         if not any(char in s for char in excluded_chars)
    #     ]
    #     final_lyrics = [s for s in filtered_lyric_lines if s != ""]
    #     file_name = album_link.replace(
    #         "http://www.darklyrics.com/lyrics/helloween/", "")
    #     file_name = file_name.replace(".html", ".txt")
    # with open("albums.txt", 'a') as f:
    #     for line in final_lyrics:
    #         f.write(line)
    #         f.write('\n')


with concurrent.futures.ThreadPoolExecutor() as exector:
    exector.map(write_files, albums_urls)
