import requests
import json
from pandas.io.json import json_normalize
import urllib.parse
import re
import pandas as pd
import numpy as np

url1 = "https://app.ganji.com/datashare/"
payload1='jsonArgs={"customerId":"801","cityScriptIndex":"401","categoryId":"6","pageIndex":"0","pageSize":"10","majorCategoryScriptIndex":"1","queryFilters":[{"name":"deal_type","operator":"=","value":"0"}],"sortKeywords":[{"field":"post_at","sort":"desc"}]}&showType=0'
payload1= urllib.parse.quote(payload1)
payload1=re.sub('jsonArgs%3D','jsonArgs=',payload1)
payload1=re.sub('%26showType%3D0','&showType=0',payload1)
#urllib.parse.unquote(payload1)
#payload1 = "jsonArgs=%7B%22customerId%22%3A%22801%22%2C%22cityScriptIndex%22%3A%22401%22%2C%22categoryId%22%3A%226%22%2C%22pageIndex%22%3A%220%22%2C%22pageSize%22%3A%2210%22%2C%22majorCategoryScriptIndex%22%3A%221%22%2C%22queryFilters%22%3A%5B%7B%22name%22%3A%22deal_type%22%2C%22operator%22%3A%22%3D%22%2C%22value%22%3A%220%22%7D%5D%2C%22sortKeywords%22%3A%5B%7B%22field%22%3A%22post_at%22%2C%22sort%22%3A%22desc%22%7D%5D%7D&showType=0"
headers1 = {
    'interface': "SearchPostsByJson3",
    'unid': "cf19dce6e45fe6988e0cea8f05717b76",
    'ay': "yingyongbaostore2",
    'userId': "ED1BC44CCF2441D03709B4F073E828EE",
    'agency': "yingyongbaostore2",
    'uniqueId': "cf19dce6e45fe6988e0cea8f05717b76",
    'ct': "17",
    'versionId': "8.6.5",
    'ds': "2.625",
    'sid': "c611c872-7592-4c53-907b-b9bf92ad1c92",
    'rl': "1080*1920",
    'clientAgent': "LeMobile/Le X620#1080*1920#2.625#6.0",
    'GjData-Version': "1.0",
    'contentformat': "json2",
    'of': "self",
    'isp': "46002",
    'dv': "LeMobile/Le X620",
    'cid': "801",
    'lct': "17",
    'net': "wifi",
    'lng': "113.912164",
    'os': "Android",
    'rid': "7bb6ef18-637e-4d1b-8116-810b6b97caeb",
    'ov': "23",
    'vs': "8.6.5",
    'lar': "1210",
    'lat': "22.545886",
    'aid': "ED1BC44CCF2441D03709B4F073E828EE",
    'CustomerId': "801",
    'model': "LeMobile/Le X620",
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 6.0; Le X620 Build/HEXCNFN5902812161S)",
    'Cache-Control': "no-cache",
    'Postman-Token': "d03d504d-0470-4129-8bac-402e80dbb4f2"
    }

response1 = requests.request("POST", url1, data=payload1, headers=headers1,verify=False)
response1=json.loads(response1.text)
data1=json_normalize(response1['posts'])
#data1.to_csv('C:\\Users\\T\\Desktop\\1.csv')
data3=pd.DataFrame()
for i in range(len(data1)):
    #爬取每辆车具体信息
    url2 = "https://app.ganji.com/datashare/"
    payload2='puid=%s&categoryId=6&d_sign=%s&postfrom=%s' %(data1['puid'][i],data1['d_sign'][i],data1['postfrom'][i])
    payload2= urllib.parse.quote(payload2)
    payload2=re.sub('puid%3D','puid=',payload2)
    payload2=re.sub('/','%2F',payload2)
    payload2=re.sub('%26postfrom%3D','&postfrom=',payload2)
    #payload2 = "puid=32770360344002%26categoryId%3D6%26d_sign%3D%7C%7C%2Fsite_tuiguang%2Ftrace%40gjaddata%3D%7B19%3A%7B1003%3A%7B0%3A32770360344002%7D%7D%7D%40atype%3Dshow%40business%3Dtrue&postfrom=58"
    headers2 = {
        'interface': "GetPostByPuid",
        'unid': "cf19dce6e45fe6988e0cea8f05717b76",
        'ay': "yingyongbaostore2",
        'userId': "ED1BC44CCF2441D03709B4F073E828EE",
        'agency': "yingyongbaostore2",
        'uniqueId': "cf19dce6e45fe6988e0cea8f05717b76",
        'ct': "17",
        'versionId': "8.6.5",
        'ds': "2.625",
        'sid': "c611c872-7592-4c53-907b-b9bf92ad1c92",
        'rl': "1080*1920",
        'clientAgent': "LeMobile/Le X620#1080*1920#2.625#6.0",
        'GjData-Version': "1.0",
        'contentformat': "json2",
        'of': "self",
        'isp': "46002",
        'dv': "LeMobile/Le X620",
        'cid': "801",
        'lct': "17",
        'net': "wifi",
        'lng': "113.912164",
        'os': "Android",
        'rid': "901df85c-0984-436c-84e0-653e2bc95a14",
        'ov': "23",
        'vs': "8.6.5",
        'lar': "1210",
        'lat': "22.545886",
        'aid': "ED1BC44CCF2441D03709B4F073E828EE",
        'CustomerId': "801",
        'model': "LeMobile/Le X620",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Accept-Encoding': "gzip",
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 6.0; Le X620 Build/HEXCNFN5902812161S)",
        'Host': "app.ganji.com",
        'Connection': "Keep-Alive",
        'Cache-Control': "no-cache",
        'Postman-Token': "e11396a9-1449-40c3-a88b-be0a4c9b4fbc"
        }
    response2 = requests.request("POST", url2, data=payload2, headers=headers2,verify=False)
    response2=json.loads(response2.text)
    data2=json_normalize(response2['data'])
    data3= pd.concat([data3, data2], axis=0)
    data3.index=np.arange(len(data3))
    print('finish:%d/%d' % (i,len(data1)))
data1=pd.concat([data1,data3],axis=1)


