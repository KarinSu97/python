import tensorflow as tf
from captcha.image import ImageCaptcha
import random
from PIL import Image
import numpy as np

class crack_captch:
    def __init__(self,w_alpha,b_alpha,MAX_CAPTCHA):
        #定义网络随机数的倍数
        self.w_alpha=w_alpha
        self.b_alpha=b_alpha
        # 验证码文本长度
        self.MAX_CAPTCHA = MAX_CAPTCHA
        #图像大小
        self.IMAGE_HEIGHT = 60
        self.IMAGE_WIDTH = 160
        #验证码字符集
        self.number= ['0','1','2','3','4','5','6','7','8','9']
        #字符集长度
        self.char_set_len=len(self.number)
    #定义文本生成函数
    def random_captcha_text(self):
        charset=self.number
        captcha_size = self.MAX_CAPTCHA
        captcha_text=[]
        for i in range(captcha_size):
            captcha_text.append(random.choice(charset))
        return captcha_text
    #定义验证码生成函数
    def gen_captcha_text_and_image(self):
        image=ImageCaptcha()
        captcha_text=self.random_captcha_text()
        captcha_text=''.join(captcha_text)
        captcha=image.generate(captcha_text)
        captcha_image=Image.open(captcha)
        captcha_image=np.array(captcha_image)
        return captcha_text,captcha_image
    #定义验证码图像转化为灰度图函数
    def convert2gray(self,img):
        if len(img.shape)>2:
            gray=np.mean(img,-1)
            return gray
        else:
            return img
    #定义文本转one-hot函数
    def text2vec(self,text):
        vector=np.zeros(self.MAX_CAPTCHA*self.char_set_len)
        for i,c in enumerate(text):
            idx=i*self.char_set_len+int(c)
            vector[idx]=1
        return vector
    #定义one-hot转文本函数
    def vec2text(self,vec):
        text=[]
        vec=vec.nonzero()[0]
        for i in vec:
            number=i%10
            text.append(str(number))
        return ''.join(text)
    #定义生成batch函数
    def get_next_batch(self,batch_size):
        batch_x=np.zeros([batch_size,self.IMAGE_HEIGHT*self.IMAGE_WIDTH])
        batch_y=np.zeros([batch_size,self.MAX_CAPTCHA*self.char_set_len])
        #有时生成的图像不是60*160*3
        def wrap_gen_captcha_text_and_image():
            while True:
                text,image=self.gen_captcha_text_and_image()
                if image.shape==(60,160,3):
                    return text,image
        #生成指定batch大小的数据
        for i in range(batch_size):
            text,image=wrap_gen_captcha_text_and_image()
            image=self.convert2gray(image)
            #对数据进行规范化
            batch_x[i,:]=image.flatten()
            batch_y[i,:]=self.text2vec(text)
        return batch_x,batch_y
    #定义CNN网络结构
    def CNN(self,X,keep_prob):
        x=tf.reshape(X,[-1,self.IMAGE_HEIGHT,self.IMAGE_WIDTH,1])
        #卷积层
        wc1=tf.Variable(self.w_alpha*tf.random_normal([3,3,1,32]))
        bc1=tf.Variable(self.b_alpha*tf.random_normal([32]))
        conv1=tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x,wc1,strides=[1,1,1,1],padding='SAME'),bc1))
        conv1=tf.nn.max_pool(conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
        conv1=tf.nn.dropout(conv1,keep_prob=keep_prob)

        wc2 = tf.Variable(self.w_alpha * tf.random_normal([3, 3, 32, 64]))
        bc2 = tf.Variable(self.b_alpha * tf.random_normal([64]))
        conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, wc2, strides=[1, 1, 1, 1], padding='SAME'),bc2))
        conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv2 = tf.nn.dropout(conv2, keep_prob=keep_prob)

        wc3 = tf.Variable(self.w_alpha * tf.random_normal([3, 3, 64, 64]))
        bc3 = tf.Variable(self.b_alpha * tf.random_normal([64]))
        conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, wc3, strides=[1, 1, 1, 1], padding='SAME'),bc3))
        conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv3 = tf.nn.dropout(conv3, keep_prob=keep_prob)

        #全连接层
        wd1=tf.Variable(self.w_alpha*tf.random_normal([8*20*64,128]))
        bd1=tf.Variable(self.b_alpha*tf.random_normal([128]))
        conv3=tf.reshape(conv3,[-1,wd1.get_shape().as_list()[0]])
        hidden=tf.nn.relu(tf.add(tf.matmul(conv3,wd1),bd1))
        hidden=tf.nn.dropout(hidden,keep_prob)

        wd2=tf.Variable(self.w_alpha*tf.random_normal([128,self.MAX_CAPTCHA*self.char_set_len]))
        bd2=tf.Variable(self.b_alpha*tf.random_normal([self.MAX_CAPTCHA*self.char_set_len]))
        out=tf.add(tf.matmul(hidden,wd2),bd2)
        return out
    #定义训练函数
    def train(self):
        learn_rate=0.001
        X = tf.placeholder('float', [None, self.IMAGE_HEIGHT * self.IMAGE_WIDTH])
        Y = tf.placeholder('float', [None, self.MAX_CAPTCHA * self.char_set_len])
        keep_prob=tf.placeholder('float')
        output=self.CNN(X,keep_prob)
        #定义损失函数
        loss=tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output,labels=Y))
        #定义优化器
        optimizer=tf.train.AdamOptimizer(learning_rate=learn_rate).minimize(loss)
        #计算准确率
        max_idx_pred=tf.argmax(tf.reshape(output,[-1,self.MAX_CAPTCHA,self.char_set_len]),2)
        max_idx_real=tf.argmax(tf.reshape(Y,[-1,self.MAX_CAPTCHA,self.char_set_len]),2)
        pred=tf.equal(max_idx_pred,max_idx_real)
        acc=tf.reduce_mean(tf.cast(pred,'float'))
        #定义saver
        saver=tf.train.Saver()
        #开始迭代
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            step=0
            while True:
                batch_x,batch_y=self.get_next_batch(64)
                _,this_loss=sess.run([optimizer,loss],feed_dict={X:batch_x,Y:batch_y,keep_prob:0.5})
                print('step:',step,",loss:",this_loss)
                #每10次计算一次准确率
                if step%10==0:
                    batch_x_test, batch_y_test=self.get_next_batch(32)
                    this_acc=sess.run(acc,feed_dict={X:batch_x_test,Y:batch_y_test,keep_prob:1})
                    print('step:',step,",acc:",this_acc)
                    #如果准确率大于0.85,则保存模型，完成训练
                    if this_acc>0.50:
                        saver.save(sess,r"C:\Users\T\Desktop\python视频\model\crack_capcha.model",global_step=step)
                        print("----Finish train!----")
                        break
                    if step%10==0:
                        learn_rate*=0.95
                step+=1
    #定义预测函数
    def predict(self,x,model_path):
        X = tf.placeholder('float', [None, self.IMAGE_HEIGHT * self.IMAGE_WIDTH])
        Y = tf.placeholder('float', [None, self.MAX_CAPTCHA * self.char_set_len])
        output=self.CNN(x)
        predict=tf.argmax(tf.reshape(output, [-1, self.MAX_CAPTCHA,self.char_set_len]), 2)
        saver=tf.train.Saver()
        with tf.Session() as sess:
            saver.restore(sess,model_path)
            text_list=sess.run(predict,feed_dict={X:x})
            text = text_list[0].tolist()
            return "".join(text)

crack_captch_model=crack_captch(w_alpha=0.01,b_alpha=0.1,MAX_CAPTCHA=4)
crack_captch_model.train()
