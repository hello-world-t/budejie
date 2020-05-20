from get_user_information import get_user_detail_main
from get_user_fans import get_user_fans_main
from home_page import get_home_page
from get_follow import get_user_follows_main
from get_user_article import get_user_articles_main
from get_user_comment import get_comment_article_main
from get_user_from_page import get_user_from_page_comment_main
import threading

def main():
    get_home_page()
    t_1 = threading.Thread(target=get_user_detail_main)
    t_2 = threading.Thread(target=get_user_fans_main)
    t_3 = threading.Thread(target=get_user_follows_main)
    t_4 = threading.Thread(target=get_user_articles_main)
    t_6 = threading.Thread(target=get_comment_article_main)
    t_7 = threading.Thread(target=get_user_from_page_comment_main)

    t_1.start()
    t_2.start()
    t_3.start()
    t_4.start()
    t_6.start()
    t_7.start()



    t_1.join()
    t_2.join()
    t_3.join()
    t_4.join()
    t_6.join()
    t_7.join()

if __name__ == '__main__':
    main()
