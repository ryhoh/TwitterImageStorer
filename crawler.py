import os
import json
from io import StringIO
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

        if uid is None or uid == "":
            raise ValueError("uid expected str of twitterID, but given '{}'".format(uid))
        else:
            self._uid = uid

    def _make_dir(self):
        try:  # ディレクトリが無ければ作成
            os.mkdir(self._uid)
        except FileExistsError:
            pass
        os.chdir(self._uid)

    def store_contents(self, include_rt_fv: bool = True):
        print("store start: {}".format(self._uid))
        self._make_dir()

        urls = list()
        try:
            for page in range(1, 17):
                tweets = self._api.user_timeline(self._uid, count=200, page=page)
                for tweet in tweets:
                    # 本人のツイートだけほしい場合
                    if not include_rt_fv and tweet._json['text'][:4] == 'RT @':
                        continue
                    # 各tweet.textからurlを抽出
                    if 'extended_entities' in tweet._json.keys():
                        ext_ent_dict = tweet._json['extended_entities']
                        urls.append(ext_ent_dict['media'][0]['media_url_https'])
                time.sleep(1)
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
        print("[{}]: {}".format(req.status_code, url))
        if req.status_code == 200:
            with open(f_name, "wb") as f:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, f)
                print("stored: {}".format(f_name))
        time.sleep(1)


if __name__ == "__main__":
    credit = Credential()
    crawler = Crawler(credit.get_api(), "Kandai_Lib")  # 適当なidでテスト
    crawler.store_contents()
