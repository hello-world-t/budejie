import redis

def analysis_history(page):
    r = redis.Redis('127.0.0.1','6379')
    page_list = page.xpath('//div[@class="j-list-c"]//a/@href')
    page_list = [i.split('-')[1].split('.')[0] for i in page_list if "detail" in i]
    page_list = set(page_list)
    for page_id in page_list:
        if not r.sismember('used_page',page_id):
            r.sadd('used_page',page_id)
            r.sadd('page',page_id)

    
