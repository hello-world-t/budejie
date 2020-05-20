from public_func import get_response
import redis
import json
import threading
import time
import random

def get_user_fans():
    r = redis.Redis('127.0.0.1','6379')

    follow_id = 0
    while True:
        user_id = r.spop('user_fans')
        if not user_id:
            time.sleep(random.randint(4,8))
            print('in get_user_fans')
            continue
        while True:
            url = 'http://api.budejie.com/api/api_open.php?a=fans_list&c=user&follow_id={}&userid={}'
            response = get_response(url.format(follow_id,user_id.decode('utf-8')))
            result = json.loads(response.content.decode('utf-8'))
            follow_id = result['data']['info']['follow_id']
            if follow_id == '0':
                break
            user_list = result['data']['list']
            for user in user_list:
                new_user_id = user['id']
                
                flag = r.sismember('used_user',new_user_id)
                if not flag:
                    r.sadd('used_user',new_user_id)
                    r.sadd('users',new_user_id)

def get_user_fans_main():

    fans_tasks = [threading.Thread(target=get_user_fans) for _ in range(13)]

    for fans_task in fans_tasks:
        fans_task.start()

    for fans_task in fans_tasks:
        fans_task.join()


if __name__ == '__main__':
    get_user_fans()
                
