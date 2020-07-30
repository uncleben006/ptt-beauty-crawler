# -*- coding: utf-8 -*

import requests
from bs4 import BeautifulSoup as bs
from day_computing import get_date_str, Is_within_Target_Date_2020


def ptt_listpage_crawler(url, day_bias=0):
    """
    crawl the ptt list page

    para::[url]
        - type: str
        - starting page URL
    para::[day_bias]
        - type: (minus) int
        - number of days before today
        - example: zero stands for today; -1 stands for yesterday 
    return::
        - [str] url of previous page; return None if achieved target date
        - [list] posts collection with target date
    """

    jar = requests.cookies.RequestsCookieJar()
    # 可把不同網頁的 cookie 設定進一個jar
    jar.set("over18", "1", domain="www.ptt.cc")
    # 將cookies加入request
    response = requests.get(url, cookies=jar).text
    # response為html格式，交由bs4解析
    html = bs(response)

    # 找到導航列
    navi_bar = html.find("div", class_="btn-group btn-group-paging")
    navi_bottons = navi_bar.find_all("a", class_="btn wide")
    # 從導航列取得上一頁的URL(next_url)
    for n in navi_bottons:
        if '上頁' in n.text:
            next_url = "https://www.ptt.cc" + n["href"]


    post_block = html.find("div", class_="r-list-container action-bar-margin bbs-screen")
    posts = post_block.find_all("div", class_="r-ent")
    post_list = []
    for post in posts:
        p = {}
        # Title - 文章標題
        try:
            p['title'] = post.find("div", class_="title").find("a").text
        except AttributeError:      # 如果文章已被刪除則略過
            p['title'] = post.find("div", class_="title").text
            if '刪除' in p['title']:
                continue
        if '公告' in p['title']:    # 如果是公告文則略過
            continue
        # URL - 文章連結
        try:
            url_path = post.find("div", class_="title").find("a")["href"]
            p['url'] = "https://www.ptt.cc" + url_path
            p['slug'] = '.'.join(url_path.split('/')[3].split('.')[:4])
            
        except:
            continue
        # DATE - 日期
        p['post_time'] = post.find("div", class_="date").text
        if not Is_within_Target_Date_2020(p['post_time'], get_date_str(day_bias)):
            next_url = None 
            continue  # 不在目標日期範圍內，略過此筆
        # PUSH - 推文數
        try:
            p['push'] = post.find("div", class_="nrec").find("span", class_="hl").text
        except AttributeError:      # 處理沒有人推文
            p['push'] = 0
        post_list.append(p)

    return next_url, post_list

# # Print for debugging
# for p in post_list:
#     for key, value in p.items():
#         print("{}: {}" .format(key, value))
#     print("------------------------------------------------")
