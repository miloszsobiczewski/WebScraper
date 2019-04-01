from WebScraper.settings import STATIC_URL
from bs4 import BeautifulSoup
from urllib3 import PoolManager
import urllib.request
import requests
from os import path, system


def get_conn(url):
    """
    Try to connect to url, return True if success
    :param url:
    :return:
    """
    try:
        request = requests.get(url)
        if request.status_code == 200:
            res = True
        else:
            res = False
    except:
        res = False
    return res


def make_soup(url):
    """
    get BeautifulSoup object
    :param url:
    :return:
    """
    if get_conn(url):
        # get url response object
        http = PoolManager()
        html = http.request('GET', url).data
        # make soup
        return BeautifulSoup(html)
    else:
        raise Exception("Page doesn't exist!")


def get_txt(url):
    """
    Get text from given url.
    :param url:
    :return: scraped text
    """
    soup = make_soup(url)

    # remove scripts and styling
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    text = soup.get_text()

    # clean data
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def save_txt(file_name, url, subdir=''):
    """
    Save scraped text to .txt file
    :param file_name:
    :param url:
    :param subdir:
    :return:
    """
    text = get_txt(url)
    create_subdir('static/api/', subdir)
    try:
        with open(file_name, "w") as text_file:
            print(text, file=text_file)
        res = True
    except:
        res = False
    return res


def get_images(url):
    """
    Look for images for given url
    :param url:
    :return: found images links
    """
    soup = make_soup(url)
    # this makes a list of bs4 element tags
    images = [img for img in soup.findAll('img')]
    print(str(len(images)) + " images found.")
    # compile our unicode list of image links
    image_links = [each.get('src') for each in images]
    # clean list
    image_links = [each for each in image_links if each is not None]
    # specific for test site
    if len(image_links) > 0 and image_links[0][:4] != 'http':
        links = [url + link for link in image_links]
    else:
        links = image_links
    return links


def save_img(url, subdir=''):
    """
    save found images
    :param url:
    :param subdir:
    :return: operation status, list of saved images
    """
    links = get_images(url)
    create_subdir('static/api/', subdir)

    if len(links) > 0:
        images = [STATIC_URL[1:] + 'api/' + subdir +
                  img.split('/')[-1] for img in links]
        try:
            print('Downloading images to current working directory.')
            for i in range(len(links)):
                urllib.request.urlretrieve(links[i],
                     STATIC_URL[1:] + 'api/' + subdir +
                                           images[i].split('/')[-1])
            res = True
        except:
            res = False
    else:
        res = True
        images = []
    return res, images


def create_subdir(dir, subdir):
    if path.isdir(dir + subdir) is False and subdir != '':
        system('mkdir ' + dir + '/' + subdir)
