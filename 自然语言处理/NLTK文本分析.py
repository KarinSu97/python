import nltk

#下载语料库
nltk.download()

#加载语料库，以布朗语料库为例
from nltk.corpus import brown
brown.categories()   #查看语料库的目录
len(brown.sents())   #句子数
len(brown.words())   #词汇数

#分词
sentence="I love my mother"
words=nltk.word_tokenize(sentence)

#词性标注
nltk.pos_tag(words)

#词形归一化
from nltk.stem import WordNetLemmatizer
wl=WordNetLemmatizer()
wl.lemmatize('dogs')
wl.lemmatize('are',pos='v')   #pos默认为nn

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
ps.stem('connected')
ps.stem('dogs')

from nltk.stem.lancaster import LancasterStemmer
ls=LancasterStemmer()
ls.stem('connected')
ls.stem('dogs')

#过滤停用词
from nltk.corpus import stopwords
stopwords.words('english')   #停用词列表
sentence='I love my mother'
words=nltk.word_tokenize(sentence)
[word for word in words if word not in stopwords.words('english')]

#词频统计
nltk.FreqDist(words)

#获取词频最高的前N个词汇
import jieba
content='''
百度一下，你就知道
网页搜索: 全球最大的中文搜索引擎
作为全球最大的中文搜索引擎公司，百度一直致力于让网民更平等的获取信息，找到所求。百度是用户获取信息的最主要入口，随着移动互联网的发展，百度网页搜索完成了由PC向移动的转型，由连接人与信息扩展到连接人与服务，用户可以在PC、Pad、手机上访问百度主页，通过文字、语音、图像多种交互方式瞬间找到所需要的信息和服务。
手机百度: 随时随地，找到所求！
手机百度是目前国内活跃用户TOP3的App，依托百度网页、百度图片、百度新闻、百度知道、百度百科、百度地图、百度音乐、百度视频等专业垂直搜索频道，方便用户随时随地使用百度搜索服务。
百度地图: Map your life！
百度地图是百度提供的一项网络地图搜索服务。用户可以查询街道、商场、楼盘的地理位置，也可以找到最近的所有餐馆、学校、银行、公园等等。
百度，连接人与服务
百度糯米: 省钱更省心！
百度糯米汇集美食、电影、酒店、休闲娱乐、旅游、到家服务等众多生活服务的相关产品，并先后接入百度外卖、去哪儿网资源，一站式解决吃喝玩乐相关的所有问题，逐渐完善了百度糯米O2O的生态布局。
百度金融
百度金融服务事业群组（FSG），成立于2015年12月14 日，业务架构主要包括消费金融、钱包支付、理财、互联网银行、互联网保险等多个板块，基本覆盖金融服务的各个领域。百度将金融业务提升到战略级位置，寻求在金融服务领域扮演‘改革派’的角色。
百度，每个人的舞台
百度贴吧: 上贴吧，找组织
百度贴吧，全球最大的中文社区。贴吧是一种基于关键词的主题交流社区，它与搜索紧密结合，准确把握用户需求，搭建别具特色的“兴趣主题“互动平台。贴吧目录涵盖社会、地区、生活、教育、娱乐明星、游戏、体育、企业等方方面面，目前是全球最大的中文交流平台。
百度百科: 全球最大的中文百科全书
百度百科是一个内容开放、自由的网络百科全书平台， 旨在创造一个涵盖各领域知识的中文信息收集平台。百度百科强调用户的参与和奉献精神，充分调动互联网用户的力量，汇聚上亿用户的头脑智慧，积极进行交流和分享。
百度知道: 总有一个人知道你问题的答案
百度知道，是百度旗下的互动式知识问答分享平台，也是全球最大的中文问答平台。广大网友根据实际需求在百度知道上进行提问，便立即获得数亿网友的在线解答。
百度文库: 让每个人平等的提升自我
百度文库是百度发布的供网友在线分享文档的知识平台，是最大的互联网学习开放平台。百度文库用户可以在此平台上，上传， 在线阅读与下载文档。
百度，互联网生活助手
百度手机助手: 最具人气的应用商店
百度手机助手是Android手机的权威资源平台，分发市场份额连续十个季度排名市场第一，拥有最全最好的应用、游戏、壁纸资源，帮助用户在海量资源中精准搜索、高速下载、轻松管理，万千汇聚，一触即得。
百度云: 云上的日子，你我共享
百度云是百度推出的一项云存储服务，不仅为用户提供免费的存储空间，还可以将照片、视频、文档、通讯录等数据在移动设备和PC客户端之间跨平台同步和管理;百度云还支持添加好友、创建群组，并可跨终端随时随地进行分享。
百度移动端输入法: 更懂你的表达
拥有六亿用户的百度输入法，支持拼音、笔画、五笔、手写、语音、智能英文等多种输入方式，还结合点划等人性化的交互操作，输入流畅精准。输入法提供丰富的emoji表情、颜文字、图片表情等帮助年轻用户个性化的表达。
百度浏览器: 做个有趣的人
百度手机浏览器是百度自主研发，为手机上网用户量身定制的一款浏览类产品，于2011 年6月15日正式上线公测，极速内核强劲动力，提供超强智能搜索，整合百度优质服务。
Hao123: 上网从这里开始
Hao123创立于1999年，2004年被百度收购。作为百度旗下核心产品，hao123及时收录包括音乐、视频、小说、游戏等热门分类的网站，与搜索完美结合，为中国互联网用户提供最简单便捷的网上导航服务，重新定义了上网导航的概念。
百度杀毒: 更快更安全
百度杀毒是由百度公司研发的专业杀毒软件，也是世界上第一款将“深度学习”技术应用到病毒查杀客户端的产品。产品依托于百度强大的云计算、大数据能力。自2013年上线以来，百度杀毒累积为千万用户提供网络安全服务。
百度卫士: 轻、快、智、净
百度卫士是百度公司出品的系统工具软件，集电脑加速、系统清理、安全维护三大功能于一身，为用户提供优质的电脑及网络安全服务。
百度医生: 更权威，更便捷，更丰富，连接人与医疗服务
百度医生打造了面向普通用户、医生以及医院的产品体系，包括百度医生、百度医生工作台、百度医学、医疗直达号等，实现医患双选的业务模式，从而优化医疗资源的配置效率，提升各方的工作效率，改善患者的就医体验。
百度商业服务，新生产力引擎
百度商业服务是原有的百度推广（以搜索推广为主）的基础上，将数据产品、交易产品、媒体产品、信用产品和咨询服务进行了深度的整合， 并已将咨询服务、百度内容联盟加入到整体的商业服务框架中来。
目前百度商业服务包括三大类产品服务: 以凤巢搜索排名为基础的推广类产品服务，品牌宣传类的产品服务以及基于大数据的数据产品增值服务
'''
words=jieba.cut(content)
words_freq=nltk.FreqDist(words)
print(words_freq.most_common(50))   #词频最高的50个词汇

#计算TF-IDF
from nltk import TextCollection
corpus=TextCollection(['I love my mother','I love my country','I love my daddy'])
corpus.tf_idf('country','I love my country')

#句法树
from nltk.corpus import treebank
from nltk.tree import Tree
sentTree='(IP (NP (NR 张三)) (VP (VV 参加) (AS 了) (NP (NN 会议))))'
tree=Tree.fromstring(sentTree)
tree.draw()