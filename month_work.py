import redis
import time
from get_user_article import get_user_articles
import threading
import time

def copy_redis():
    r = redis.Redis('127.0.0.1','6379')
    r.sdiffstore('month_work_user','used_user','users')

def main():
    copy_redis()
    print('get user from redis')
    task_list = [threading.Thread(target = get_user_articles,kwargs = {'redis_set':'month_work_user','not_climb_depth':True,'check_date':True,'redis_increament_set': None}) for _ in range(10)]
    print('create tasks')
    for i in task_list:
        i.start()
    print('threading all start')
    for i in task_list:
        i.join()


if __name__ == '__main__':
    main()
