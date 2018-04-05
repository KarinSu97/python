import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

def get_momo_data(index,iter):
    url1 = "https://api.immomo.com/v1/nearby/index"
    querystring1 = {"fr":"593768028"}
    payload1 = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dpp\"\r\n\r\nf6a754e0b85abf8e424d54cc23d83a6a\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"industry\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"device_type\"\r\n\r\nandroid\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"screen\"\r\n\r\n1080x1920\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"native_ua\"\r\n\r\nMozilla/5.0 (Linux; Android 6.0; Le X620 Build/HEXCNFN5902812161S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.91 Mobile Safari/537.36\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"activetime\"\r\n\r\n4320\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"constellation\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"locater\"\r\n\r\n200\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"_h\"\r\n\r\n1b11e\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ct\"\r\n\r\n1521282092031684\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"count\"\r\n\r\n24\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"phone_netWork\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"market_source\"\r\n\r\n13\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"rom\"\r\n\r\n6.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"loctype\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"emu\"\r\n\r\n029f181d6e7ba188885c78462623c37a\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"imei\"\r\n\r\n861545033179591\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"version\"\r\n\r\n694\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"osversion_int\"\r\n\r\n23\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"rqid\"\r\n\r\nef9c9cc2\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"index\"\r\n\r\n%d\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"manufacturer\"\r\n\r\nLeMobile\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"phone_type\"\r\n\r\nGSM\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"apksign\"\r\n\r\n4f3a531caff3e37c278659cc78bfaecc\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"imsi\"\r\n\r\ne5a2b54e06db75d57023f5ec0e03f77a\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"agerange\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"acc\"\r\n\r\n30.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"android_id\"\r\n\r\ncb9c4d22158e7bcb\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"gapps\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"cell_id\"\r\n\r\n101959426\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"buildnumber\"\r\n\r\nHEXCNFN5902812161S/1513359015\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"mac\"\r\n\r\n02:00:00:00:00:00\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"refreshmode\"\r\n\r\nauto\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"network_class\"\r\n\r\nwifi\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"net\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"lng\"\r\n\r\n0.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"router_mac\"\r\n\r\nc8:3a:35:30:43:20\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"total\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"save\"\r\n\r\nYES\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"social\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"uid\"\r\n\r\nf11c77ab99c6b028a6521b7280ac05ab\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"sex\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"lat\"\r\n\r\n0.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nLe X620\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % index
    headers1 = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cookie': "SESSIONID=FBBB2701-2721-800B-C461-BEF0D6944D84",
        'Cache-Control': "no-cache",
        'Postman-Token': "6555c76b-c37f-49c8-882b-e1972f382efb"
        }
    response1 = requests.request("POST", url1, data=payload1, headers=headers1, params=querystring1,verify=False)
    result1=json.loads(response1.text)
    data1=json_normalize(result1['data']['lists'])
    raw_count=data1.shape[0]
    print('获取第%d次列表完毕...' % iter)
    #print(data1)
    data2=pd.DataFrame()
    for i in data1['source.momoid']:
        url2 = "https://api.immomo.com/api/profile/%s" % i
        querystring2 = {"fr": "593768028"}
        payload2 = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"_h\"\r\n\r\n8574b\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ct\"\r\n\r\n1521363078377545\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"rqid\"\r\n\r\nadd70a75\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"source_info\"\r\n\r\n{type:2,extra:com.immomo.momo.maintab.cx}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"source\"\r\n\r\n附近的人\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"pversion\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"signcount\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".encode(
            'utf-8')
        headers2 = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cookie': "SESSIONID=FBBB2701-2721-800B-C461-BEF0D6944D84",
            'Cache-Control': "no-cache",
            'Postman-Token': "6459782e-03b0-40e1-9306-a44ffdb4dac5"
        }
        response2 = requests.request("POST", url2, data=payload2, headers=headers2, params=querystring2, verify=False)
        result2 = json.loads(response2.text)
        data3 = json_normalize(result2)
        url3 = "https://api.immomo.com/v1/feed/user/timeline"
        querystring3 = {"fr": "593768028"}
        payload3 = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"_h\"\r\n\r\nc82ce\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ct\"\r\n\r\n1521384223063437\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"rqid\"\r\n\r\n26e049d7\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"count\"\r\n\r\n20\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"index\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"remoteid\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % i
        headers3 = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cookie': "SESSIONID=FBBB2701-2721-800B-C461-BEF0D6944D84",
            'Cache-Control': "no-cache",
            'Postman-Token': "81ff5c51-f172-449a-9384-b07b6e63ca09"
        }
        response3 = requests.request("POST", url3, data=payload3, headers=headers3, params=querystring3,verify=False)
        result3=json.loads(response3.text)
        data3['全部动态']=[result3]
        data2 = pd.concat([data2,data3],axis=0)
        print('获取用户%s完毕' % i)
        #print(data3)
    data=pd.merge(data1,data2,left_on='source.momoid',right_on='momoid')
    return data,raw_count

data_all=pd.DataFrame()
index=0
iter=1
data,raw_count=get_momo_data(index=index,iter=iter)
while data.shape[0]>0:
    data_all=data_all.append(data)
    index=index+raw_count
    iter+=1
    data,raw_count=get_momo_data(index=index,iter=iter)

data_all.to_csv('C:\\Users\\T\\Desktop\\momo_example.csv')



