import requests
import pickle

from bs4 import BeautifulSoup
import slackweb


TARGET_URL = 'https://shikaku-mafia.com/'


# 以前の新着データを読み込む
with open('./before_article.pickle', 'rb') as f:
    before_new_article = pickle.load(f)

# Webページを取得する
html = requests.get(TARGET_URL)
soup = BeautifulSoup(html.content, "html.parser")

# 新着データを抽出する
new_article = str(soup.find(class_="entry-card-wrap").get("title"))
with open('./before_article.pickle', 'wb') as f:
    pickle.dump(before_article.pickle, f)

# 最新記事が更新されているかどうかチェック
if new_article != before_new_article:
    print('新着あり')
