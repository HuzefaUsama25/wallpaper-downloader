#!/bin/python3

import requests
from bs4 import BeautifulSoup as bs4
from multiprocessing import Pool
from fake_headers import Headers
import random
import time


def get_random_header():
    return header.generate()


def write_to_file(res):
    with open("index.html", "wb") as f:
        f.write(res)




def get_wallpapers_list_on_query(query):
    response = requests.get(f"https://wallhaven.cc/search?q={query}&resolutions=1920x1080&sorting=relevance", headers = get_random_header()).content
    write_to_file(response)
    soup = bs4(response, "html.parser")

    
    wallpapers = []
    for img_thumb in soup.select("#thumbs > section > ul > li > figure > img"):
        img_thumb_url = img_thumb.get("data-src")
        img_info = img_thumb_url.split("/")[-1].split(".")
        img_id = img_info[0]
        img_ext = img_info[1]
        url = f"https://w.wallhaven.cc/full/{img_id[:2]}/wallhaven-{img_id}.{img_ext}"
        print(url)
        wallpapers.append(url)
    return wallpapers


def download_wallpaper(url):
    time.sleep(int(random.randrange(2,10)))
    image_id = url.split("/")[-1]
    local_filename = image_id 
    with requests.get(url, stream=True, headers = get_random_header()) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=3000):
                f.write(chunk)
    return local_filename



def download_wallpapers(wallpaper_urls):
    pool = Pool(processes=len(wallpaper_urls))
    pool.map(download_wallpaper, wallpaper_urls)
    

def main():
    query = input("pls enter a query: ")
    wall_urls = get_wallpapers_list_on_query(query)
    print(f"urls = {wall_urls}")
    download_wallpapers(wall_urls)


if __name__=="__main__":
    header = Headers(headers=False)
    main()

