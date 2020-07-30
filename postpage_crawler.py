# -*- coding: utf-8 -*

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from zipfile import ZipFile
from os import remove
import ssl
import warnings


# Issue handling
ssl._create_default_https_context = ssl._create_unverified_context  # SSL
warnings.filterwarnings('ignore')  # 移除bs4的warning


def post_crawler(post_url, zipfile_name):
    jar = requests.cookies.RequestsCookieJar()
    # 可把不同網頁的 cookie 設定進一個jar
    jar.set("over18", "1", domain="www.ptt.cc")
    # 將cookies加入request
    response = requests.get(post_url, cookies=jar).text

    # response為html格式，交由bs4解析
    html = bs(response)

    main_content = html.find("div", class_="bbs-screen bbs-content")

    metas = main_content.find_all("span", class_="article-meta-tag")
    m_values = main_content.find_all("span", class_="article-meta-value")

    # Remove(extract) 作者 標題 時間 ------------------------
    meta = main_content.find_all("div", class_="article-metaline")
    for m in meta:
        m.extract()
    # Remove(extract) 看板名稱 ------------------------------
    right_meta = main_content.find_all("div", class_="article-metaline-right")
    for single_meta in right_meta:
        single_meta.extract()

    # Remove(extract) 推文前   ------------------------------
    datas = main_content.find_all("span", class_="f2")
    for data in datas:
        data.extract()

    # Remove(extract) 推文   --------------------------------
    pushes = main_content.find_all("div", class_="push")
    comments = []
    for single_push in pushes:
        push_tag = single_push.find("span", class_="push-tag").text.strip()
        push_userid = single_push.find("span", class_="push-userid").text.strip()
        push_content = single_push.find("span", class_="push-content").text.split(":")[1].strip()
        ipdatetime = single_push.find("span", class_="push-ipdatetime").text
        push_ip = ipdatetime.strip().split(" ")[0]
        push_time = " ".join(ipdatetime.strip().split(" ")[1:])
        comment = { "status": push_tag, "comment_id": push_userid, "content": push_content,"ip": push_ip,"comment_time": push_time }
        comments.append(comment)

    # Remove(extract) imgur圖片 ----------------------------
    # 1. 第一個部分，連結
    img_l = []
    photo_hrefs = main_content.find_all("a")
    for pic in photo_hrefs:
        if 'imgur' in pic["href"] and 'https' in pic["href"]:
            img_l.append(pic["href"])
            pic.extract()
    # # 2. 第二個部分，圖片顯示(richcontent)
    # richcontents = main_content.find_all("div", class_="richcontent")
    # for rich in richcontents:
    #   rich.extract()

    reply_msg = ""  # 開始搜集回應使用者的文字資訊

    # for (m, v) in zip(metas, m_values):
    #     print(m.text, ':', v.text)
    # for (m, v) in zip(metas, m_values):
    #     if m.text in ['標題', '時間']:
    #         reply_msg += m.text + ': ' + v.text + '\n'
    #     print(m.text, ':', v.text)
    # print(m_values[0].text)
    try:
        author = m_values[0].text        
    except:
        author = ''
    
    try:
        post_time = m_values[3].text
    except:
        post_time = ''

    # print("分數 :", score)
    # reply_msg += "分數: " + str(score) + '\n'
    # print("內文 :")
    # reply_msg += "內文: "

    # print(main_content.text)
    content = main_content.text
    # content_split = content.split('--')
    origin_content = content.split('--')[0]
    ori_l = origin_content.split("\n")
    ori_linted = []
    for o in ori_l:
        if o != "":
            ori_linted.append(o)
    # for i in ori_linted:
    #     reply_msg += (i + '\n')
    #     print(i)

    # print("圖片連結 :")
    img_name_list = []
    img_url_list = []
    for img in img_l:
        # 連結不含副檔名則加上.jpg
        if img[-4:] != ".gif" and img[-3:] != "jpg":
            img += ".jpg"
        # 下載圖片
        f = img.split('/')[-1]
        # urlretrieve(img, f)
        # print(img)
        img_name_list.append(f)
        img_url_list.append(img)

    return post_time, author, comments, img_name_list, img_url_list  # (回應使用者的文字資訊, 回傳圖片檔名list)


def img_dl_zip(img_url_list, zipfile_name):
    f_name = zipfile_name + '.zip'
    with ZipFile(f_name, 'w') as myzip:
        for img in img_url_list:
            # 連結不含副檔名則加上.jpg
            if img[-4:] != ".png" and img[-4:] != ".gif" and img[-3:] != "jpg":
                img += ".jpg"

            # 下載圖片、加入zip、刪除照片
            f = img.split('/')[-1]
            urlretrieve(img, f)
            print("downloaded: ", img)

            filename = img.split('/')[-1]
            myzip.write(filename)
            print("added to zip: ", filename)

            remove(filename)
            print("removed: ", filename)
    return f_name


def rm_img(img_name_list, num):
    '''
    param img_name_list: image file names
    param num: number of img to remove this time
                1, 2, 3, ...
                0 for remove all
    '''
    if num == 0:
        for img in img_name_list:
            print(img)
            remove(img)
    else:
        for _ in range(num):
            f = img_name_list.pop(0)
            remove(f)
            print(f)
