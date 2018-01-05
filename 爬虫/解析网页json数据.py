import requests
import json
from pandas import DataFrame

#获取json数据
url='http://180.153.255.6/mobile/discovery/v2/category/keyword/albums?calcDimension=hot&categoryId=13&device=android&keywordId=286&pageId=1&pageSize=20&version=6.3.15'
text=requests.get(url).text
data=json.loads(text)

#转化为dataframe格式
data=DataFrame(data)