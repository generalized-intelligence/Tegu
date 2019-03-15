#encoding=utf-8
"""
Retrain the YOLO model for your own dataset.
"""
import keras.backend as K
K.set_image_data_format('channels_last')
import tensorflow as tf
import keras.backend.tensorflow_backend as ktf

import colorsys
def get_session(gpu_fraction=0.99):
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction,
                                allow_growth=True)
    return tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
ktf.set_session(get_session())

import os

import numpy as np
from PIL import Image
from keras.layers import Input, Lambda
from keras.models import load_model, Model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping

from Network.YOLOv3.yolo3.model import preprocess_true_boxes, yolo_eval, yolo_body, yolo_loss, tiny_yolo_body
import Network.YOLOv3.train as train

from PIL import Image, ImageFont, ImageDraw

import cv2
import random
from Util.decrypt import decrypt_txt_file


class YOLOv3_Model:
    def __init__(self,class_count=3,lr=0.0001, freeze_body=185):
        '''
        Management training and predict.
        Parameters are hyperparameters that allow adjustments.

        Args:
            class_count -- number of categories to identify.
            lr -- learning rate
            freeze_body -- layers to freeze.(default 185)

        '''
        self.YOLO_ANCHORS = np.array(((10,13), (16,30), (33,23), (30,61),
                                           (62,45), (59,119), (116,90), (156,198), (373,326)))
        self.class_names = None                                
        self.log_dir = 'D:/logs/000/'
        self.model_path=None
        self.sess = K.get_session()
        self.evalready=False
        self.class_count=class_count
        self.score = 0.1
        self.iou = 0.1
        self.lr=lr
        self.input_shape = (416,416) # multiple of 32  # <- shut up, you son of bitch.
        self.anchors_path =  r'Network\yolo3\model_data\yolo_anchors.txt'
        self.anchors = train.get_anchors(self.anchors_path)        
        self.dataset = None
        self.freeze_body = freeze_body
        self.infer_model,self.model = train.create_model(self.input_shape, self.anchors, self.class_count,
                                                            load_pretrained=True, freeze_body=self.freeze_body)
        self.weights=self.infer_model.get_weights()
        # self.model.compile(optimizer=Adam(lr=self.lr), loss={
        #     # use custom yolo_loss Lambda layer.
        #     'yolo_loss': lambda y_true, y_pred: y_pred})

        # self.update_params_and_compile(self.lr)
        
        self.model.compile(optimizer=Adam(lr=self.lr), loss={
            # use custom yolo_loss Lambda layer.
            'yolo_loss': lambda y_true, y_pred: y_pred})

        self.logging = TensorBoard(log_dir=self.log_dir)
        #self.checkpoint = ModelCheckpoint(log_dir + "ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5",
        #                                    monitor='val_loss', save_weights_only=True, save_best_only=True)
    
    def reload_weights(self):
        # self.model.set_weights(self.weights)
        self.infer_model.set_weights(self.weights)

    def update_params_and_compile(self,lr,freeze_body=None):
        self.lr=lr
        if(freeze_body is None):
            freeze_body=self.freeze_body
        else:
            self.freeze_body=freeze_body
        for i in range(len(self.infer_model.layers)-77,len(self.infer_model.layers)-3):
            self.infer_model.layers[i].trainable = not freeze_body
        print(freeze_body)

        self.model.compile(optimizer=Adam(lr=lr), loss={
            # use custom yolo_loss Lambda layer.
            'yolo_loss': lambda y_true, y_pred: y_pred})

        
    def get_eval_model(self):
        '''Load prediction model.'''
        if(not self.model_path==None):
            model_path = os.path.expanduser(self.model_path)
            self.infer_model.load_weights(model_path)
            print('{} model weights loaded.'.format(model_path))

        if (self.evalready==False):
            # Generate colors for drawing bounding boxes.
            hsv_tuples = [(x / len(self.class_names), 1., 1.)
                        for x in range(len(self.class_names))]
            self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
            self.colors = list(
                map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                    self.colors))
            random.seed(10101)  # Fixed seed for consistent colors across runs.
            random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
            random.seed(None)  # Reset seed to default.

            # Generate output tensor targets for filtered bounding boxes.
            self.input_image_shape = K.placeholder(shape=(2, ))
            self.boxes,self.scores,self.classes = yolo_eval(self.infer_model.output, self.anchors,
                    len(self.class_names), self.input_image_shape,
                    score_threshold=self.score, iou_threshold=self.iou)
            # boxes, scores, classes = yolo_eval(self.infer_model.output, self.anchors,
            #     len(self.class_names), self.input_image_shape,
            #     score_threshold=self.score, iou_threshold=self.iou)
            self.evalready=True
      


    def set_dataset(self,dataset):
        self.dataset = dataset
        assert dataset.input_shape == self.input_shape
        self.class_names = self.dataset.class_names


    def train(self):  
        '''Train the model one epoch every time.'''
        print('Start training.')
        history = self.model.fit_generator(self.dataset.generate_train(), self.dataset.train_batches,
                              1, verbose=1,#callbacks=callbacks,
                            #   validation_data=self.gen.generate_vaild(),
                            #   nb_val_samples=self.gen.val_batches,
                              nb_worker=1)
        return history


    def predict(self,img_path,model_path=None, anno_path=None):
        '''
        Predict one image.
        Return: [label, class_name, score, (left, top), (right, bottom)]

        Args:
            img_path -- The image path to be predicted.
            model_path -- Yolov3 model path for prediction.
        '''
        if self.class_names is None:
            assert anno_path is not None, "Set class names first."
            _, contents = decrypt_txt_file(anno_path)
            contents = contents.split('\n')
            self.class_names = contents[1].split(',')
            self.class_names = [cn.split(':')[1] for cn in self.class_names]

        if(self.evalready==False or not self.model_path==model_path):
            self.model_path=model_path
            self.get_eval_model()          
            print("(re)loading eval/infering model")
        
        try:
            image=np.asarray(Image.open(img_path)) #.swapaxes(0,1)
        except Exception as e:
            print('open wrong :',e)
            return None
        boxed_image = letterbox_image(image, tuple(reversed((416, 416))))
        image_data = np.array(boxed_image, dtype='float32')

        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.infer_model.input: image_data,
                self.input_image_shape: [image.shape[1], image.shape[0]],
                K.learning_phase(): 0
            })
        image=Image.open(img_path)
        result = []
        for i, c in reversed(list(enumerate(out_classes))):
            if c==0:
                pass
            class_name = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]
            score = '{:.4f}'.format(score)
            top, left, bottom, right = box
            y_pad=(image.size[0]-image.size[1])/2
            x_pad=(image.size[1]-image.size[0])/2
            top = max(0, np.floor(top + 0.5-y_pad).astype('int32'))
            left = max(0, np.floor(left + 0.5-x_pad).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5-y_pad).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5-x_pad).astype('int32'))
            result.append([c, class_name, score, (left, top), (right, bottom)])
        return result

