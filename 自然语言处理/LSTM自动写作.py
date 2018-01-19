import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Activation,LSTM,Dropout

#读取数据
file_path=r'C:\Users\T\Desktop\python视频\Winston_Churchil.txt'
raw_text=open(file_path,'rb').read().decode('utf-8')
raw_text=raw_text.lower()

#对字母进行编码
chars=sorted(list(set(raw_text)))
char_to_int=dict((c,i) for i,c in enumerate(chars))
int_to_char=dict((i,c) for i,c in enumerate(chars))

#构造数据，以每个字母前100个字母作为特征进行预测
seq_length=100
x=[]
y=[]
for i in range(len(raw_text)-seq_length):
    given=raw_text[i:i+seq_length]
    predict=raw_text[i+seq_length]
    x.append([char_to_int[char] for char in given])
    y.append(char_to_int[predict])

#将x转变为LSTM所需的形式,[样本,时间长度，特征]
n_pattern=len(x)
n_vocab=len(chars)
x=np.reshape(x,(n_pattern,seq_length,1))

#将x标准化
x=x/float(n_vocab)

#将y转化为one-hot形式
y=np_utils.to_categorical(y)

#建立LSTM模型
model=Sequential()
model.add(LSTM(100,input_shape=(x.shape[1],x.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1],activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer='adam')
model.fit(x,y,nb_epoch=50,batch_size=2000)

#预测
def string_to_index(input_string):
    res=[]
    for i in input_string[len(input_string)-seq_length:]:
        res.append(char_to_int[i])
    return res

def predict_next(input_array):
    x=np.reshape(input_array,[1,seq_length,1])
    x=x/float(n_vocab)
    y=model.predict(x)
    return y

def y_to_char(y):
    pred=y.argmax()
    y=int_to_char[pred]
    return y

def generate_article(input_string,rounds=200):
    input_string=input_string.lower()
    for i in range(rounds):
        c=y_to_char(predict_next(string_to_index(input_string)))
        input_string+=c
    return input_string

init = 'His object in coming to New York was to engage officers for that service. He came at an opportune moment'
article = generate_article(init)
print(article)