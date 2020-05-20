from public_func import get_response
import redis
import json
import threading
import time
import random

def get_user_from_page_comment():
    r = redis.Redis('127.0.0.1','6379')

    page = 0
    while True:
        page_id = r.spop('page')

        if not page_id:
            print('in get_user_from_page_comment')
            time.sleep(random.randint(5,10))
            continue

        while True:
            url = 'http://api.budejie.com/api/api_open.php?a=datalist&per=5&c=comment&hot=0&appname=www&client=www&device=pc&data_id={}&page={}'
            response = get_response(url.format(page_id.decode('utf-8'),page))
            result = json.loads(response.content)
            if not result:
                page = 1
                break
            page += 1
            for user in result['data']:
                user_id = user['user']['id']
                
                flag = r.sismember('used_user',user_id)
                if not flag:
                    r.sadd('used_user',user_id)
                    r.sadd('users',user_id)


def get_user_from_page_comment_main():
    page_tasks = [threading.Thread(target=get_user_from_page_comment) for _ in range(1)]

    for page_task in page_tasks:
        page_task.start()

    for page_task in page_tasks:
        page_task.join()
