# -*- coding: utf-8 -*

from time import sleep, time
from listpage_crawler import ptt_listpage_crawler
from postpage_crawler import post_crawler
import json

# 取得指定天數的 post list 資料，存成陣列
def get_post_list(day_bias = 7):
    # Input day_bias: 要查詢的天數(正整數)
    # return msg_r : 可傳給使用者看的查詢結果(string)
    # return df_r : 查詢結果組成的sorted DataFrame
    # PTT表特版首頁
    url = "https://www.ptt.cc/bbs/Beauty/index.html"

    day_bias = -day_bias + 1

    start_time = time()

    post_list = []
    delay_sec = 0.1
    count = 0
    if day_bias > 0:
        print("Check day_bias!!!")
    # while url != None:
    while url is not None:
        url, next_post_list = ptt_listpage_crawler(url, day_bias)
        print(url,'\n')
        post_list = post_list + next_post_list[::-1]
        count += 1
        sleep(delay_sec)

    end_time = time()
    duration = end_time - start_time
    print("花費時間: ",duration)
    return post_list



post_list = get_post_list(60)

print("\n\n post_list:", post_list)

# 從陣列裡面把每個 url 丟進 post_crawler 爬取 po 文內容，回傳 post_time, author, comments, img_name_list, img_url_list
for index, post in enumerate(post_list):
    post_time, author, comments, img_name_list, img_url_list = post_crawler(post['url'], index)
    # print(post_time, author, img_name_list, img_url_list)
    post_list[index]['post_time'] = post_time
    post_list[index]['imgs'] = img_url_list
    post_list[index]['author'] = author
    post_list[index]['comments'] = comments
    
    # 顯示每一頁的資料
    print(post_list[index]['url'])
    print(post_list[index],'\n')

print("\n\n Done \n\n",post_list, "\n\n Done \n\n")

# 存成字典
with open('data.json', 'w') as file:
    json.dump(post_list, file, ensure_ascii=False)