#털과 날개가 있는지 없는지에 따라 포유류인지 조류인지 분류하는 신경망 모델

import tensorflow as tf
import numpy as np

#[털 날개]
x_data = np.array(
    [[0, 0], [1, 0], [1, 1], [0, 0], [0, 0], [0, 1]])

# [기타 포유류, 조류]
# 다음과 같은 형식을 one-hot 형식의 데이터라고 합니다.
y_data = np.array([
    [1, 0, 0], # 기타
    [0, 1, 0], # 포유류
    [1, 0, 0], # 조류
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, 1]
])

############
# 신경망 모델 구성
#############

X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

# 신경망은 2차원으로 [입력층(특성), 출력층(레이블)] -> [2, 3] 으로 정한다
W = tf.Variable(tf.random_uniform([2, 3], -1., 1.))

# bias 을 각각 각 레이어의 아웃풋 갯수로 설정한다.
# bias 은 아웃풋의 개수 즉 최종 결과값의 분류 갯수인 3으로 설정한다
b = tf.Variable(tf.zeros([3]))

#신경망에 가중치 W와 bias  b를 적용한다
L = tf.add(tf.matmul(X, W), b)

# 가중치와 bias 를 이용해 계산한 결과 값에
# 텐서플로우에서 기본적으로 제공하는 활성화 함수인 ReLU 함수를 적용한다
L = tf.nn.relu(L)

# 마지막으로 softmax 함수를 이용하여 출력값을 사용하기 쉽게 만듭니다
# softmax 함수는 다음처럼 결과값을 전체합이 1인 함수로 만들어주는 함수입니다
model = tf.nn.softmax(L)

# 신경합을 최적화하기 위한 비용 함수를 작성한다
# 각 개별 결과에 대한 합을 구한 뒤 평균을 내는 방식을 사용한다
# 전체 합이 아닌 개별 결과를 구한 뒤 평균을 내는 방식을 사용하기위애 axis 옵셥을 사용한다
# axis 옵션이 없으면 -1.09 처럼 총합인 스칼라 값으로 출력된다.
# 즉, 이것은 예측값과 실제값 사이의 확률 분포의 차이를 비용으로 계산한 것이며
#이것을 Cross -entropy 라고 한다
cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(model), axis=1))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train_op = optimizer.minimize(cost)

#####################
# 신경망 모델 학습
#####################
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

for step in range(1000):
    sess.run(train_op, feed_dict={X: x_data, Y: y_data})

    if (step + 1) % 10 == 0:
        print(step + 1, sess.run(cost, feed_dict={X: x_data, Y: y_data}))

################
# 결과 확인
# 0 : 기타 1:포유류 2: 조류
# tf.arg_max: 예측값과 실제값의 행렬에서 tf.argmax 를 이용해 가장 큰 값을 가져옵니다
# 예) [[0 1 0], [1, 0, 0]] -> [1 0]
# [[0.2 0.7 0.1] [0.9 0.1 0.]] -> [1 0]
precondition = tf.argmax(model, 1)
target = tf.argmax(Y, 1)
print('예측 값 : ', sess.run(precondition, feed_dict={X: x_data}))
print('실제 값 : ', sess.run(target, feed_dict={Y: y_data}))

is_correct = tf.equal(precondition, target)
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
print('정확도: %.2f' % sess.run(accuracy * 100, feed_dict={X: x_data, Y: y_data}))