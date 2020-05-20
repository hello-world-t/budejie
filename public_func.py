import requests
import json
from lxml import etree

def get_response(url):
    headers = headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

    response = requests.get(url,headers=headers)

    return response

    
def get_page(url):
    response = get_response(url)
    page = etree.HTML(response.content)
    return page

if __name__ == '__main__':
    print(get_response('http://www.budejie.com').content)
