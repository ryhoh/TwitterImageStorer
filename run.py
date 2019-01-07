from crawler import *
from load_credential import Credential

credit = Credential()

# ターゲットの Twitter id を改行区切りで記述し id.txt とする
with open("id.txt", "r") as f:
    ids = f.read().split("\n")
    ids.remove("")

for uid in ids:
    crawler = Crawler(credit.load_api(), uid)
    crawler.store_contents()
