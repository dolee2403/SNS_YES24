#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

base_url = 'https://www.yes24.com/24/category/bestseller'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

all_books = []
rank_counter = 1 

for page in range(1, 43):
    params = {'PageNumber': page}
    response = requests.get(base_url, headers=headers, params=params)
    print(f"[{page}페이지] 상태코드: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = [tag.text.strip() if tag else '정보 없음' for tag in soup.select('a.gd_name')]
    authors = [tag.text.strip() if tag else '정보 없음' for tag in soup.select('span.authPub.info_auth a')]
    publishers = [tag.text.strip() if tag else '정보 없음' for tag in soup.select('span.authPub.info_pub a')]

    min_len = min(len(titles), len(authors), len(publishers))
    print(f"→ {min_len}권 수집됨")

    for i in range(min_len):
        순위 = rank_counter + i
        책제목 = titles[i]
        저자 = authors[i]
        출판사 = publishers[i]

        print(순위, 책제목, 저자, 출판사)
        all_books.append([순위, 책제목, 저자, 출판사])

    rank_counter += min_len
    time.sleep(1)  

df = pd.DataFrame(all_books, columns=["순위", "책제목", "저자", "출판사"])
df.to_csv("yes24_bestseller_final.csv", index=False, encoding="utf-8-sig")
print(f"\n✅ 총 {len(df)}권 저장 완료 → yes24_bestseller_final.csv")

