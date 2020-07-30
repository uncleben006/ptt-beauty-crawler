import requests
import json

with open('data.json') as json_file:
    datas = json.load(json_file)

    book = []
    section = []
    # 如果 index 集到 200 就存成一個 array，一次兩百筆輸入會比較快
    for index, data in enumerate(datas):

        # 先把 data 存入 section，當 index 被 200 整除時再存入 book，同時清空 section，重複直到 datas 沒了
        section.append(data)

        if index % 200 == 0 and index != 0:
            book.append(section)
            section = []

        # 若 index 與最大值相同，也要存入 book
        if index == len(datas)-1:
            book.append(section)

    # 以 section 為單位打入 api
    for section in book:
        print(len(section))
        response = requests.post('http://127.0.0.1:5000/api/', json.dumps(section, ensure_ascii = False).encode('utf-8'))
        # print(data, '\n')
        print(response.status_code)