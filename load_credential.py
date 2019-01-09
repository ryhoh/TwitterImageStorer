import tweepy


# OAuth 認証データのロード
class Credential(object):
    def __init__(self):
        self._api = None  # type: tweepy.API

    def get_api(self) -> tweepy.API:
        # 一度認証を済ませたら，以後は認証済みのオブジェクトを返す
        if self._api is not None:
            return self._api
        else:
            credit = dict()
            with open("credential.txt") as f:
                while True:
                    line = f.readline().replace("\n", "")
                    if line == "\n":
                        continue
                    elif line == "":
                        break
                    else:
                        elm = line.replace(" ", "").replace("\t", "").split(":")
                        credit[elm[0]] = elm[1]

            auth = tweepy.OAuthHandler(credit["consumer_key"], credit["consumer_secret"])
            auth.set_access_token(credit["access_token_key"], credit["access_token_secret"])
            self._api = tweepy.API(auth)
            return self._api


if __name__ == '__main__':
    c = Credential()
    print(c.get_api())
    print(c.get_api())

    print(c._api.get_user("Kandai_Lib"))
