from public_func import get_page
from get_history import analysis_history
import redis
import time

def get_home_page():
    r = redis.Redis('127.0.0.1','6379')
    for url in ['http://www.budejie.com/{}']:
        for i in range(1,51):
            page = get_page(url.format(i))
            analysis_history(page)
            try:
                div_list = page.xpath('//div[@class="u-img"]/a/@href')
                user_id_list = [i[:-5].split('-')[1] for i in div_list]
            except Exception as e:
                continue
            for i in user_id_list:
                flag = r.sismember('used_user',i)
                if not flag:
                    r.sadd('used_user',i)
                    r.sadd('users',i)


if __name__ == '__main__':
    get_home_page()
