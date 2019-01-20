import os
import re
import sys
import requests
import shutil
import time
import tweepy

from load_credential import Credential


class Crawler(object):
    def __init__(self, api: tweepy.API, uid: str):
        if api is None:
            raise ValueError
        else:
            self._api = api

        if uid is None:
            raise ValueError
        elif uid == "":
            raise ValueError
        else:
            self._uid = uid

    def _make_dir(self):
        try:  # ディレクトリが無ければ作成
            os.mkdir(self._uid)
        except FileExistsError:
            pass
        os.chdir(self._uid)

    def store_contents(self):
        self._make_dir()

        html_pat = re.compile("https?://[a-zA-Z0-9./\-!?=#]+")
        urls = list()
        try:
            for page in range(1, 17):
                tweets = self._api.user_timeline(self._uid, count=200, page=page)
                for tweet in tweets:
                    # 各tweet.textからurlを抽出
                    # jsonの各属性にそれらしいurlが集まってる模様
                    urls.extend(re.findall(html_pat, str(tweet._json)))
        except tweepy.TweepError:
            sys.stderr.write(self._uid + ": user loading error (invalid id?)\n")

        for url in set(urls):
            self.download_image(url)

        os.chdir("..")  # 親ディレクトリに戻しておく

    @classmethod
    def download_image(cls, url: str):
        # クロールすべきか判定
        valid_suffixes = ["jpg", "png", "gif", "mp4"]
        for valid_suffix in valid_suffixes:
            if "." + valid_suffix in url:
                extension = "." + valid_suffix  # 拡張子を覚えておく
                break
        else:
            return None

        # ファイル名は，最後の/から後ろをそのまま
        # ただし，拡張子の後にゴミが付いている場合は取り除く
        f_name = url.split("/")[-1].split(extension)[0] + extension

        # すでに同名ファイルが存在するなら取得せずにスキップすべき
        if os.path.exists(f_name):
            return None

        # 実際にクロール
        req = requests.get(url, stream=True)
        if req.status_code == 200:
            with open(f_name, "wb") as f:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, f)
        time.sleep(1)


if __name__ == "__main__":
    credit = Credential()
    crawler = Crawler(credit.get_api(), "Kandai_Lib")  # 適当なidでテスト
    crawler.store_contents()
