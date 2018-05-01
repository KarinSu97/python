import urllib.request
import re
import pymysql

#连接数据库
conn = pymysql.connect(host='localhost', user='root', password='123456', db='spiders', port=3306,charset='utf8mb4')

def get_item_content(key_word='短裤'):
    #模拟表头信息并对搜索关键词进行编码
    key_word=urllib.request.quote(key_word)
    headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
    opener=urllib.request.build_opener()
    opener.addheaders=[headers]
    urllib.request.install_opener(opener)
    #爬取第一页数据
    url1='https://s.taobao.com/search?q='+key_word+'&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
    data1=urllib.request.urlopen(url1).read().decode('UTF-8','ignore')
    #获取第一页对应的商品名称和商品id
    pattern1='"raw_title":"(.*?)"'
    title=re.compile(pattern1).findall(data1)
    pattern2='"nid":"(.*?)"'
    nid=re.compile(pattern2).findall(data1)
    i=1
    while len(nid)>0:
        for k in range(len(nid)):
            url2='https://rate.taobao.com/feedRateList.htm?auctionNumId=%s&userNumId=42314291&currentPageNum=1&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list' % nid[k]
            data2=urllib.request.urlopen(url2).read().decode('gbk','ignore')
            pattern3='"content":"(.*?)"'
            content=re.compile(pattern3).findall(data2)
            this_content=[]
            this_content.extend(content)
            j=2
            while len(content)>0:
                url2 = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=%s&userNumId=42314291&currentPageNum=%d&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list' % (nid[k],j)
                data2 = urllib.request.urlopen(url2).read().decode('gbk','ignore')
                content = re.compile(pattern3).findall(data2)
                this_content.extend(content)
                j+=1
            for text in this_content:
                if text!='此用户没有填写评价。':
                    sql='INSERT INTO taobao VALUES ("'+nid[k]+'","'+title[k]+'","'+text+'");'
                    #print(sql)
                    conn.query(sql)
                    conn.commit()
            print("finish--"+nid[k])
        # 爬取第i+1页数据
        url1 = 'https://s.taobao.com/search?q=' + key_word + '&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&s='+str(i*44)
        data1 = urllib.request.urlopen(url1).read().decode('UTF-8', 'ignore')
        # 获取第i+1页对应的商品名称和商品id
        pattern1 = '"raw_title":"(.*?)"'
        title = re.compile(pattern1).findall(data1)
        pattern2 = '"nid":"(.*?)"'
        nid = re.compile(pattern2).findall(data1)
        i+=1

get_item_content(key_word='连衣裙')
conn.close()
