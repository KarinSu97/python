import requests, os, bs4
import urllib.request

os.makedirs('npm', exist_ok = True) #我准备把图片放到‘npm’这个文件夹里面

url = 'https://www.npm.gov.tw/Article.aspx?sNo=03000060&pageNo=1' #台北故宫博物馆的网址,这里需要在url里面添加pageNo的属性
res = requests.get(url) #先把网址拿到
soup = bs4.BeautifulSoup(res.text,'html.parser')#再去解析里面的东西
picElem=soup.find_all("div", {"class":"pic imgLiquid"})#筛选出所有class=pic imgLiquid的东东

#进行循环迭代
i=1
while picElem:
    #获取当前页所有图片的链接列表
    img_list=[]
    for text in picElem:
        child=list(text.children)[0]
        img_list.append(child.get('src'))
    #下载图片
    for picUrl in img_list:
        print(picUrl)
        #开始下载图片
        urllib.request.urlretrieve(picUrl,filename=os.path.join('npm', os.path.basename(picUrl)))
        # #print ('Downloading image %s...' % (picUrl))   
        # res = requests.get(picUrl)
        # #开始保存图片到npm的文件夹
        # imageFile = open(os.path.join('npm', os.path.basename(picUrl)), 'wb')
        # for chunk in res.iter_content(100000):
        #     imageFile.write(chunk)
        #  imageFile.close()
    i+=1
    url = 'https://www.npm.gov.tw/Article.aspx?sNo=03000060&pageNo=%d' % i  # 台北故宫博物馆的网址,这里需要在url里面添加pageNo的属性
    res = requests.get(url)  # 先把网址拿到
    soup = bs4.BeautifulSoup(res.text, 'html.parser')  # 再去解析里面的东西
    picElem = soup.find_all("div", {"class": "pic imgLiquid"})  # 筛选出所有class=pic imgLiquid的东东


