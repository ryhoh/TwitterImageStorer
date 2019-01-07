import os
import re
import requests
import shutil
import time

from load_credential import Credential


class Crawler(object):
    def __init__(self, api, uid):
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

    def make_dir(self):
        try:  # ディレクトリが無ければ作成
            os.mkdir(self._uid)
        except FileExistsError:
            pass
        os.chdir(self._uid)

    def store_contents(self):
        self.make_dir()

        html_pat = re.compile("https?://[a-zA-Z0-9./\-_!?]+")
        urls = list()
        for page in range(1, 2):
            tweets = self._api.user_timeline(self._uid, count=200, page=page)
            for tweet in tweets:
                # 各tweet.textからurlを抽出
                # jsonのentities属性にそれらしいurlが集まってる模様
                urls.extend(re.findall(html_pat, str(tweet._json["entities"])))
        for url in urls:
            self.download_image(url)

    @classmethod
    def download_image(cls, url):
        # クロールすべきか判定
        valid_suffixes = ["jpg", "png", "gif"]
        for valid_suffix in valid_suffixes:
            if url[-len(valid_suffix)-1:] == "." + valid_suffix:
                break
        else:
            return None

        # 実際にクロール
        req = requests.get(url, stream=True)
        if req.status_code == 200:
            with open(url.split("/")[-1], "wb") as f:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, f)
        time.sleep(1)


if __name__ == "__main__":
    credit = Credential()
    crawler = Crawler(credit.load_api(), "Kandai_Lib")  # 適当なidでテスト
    crawler.store_contents()
