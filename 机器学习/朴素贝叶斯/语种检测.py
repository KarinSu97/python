'''
#############################
采用朴素贝叶斯进行语种检测
#############################
'''

from sklearn.cross_validation import train_test_split
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

#加载数据
file_path=r'C:\Users\T\Desktop\python视频\data.csv'
with open(file_path) as f:
    lines=f.readlines()
dataset=[(line.strip()[:-3],line.strip()[-2:]) for line in lines]

#切分训练集和测试集
x,y=zip(*dataset)
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=1)

#数据清洗，去除链接等字符串
def remove_noise(document):
    pattern=re.compile("|".join(["http\S+","\@\w+","\#\w+"]))
    clean_test=re.sub(pattern,"",document)
    return clean_test.strip()

#提取特征,统计词频
vec=CountVectorizer(
    lowercase=True,   #转化为小写
    ngram_range=(1,2),   #提取1-gram,2-gram的统计特征
    analyzer="char_wb",   #采用character ngrams分词
    max_features=1000,   #保留前1000个关键词
    preprocessor=remove_noise   #预处理函数
)
vec.fit(x_train)

#构建朴素贝叶斯分类
classifier=MultinomialNB()
classifier.fit(vec.transform(x_train),y_train)

#查看准确率
classifier.score(vec.transform(x_test),y_test)

'''
#############################
写成class类版本
#############################
'''
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


class LanguageDetector():

    def __init__(self, classifier=MultinomialNB()):
        self.classifier = classifier
        self.vectorizer = CountVectorizer(ngram_range=(1,2), max_features=1000, preprocessor=self._remove_noise)

    def _remove_noise(self, document):
        noise_pattern = re.compile("|".join(["http\S+", "\@\w+", "\#\w+"]))
        clean_text = re.sub(noise_pattern, "", document)
        return clean_text

    def features(self, X):
        return self.vectorizer.transform(X)

    def fit(self, X, y):
        self.vectorizer.fit(X)
        self.classifier.fit(self.features(X), y)

    def predict(self, x):
        return self.classifier.predict(self.features([x]))

    def score(self, X, y):
        return self.classifier.score(self.features(X), y)

in_f = open('data.csv')
lines = in_f.readlines()
in_f.close()
dataset = [(line.strip()[:-3], line.strip()[-2:]) for line in lines]
x, y = zip(*dataset)
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)

language_detector = LanguageDetector()
language_detector.fit(x_train, y_train)
print(language_detector.predict('This is an English sentence'))
print(language_detector.score(x_test, y_test))