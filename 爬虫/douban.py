import requests, os, bs4

os.makedirs('npm', exist_ok=True)  # 我准备把图片放到‘npm’这个文件夹里面

#总共有两页
for page in range(2):
    print("爬取第%d页内容..." % (page+1))
    url = 'https://www.douban.com/doulist/45345711/?start=%d' % (page*25)  #每页25本书

    res = requests.get(url) #先把网址拿到
    soup = bs4.BeautifulSoup(res.text,'html.parser')#再去解析里面的东西
    # print(res.text)
    picElem = soup.find_all('img',{'width':'100'}) #获取图像链接

    if picElem == []:
        print ('Could not find exhibition picture')
    else:
        img_list = []
        for text in picElem:
            img_list.append(text.get('src'))
        for picUrl in img_list:
            print(picUrl)
            #开始下载图片
            # print ('Downloading image %s...' % (picUrl))   
            res = requests.get(picUrl)
            #开始保存图片到npm的文件夹
            imageFile = open(os.path.join('npm', os.path.basename(picUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()


