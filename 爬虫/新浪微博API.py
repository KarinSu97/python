from sinaweibopy import APIClient


APP_KEY='3151141516'
APP_SECRET='3ebb0fc72a4b807560bac39973dad389'
CALLBACK_URL='https://api.weibo.com/oauth2/default.html'
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()

code =input()
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)

access_token = r.access_token #新浪返回的token，类似abc123xyz456
expires_in = r.expires_in  #token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
client.set_access_token(access_token, expires_in)  #在此可保存access token

print(client.get.statuses__public_timeline())