import tweepy


# OAuth 認証データのロード
class Credential(object):
    def __init__(self):
        self.api = None  # type: tweepy.API

    def load_api(self) -> tweepy.API:
        # 一度認証を済ませたら，以後は認証済みのオブジェクトを返す
        if self.api is not None:
            return self.api
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
            self.api = tweepy.API(auth)
            return self.api


if __name__ == '__main__':
    c = Credential()
    print(c.load_api())
    print(c.load_api())

    print(c.api.get_user("Kandai_Lib"))
