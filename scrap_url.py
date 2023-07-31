from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print(str(e))


def is_good_response(resp):
    content_type = resp.headers['content-type'].lower()
    return (resp.status_code == 200 and
            content_type is not None and
            content_type.find('html') > -1)


def app(url):
    raw_html = simple_get(url)
    len(raw_html)
    try:
        utf_html = raw_html.decode('utf-8')
    except UnicodeDecodeError as e:
        print('cannot decode website', e)
        sys.exit(1)
    html = BeautifulSoup(utf_html, 'html.parser')
    for link in html.find_all('a'):
        print(link.get('href'))

    for link in html.find_all('script'):
        if link.get('src') is not None:
            print(link.get('src'))

    for link in html.find_all('link'):
        if link.get('href') is not None:
            print(link.get('href'))

    for link in html.find_all('iframe'):
        if link.get('src') is not None:
            print(link.get('src'))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: scrapurl.exe <url>")
        sys.exit(1)
    app(sys.argv[1])

