import tensorflow as tf

#保存模型
v1=tf.Variable(tf.random_normal([1,2],stddev=0.1))
v2=tf.Variable(tf.random_normal([2,3],stddev=0.1))
saver=tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(v1))
    print(sess.run(v2))
    saver.save(sess,r"C:\Users\T\Desktop\python视频\model\model.model")

#加载模型
with tf.Session() as sess:
    saver.restore(sess,r"C:\Users\T\Desktop\python视频\model\model.model")
    print(sess.run(v1))
    print(sess.run(v2))