from keras import backend as K

def weighted_mse(y_true, y_pred):
    weight_vector_const_nparray = [0.52, 0.95,1.41] #user-defined weights based on frequency of each class  1/num_of_sec_of_each_class*100
    return K.mean(K.square(y_pred - y_true)*(weight_vector_const_nparray), axis=-1)
