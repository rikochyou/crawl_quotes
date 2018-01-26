# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<span.*?text">(.*?)</span>.*?author">(.*?)</small>',re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield{
            'content':item[0],
            'author':item[1]
        }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()

def main(page_num):
    url = "http://quotes.toscrape.com/page/"+str(page_num)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == "__main__":
    '''for i in range(0,10):
        main(i)'''
    pool = Pool()
    pool.map(main, [i for i in range(0,10)])

