from public_func import get_response
import redis
import json
import threading
import time
import random

def get_comment_article():
    r = redis.Redis('127.0.0.1','6379')

    np = 0
    while True:
        user_id = r.spop('user_comment')
        
        if not user_id:
            time.sleep(random.randint(4,8))
            print('in get_comment_article')
            continue
        while True:
            url = 'http://d.api.budejie.com/comment/user-comment/{}/baisishequ-iphone-8.0/{}-20.json'
            response = get_response(url.format(user_id.decode('utf-8'),np))
            result = json.loads(response.content)

            np = result['info']['np']

            if not np:
                np = 0
                break
            np = int(np)

            for page in result['list']:
                page_id = page['topic']['id']
                #page_up = page['topic']['up']
                page_comment = page['topic']['comment']

                flag = r.sismember('used_page',page_id)
                if int(page_comment) >0 and not flag:
                    r.sadd('used_page',page_id)
                    r.sadd('page',page_id)


def get_comment_article_main():
    comment_tasks = [threading.Thread(target=get_comment_article) for _ in range(1)]

    for comment_task in comment_tasks:
        comment_task.start()

    for comment_task in comment_tasks:
        comment_task.join()
    
