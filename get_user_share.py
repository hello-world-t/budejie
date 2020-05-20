from public_func import get_response
import redis
import json
import threading

def get_share_article():
    r = redis.Redis('127.0.0.1','6379')

    np = 0
    while True:
        user_id = r.spop('user_share')

        if not user_id:
            print('in get_share_article')
            continue

        while True:
            url = 'http://d.api.budejie.com/topic/share-topic/{}/baisishequ-iphone-8.0/{}-20.json'
            response = get_response(url.format(user_id.decode('utf-8'),np))
            result = json.loads(response.content)
            
            np = result['info']['np']
            if not np:
                np = 0
                break
            np = int(np)
            for page in result['list']:
                page_id = page['id']
                page_up = page['up']

                flag = r.sismember('used_page',page_id)
                if not flag:
                    r.sadd('used_page',page_id)
                    r.sadd('page',page_id)


def get_share_article_main():
    share_tasks = [threading.Thread(target=get_share_article) for _ in range(1)]
    
    for share_task in share_tasks:
        share_task.start()

    for share_task in share_tasks:
        share_task.join()
