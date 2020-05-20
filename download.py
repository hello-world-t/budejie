import pymongo
from public_func import get_response
from threading import Lock
import os
import time
import threading
import redis
import pickle


def get_mongodb():
    mongodb_client = pymongo.MongoClient(host='127.0.0.1',port=27017)
    mongodb_db = mongodb_client.budejie
    mongodb_table = mongodb_db.budejie_article
    return mongodb_table

def download_file(thread_id, total_result):
    page_list = []
    id_result_list = []
    for key,value in total_result.items():
        base_path = '/root/budejie_dir/{}'.format(key)
        skip_num = thread_id*value
        mongodb_table = get_mongodb()
        file_result = mongodb_table.find({'article_type':key}).limit(value).skip(skip_num)
        file_result = [i for i in file_result if i['is_download'] == 'false']
        id_result = [result.pop('_id') for result in file_result]
        for i in range(1,len(file_result)+1,100):
            dir_name = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time()))
            file_path = base_path+ '/'+dir_name+'-{}-{}'.format(thread_id,i)
            status = os.system(' touch {}'.format(file_path))
            print('file_path is: {}'.format(file_path))
            with open(file_path,'wb') as f:
                pickle.dump(file_result[i:i+100],f)
            time.sleep(1)

        for id_name in id_result:
            mongodb_table.update({'_id':id_name,{$set:{'is_download':'true'}}})

        
    return

def get_task_total():
    mongodb_table = get_mongodb()
    mongo_result = mongodb_table.aggregate([{'$group':{'_id':"$article_type",'num':{'$sum':1}}}])
    result = {}
    for i in mongo_result:
        result[i['_id']] = i['num'] // 1000 * 1000 //10

    return result

def main():
    total_result = get_task_total()
    print(total_result)


    task_list = [threading.Thread(target=download_file,args=(i,total_result)) for i in range(10)]
    
    for i in task_list:
        i.start()

    for i in task_list:
        i.join()

if __name__ == '__main__':
    main()

