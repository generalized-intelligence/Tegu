# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import scipy.misc
import cv2
from Network.facenet.facenet.facenet import load_model,prewhiten
import time
#image_size = 200 #don't need equal to real image size, but this value should not small than this
image_size = 160 #don't need equal to real image size, but this value should not small than this
modeldir = 'Network/facenet/model_file/20180408-102900' #change to your model dir
image_name1 = '/home/gi/face_dataset/lfw/Laura_Bush/Laura_Bush_0001.jpg' #change to your image name
image_name2 = '/home/gi/face_dataset/lfw/Laura_Bush/Laura_Bush_0002.jpg' #change to your image name

print('建立facenet embedding模型')
tf.Graph().as_default()

sess = tf.InteractiveSession()
#sess.as_default()cd


load_model(modeldir)

print('Model loaded!')


def get_vec_from_cvimg(cv_img_bgr_origin):
    image1 = cv2.cvtColor(cv_img_bgr_origin, cv2.COLOR_BGR2RGB)
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    embedding_size = embeddings.get_shape()[1]


    #scaled_reshape = []
    image1 = cv2.resize(image1, (image_size, image_size), interpolation=cv2.INTER_CUBIC)
    t1 = time.time()
    image1 = prewhiten(image1)
    #scaled_reshape.append(image1.reshape(-1,image_size,image_size,3))
    reshaped_tensor = image1.reshape(-1,image_size,image_size,3)
    emb_array = np.zeros( embedding_size)
    emb_array = sess.run(embeddings, feed_dict={images_placeholder: reshaped_tensor, phase_train_placeholder: False })[0]
    print ('Time cost:',time.time() - t1,'s')
    #print emb_array
    return tuple(emb_array)

    '''
    t1 = time.time()
    image2 = scipy.misc.imread(image_name2, mode='RGB')
    image2 = cv2.resize(image2, (image_size, image_size), interpolation=cv2.INTER_CUBIC)
    image2 = facenet.prewhiten(image2)
    scaled_reshape.append(image2.reshape(-1,image_size,image_size,3))
    emb_array2 = np.zeros((1, embedding_size))
    emb_array2[0, :] = sess.run(embeddings, feed_dict={images_placeholder: scaled_reshape[1], phase_train_placeholder: False })[0]
    print 'Time cost:',time.time() - t1,'s'


    dist = np.sqrt(np.sum(np.square(emb_array1[0]-emb_array2[0])))
    print("128维特征向量的欧氏距离：%f "%dist)'''

# get_vec_from_cvimg(np.zeros((200,200,3))) #preheat model.

if __name__ == '__main__':
    #for _ in range(10):
    print(get_vec_from_cvimg(cv2.imread(r"D:\backup\facenet\test\IMG_0963.JPG")))
