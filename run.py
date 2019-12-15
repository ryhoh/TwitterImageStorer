import sys
import traceback
from crawler import *
from load_credential import Credential

credit = Credential()

# ターゲットの Twitter id を改行区切りで記述し id.txt とする
with open("id.txt", "r") as f:
    ids = f.read().split("\n")

    if " " in ids:
        ids.remove(" ")

    if "" in ids:
        ids.remove("")

    # '#' によってコメントアウトされた行を飛ばす
    for uid in ids:
        if uid[0] == '#':
            ids.remove(uid)

for uid in ids:
    try:
        crawler = Crawler(credit.get_api(), uid)
    except ValueError as e:
        t, v, tb = sys.exc_info()
        err_name = traceback.format_exception(t, v, tb)[-1].split(':')[0]
        sys.stderr.write("[{}] skipping '{}'\n".format(err_name, uid))
        continue

    crawler.store_contents()
