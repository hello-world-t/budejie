from public_func import get_response
import redis
import json
import threading
import pymongo
import random
import time
import datetime

def get_user_articles(redis_set = 'user_article',not_climb_depth = False,check_date = False, redis_increament_set = None):
    r = redis.Redis('127.0.0.1','6379')
    mongodb_client = pymongo.MongoClient(host='127.0.0.1',port=27017)
    mongodb_db = mongodb_client.budejie
    mongodb_table = mongodb_db.budejie_article
    print('redis_set is: {},not_climb_depth is: {},bool is: {},check_date is: {},bool is: {}'.format(redis_set,not_climb_depth,bool(not_climb_depth),check_date,bool(check_date)))
    while True:
        user_id = r.spop(redis_set)
        np = 0
        outdate_flag  = False
        if not user_id:
            time.sleep(random.randint(4,8))
            continue
        while True:
            url = 'http://d.api.budejie.com/topic/user-topic/{}/1/desc/baisishequ-win-1.0/{}-20.json'
            response = get_response(url.format(user_id.decode('utf-8'),np))
            try:
                result = json.loads(response.content)
            except Exception as e:
                print(response.content)
                input()
            
            np = result['info']['np']
            if not np:
                break
            for page in result['list']:
                value = {'user_id':user_id.decode('utf-8')}
                page_id = page['id']
                # 点赞数
                page_comment = page['comment']
                if int(page_comment) >=0 and not r.sismember('used_page',page_id):
                    r.sadd('used_page',page_id)
                    r.sadd('page',page_id) 
                up_count = page['up']
                article_text = page['text'].replace(' ','').replace('\n','')
                if int(up_count) <= 0 or '该内容已被删除' in article_text:
                    continue
                data = page['passtime'].split(' ')[0]
                if check_date and data < str(datetime.date.today()-datetime.timedelta(days=30)):
                    outdate_flag = True
                    continue
                if redis_increament_set:
                    r.sadd(redis_increament_set,user_id)
                print('up_count is: {}'.format(up_count))
                article_type = page['type']
                value.update({'page':page_id,'up_count':up_count,'article_type':article_type,'article_text':article_text})
                try:
                    hot_comment_list = [comment['content'].replace(' ','').replace('\n','') for comment in page['top_comments'] if comment['content'] != '']
                    value.update({'hot_comment':hot_comment_list})
                except Exception as e:
                    pass
                if article_type == 'image':
                    url = page['image']['big'][0]
                    value.update({'url':url})
                elif article_type == 'gif':
                    url = page['gif']['images'][0]
                    value.update({'url':url})
                elif article_type == 'video':
                    url = page['video']['download'][0]
                    value.update({'url':url})
                value.update({'is_download':'false'})
                try:
                    mongodb_table.insert_many([value])
                except Exception as e:
                    print(e)
                    continue

            if not_climb_depth or outdate_flag:
                break


def get_user_articles_main():
    article_tasks = [threading.Thread(target=get_user_articles) for _ in range(3)]
    
    for article_task in article_tasks:
        article_task.start()

    for article_task in article_tasks:
        article_task.join()

if __name__ == '__main__':
    get_user_articles()



