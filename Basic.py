import tensorflow as tf

#tf.constant : 말 그대로 상수입니다

hello = tf.constant('hello, Tensorflow!')

print(hello)


a = tf.constant(10)
b = tf.constant(20)

c = tf.add(a, b)

print(c) 

sess = tf.Session()

print(sess.run(hello))
print(sess.run([a,b,c]))

sess.close()
