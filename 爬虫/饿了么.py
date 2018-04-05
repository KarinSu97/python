import requests
from pandas.io.json import json_normalize
import json

url = "https://mainsite-restapi.ele.me/shopping/v1/restaurants/161862962/menu/categories"

headers = {
    'charset': "utf-8",
    'Accept-Encoding': "gzip",
    'referer': "https://servicewechat.com/wxece3a9a4c82f58c9/136/page-frame.html",
    'x-shard': "shopid=161862962;loc=113.347565,23.131674",
    'content-type': "application/json",
    'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Le X620 Build/HEXCNFN5902812161S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.5.1280(0x26060536) NetType/WIFI Language/zh_CN MicroMessenger/6.6.5.1280(0x26060536) NetType/WIFI Language/zh_CN",
    'Host': "mainsite-restapi.ele.me",
    'Connection': "Keep-Alive",
    'Cache-Control': "no-cache",
    'Postman-Token': "95244ab2-6243-4440-a87c-4c33b3c556fb"
    }

response = requests.request("GET", url, headers=headers,verify=False)
response=json.loads(response.text)
data=json_normalize(response[0]['foods'])
#data.to_csv('C:\\Users\\T\\Desktop\\1.csv')