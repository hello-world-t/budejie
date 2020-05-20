# -*- coding: UTF-8 -*-
from public_func import get_response
import redis
import json
import psycopg2
import threading
import time
import random

def get_user_detail():
    r = redis.Redis('127.0.0.1','6379')
    conn = psycopg2.connect(database = 'budejie', user = 'aaa', password = 'aaa',host = '127.0.0.1', port = 5432)
    cur = conn.cursor()
    count = 0
    while True:
        user_id = r.spop('users')
        if not user_id:
            print('in get_user_information')
            time.sleep(random.randint(4,8))
            continue
        url = 'http://api.budejie.com/api/api_open.php?a=profile&c=user&userid={}'
        count += 1
        try:
            response = get_response(url.format(user_id.decode('utf-8')))
            user_information = json.loads(response.content.decode('utf-8'))['data']
            user_article_num = user_information['tiezi_count']
            user_sex = user_information['sex']
            user_follow = user_information['follow_count']
            user_fans = user_information['fans_count']
            user_phone = user_information['phone']
            user_name = user_information['username'].strip()
            user_id = user_information['id']
            user_comment = user_information['comment_count']
            #user_share = user_information['share_count']

        except Exception as e:
            continue
        if 0 < int(user_fans):
            r.sadd('user_fans',user_id)
        
        if 0 < int(user_follow):
            r.sadd('user_follow',user_id)
        
        if 0 < int(user_article_num):
            r.sadd('user_article',user_id)
        
        # if 0 < int(user_share):
        #    r.sadd('user_share',user_id)
        
        if 0 < int(user_comment):
            r.sadd('user_comment',user_id)
        try:  
            if user_phone != '':
                cur.execute("insert into budejie_user (user_id,user_sex,user_phone,user_name,user_fans,user_article,is_download) values (%s,%s,%s,%s,%s,%s,%s);",(user_id,'女' if user_sex == 'f' else '男',user_phone,user_name,user_fans,user_article_num,'0'))
                print('user_id is: {},user_name is: {},user_sex is: {},user_phone is: {},user_comment is: {}'.format(user_id,user_name,user_sex,user_phone,user_comment))
            else:
                continue
        except Exception as e:
            print('insert error,user_id is: {}'.format(user_id))
            continue
        
        if count % 1 == 0:
            conn.commit()

    
    cur.close()
    conn.close()

def get_user_detail_main():
    
    information_tasks = [threading.Thread(target=get_user_detail) for _ in range(1)]

    for information_task in information_tasks:
        information_task.start()

    for information_task in information_tasks:
        information_task.join()

if __name__ == '__main__':
    get_user_detail()
