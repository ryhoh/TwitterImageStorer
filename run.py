from crawler import *
from load_credential import Credential

credit = Credential()

# ターゲットの Twitter id を改行区切りで記述し id.txt とする
with open("id.txt", "r") as f:
    ids = f.read().split("\n")
    ids.remove("")

    # '#' によってコメントアウトされた行を飛ばす
    for uid in ids:
        if uid[0] == '#':
            ids.remove(uid)

for uid in ids:
    crawler = Crawler(credit.get_api(), uid)
    crawler.store_contents()