class YOLOv3_Dataloader:
    def __init__(self,data_path, anno_path, max_boxes=128,batch_size=8,extra_params=None):
        '''
        Manager of YOLOv3 datasets.

        Args:
            max_boxes -- Take the first num of the annotations for training.(default 128)
            anno_path -- Path of annotation file.
            batch_size -- Num of one batch.(default 8)
            data_path -- Path of dataset
            extra_params -- Custom parameter.
        '''

        self.data_path = data_path
        self.anno_path = anno_path

        _,content = decrypt_txt_file(self.anno_path)
        content=content.split("\n")
        clses=content[1]
        annos=content[2:]
        self.class_names=[x.split(":")[1] for x in clses.split(",")]
    
        self.input_shape = (416,416)
        self.files=[]
        self.boxes=[]
        for line in annos:
            x=line.split(":")
            if(len(x)==1) or x[1]=='':
                continue
            file=os.path.join(self.data_path,x[0])
            self.files.append(file)
            
            x=list(map(int,x[1].split(",")))
            box=np.zeros((max_boxes,5),dtype='int32')
            i=0
            while(len(x)>0 and i<max_boxes):
                box[i]=np.array([x[1],x[2],x[3],x[4],x[0]])
                x=x[5:]; i=i+1
            image_size=np.asarray(Image.open(file).size)
            new_size = (image_size * np.min(self.input_shape/image_size)).astype('int32')
            box[:i+1, 0:2] = (box[:i+1, 0:2]*new_size/image_size + (self.input_shape-new_size)/2).astype('int32')
            box[:i+1, 2:4] = (box[:i+1, 2:4]*new_size/image_size + (self.input_shape-new_size)/2).astype('int32')
            self.boxes.append(box)
        
        print('Dataloader input_shape must be the same as model input shape.Asserted in yolo model class')
        self.anchors_path =  r'Network\yolo3\model_data\yolo_anchors.txt'
        self.anchors = train.get_anchors(self.anchors_path)
    
        self.y_true= preprocess_true_boxes(self.boxes, self.input_shape, self.anchors, len(self.class_names))
        print(len(self.y_true[2]))
        print(type(self.y_true[2]))
        print(self.y_true[2].shape)
        print(self.y_true[0].shape)
        print(self.y_true[1].shape)
        
        
        self.y_true3  = self.y_true[2]#.tolist()
        self.y_true2 = self.y_true[1]#.tolist()
        self.y_true1 = self.y_true[0]#.tolist()

        #print((type(self.image_data),type(self.box_data),type(self.y_true)))
        print ((len(self.files),len(self.boxes),len(self.y_true1)   ))
        #print ('y_true.shape',self.y_true.shape)
        print ('y_true[0]',self.y_true[0].shape)
        assert(len(self.files) == len(self.boxes)) and (len(self.boxes)==len(self.y_true1))

        zipped_list = list(zip(self.files,self.boxes,self.y_true1,self.y_true2,self.y_true3))

        random.shuffle(zipped_list)  # Ensure that images are shuffled.This is important!!
        print('Dataset_shuffled!')
        total_num = len(zipped_list)
        print('Train ratio:0.9.This ratio can be changed.')
        # train_num = int(total_num * 0.8)
        train_num = int(total_num * 0.9)
        test_num = total_num - train_num
        assert test_num > 0
        self.image_train,self.box_train,self.y_train1,self.y_train2,self.y_train3 = zip(*(zipped_list[:train_num]))
        self.image_test,self.box_test,self.y_test1,self.y_test2,self.y_test3 = zip(*(zipped_list[-test_num:]))

        # self.y_train = [self.y_train1,self.y_train2,self.y_train3]
        # self.y_test = [self.y_test1,self.y_test2,self.y_test3]
        self.image_train,self.box_train = map(np.array,[self.image_train,self.box_train])
        # self.y_train,self.y_test = map(lambda x:np.array(x),self.y_train),map(lambda x:np.array(x),self.y_test)
        
        self.image_test,self.box_test = map(np.array,[self.image_test,self.box_test])

        self.batch_size=batch_size
        self.train_batches = (len(self.image_train)-1)//batch_size+1
        # self.y_train = tuple(self.y_train)
        # self.y_test = tuple(self.y_test)
        # print(('items are:-----------',self.image_test,self.box_test,self.y_test))

    def generate_train(self):
        '''Training set generator.'''
        batch_size=self.batch_size
        ret1=[]
        ret2=[]
        ret3=[]
        ret4=[]
        ret5=[]
        for im,box,y1,y2,y3 in zip(self.image_train,self.box_train,self.y_train1,self.y_train2,self.y_train3):
            try:
                ret1.append(letterbox_image(np.asarray(Image.open(im)),self.input_shape)/255)
            except:
                from PIL.Image import open as op2
                print(im)
                op2(im)
                continue
            ret2.append(box)
            ret3.append(y1)
            ret4.append(y2)
            ret5.append(y3)
            if(len(ret1)==batch_size):
                img_data = np.array(ret1,dtype="float")
                yield [img_data,np.array(ret3,dtype="float"),np.array(ret4,dtype="float"),np.array(ret5,dtype="float")], np.zeros(len(img_data))
                ret1=[]
                ret2=[]
                ret3=[]
                ret4=[]
                ret5=[]
        if(not len(ret1)==0):
            img_data = np.array(ret1,dtype="float")
            yield [img_data,np.array(ret3,dtype="float"),np.array(ret4,dtype="float"),np.array(ret5,dtype="float")], np.zeros(len(img_data))
            
    def generate_vaild(self):
        '''validation set generator.'''
        batch_size=self.batch_size
        ret1=[]
        ret2=[]
        ret3=[]
        ret4=[]
        ret5=[]
        for im,box,y1,y2,y3 in zip(self.image_test,self.box_test,self.y_test1,self.y_test2,self.y_test3):
            ret1.append(letterbox_image(np.asarray(Image.open(im)),self.input_shape)/255)
            ret2.append(box)
            ret3.append(y1)
            ret4.append(y2)
            ret5.append(y3)
            if(len(ret1)==batch_size):
                if(len(self.image_test)%batch_size==0):
                    break
                else:
                    img_data = np.array(ret1,dtype="float")
                    yield [img_data,np.array(ret2,dtype="float"),np.array(ret3,dtype="float"),np.array(ret4,dtype="float"),np.array(ret5,dtype="float")], np.zeros(len(img_data))
                    ret1=[]
                    ret2=[]
                    ret3=[]
                    ret4=[]
                    ret5=[]
        if(not len(ret1)==0):
            img_data = np.array(ret1,dtype="float")
            yield [img_data,np.array(ret2,dtype="float"),np.array(ret3,dtype="float"),np.array(ret4,dtype="float"),np.array(ret5,dtype="float")], np.zeros(len(img_data))

def letterbox_image(image, size):
    '''Resize image with unchanged aspect ratio using padding'''
    ih, iw = image.shape[:2]
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)
    image = cv2.resize(image, (nw,nh),interpolation= cv2.INTER_CUBIC) #.swapaxes(0,1)
    new_image = np.zeros((size[0],size[1],3),dtype="float")

    new_image[(size[0]-nh)//2:(size[0]+nh)//2,(size[1]-nw)//2:(size[1]+nw)//2,:]=image
    return new_image

