#encoding=utf-8

import cv2
import keras
from keras.applications.imagenet_utils import preprocess_input
from keras.backend.tensorflow_backend import set_session
from keras.models import Model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
import pickle
from random import shuffle
# from scipy.misc import imread
# from scipy.misc import imresize
import tensorflow as tf
import os
from Util.enhance import random_sized_crop
from Network.SSD300.ssd import SSD300
from Network.SSD300.ssd_training import MultiboxLoss
from Network.SSD300.ssd_utils import BBoxUtility
from Util.metrics import evaluate_detections
from Util.mylogger import MyLogger
from Util.decrypt import decrypt_txt_file

# %matplotlib inline
plt.rcParams['figure.figsize'] = (8, 8)
plt.rcParams['image.interpolation'] = 'nearest'

np.set_printoptions(suppress=True)

# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.9
# set_session(tf.Session(config=config))
__MODE__ = 'RELEASE'#'RELEASE'
def debug_print(x):
    if __MODE__ =='DEBUG':
        print(x)

class SSD_Model:
    def __init__(self,class_count=4, input_shape=(300, 300, 3),lr = 3e-4, num_freeze_layer=11):
        '''
        Management of training and predict.
        Parameters are hyperparameters that allow adjustments.

        Args:
            class_count -- number of categories to identify.
            input_shape -- The shape of input data to resized.
            lr -- learning rate
            num_freeze_layer -- The number of layer to be freeze.
        '''
        self.class_names = None
        self.class_count = class_count
        self.input_shape = input_shape
        self.name = 'SSD300'
        self.lr = lr
        self.num_freeze_layer = num_freeze_layer
        print('Freeze:',num_freeze_layer)    

        if os.path.exists(os.path.join('Network','SSD300','prior_boxes_ssd300.pkl')):
            priors = pickle.load(open(os.path.join('Network','SSD300','prior_boxes_ssd300.pkl'), 'rb'))
            print('Priors load success.')
        self.bbox_util = BBoxUtility(self.class_count, priors)
        # path_prefix = '../../frames/'

        self.model = SSD300(input_shape, num_classes=self.class_count)
        if os.path.exists(os.path.join('Network','SSD300','weights_SSD300.hdf5')):
            self.model.load_weights( os.path.join('Network','SSD300','weights_SSD300.hdf5'), by_name=True)
            print('Load pre-trained weights success')
        
        layers = ['input_1', 'conv1_1', 'conv1_2', 'pool1',
                'conv2_1', 'conv2_2', 'pool2',
                'conv3_1', 'conv3_2', 'conv3_3', 'pool3',
                'conv4_1', 'conv4_2', 'conv4_3', 'pool4']
        
        freeze = layers[:num_freeze_layer]

        self.batch_size=4
        for L in self.model.layers:
            if L.name in freeze:
                L.trainable = False
        self.gt_info_test = None

        # def schedule(epoch, decay=0.9):
        #     return base_lr * decay**(epoch)

        # callbacks = [keras.callbacks.ModelCheckpoint('./checkpoints/weights.{epoch:02d}-{val_loss:.2f}.hdf5',
        #                                             verbose=1,
        #                                             save_weights_only=True),
        #             keras.callbacks.LearningRateScheduler(schedule)]

        optim = keras.optimizers.Adam(lr=lr)
        # optim = keras.optimizers.RMSprop(lr=base_lr)
        # optim = keras.optimizers.SGD(lr=base_lr, momentum=0.9, decay=decay, nesterov=True)
        self.model.compile(optimizer=optim,loss=MultiboxLoss(self.class_count, neg_pos_ratio=2.0).compute_loss)

    

    def set_dataset(self, dataset):
        self.dataset = dataset
        self.train_keys = dataset.train_keys
        self.val_keys = dataset.val_keys
        self.class_count = dataset.class_count
        self.class_names = dataset.class_names
        self.gt_boxes = dataset.gt_boxes
        self.dataset.bbox_util = self.bbox_util
        self.data_path = dataset.data_path
        self.serval_path = dataset.anno_path
        

    def train(self):  # Train on the whole train set batch for once.
        print('Start training.')
        assert self.dataset.bbox_util is not None, 'Set dataset before start training.'
        history = self.model.fit_generator(self.dataset.generate_train(), self.dataset.train_batches,
                              1, verbose=2,#callbacks=callbacks,
                              validation_data=self.dataset.generate_vaild(),
                              nb_val_samples=self.dataset.val_batches,
                              nb_worker=1)
        return history


    def get_gt_info_test(self):
        '''for metrics, get annotation info. '''
        if self.gt_info_test==None:
            self.gt_info_test = {}
            for k in self.class_names[1:]:
                self.gt_info_test[k] = []
            for name in self.val_keys:
                gt = self.gt_boxes[name]
                gt.astype(float)
                for k in self.gt_info_test.keys():
                    self.gt_info_test[k].append({'bbox':[],'det':[],'difficult':[]})
                for x in gt:
                    if x[4]==0:
                        continue
                    self.gt_info_test[self.class_names[x[4]]][-1]['bbox'].append(x)
                    self.gt_info_test[self.class_names[x[4]]][-1]['det'].append(False)
                    self.gt_info_test[self.class_names[x[4]]][-1]['difficult'].append(False)
            return self.gt_info_test
        else:
            return self.gt_info_test

    def metrics(self, model_path):
        '''Get mAP, recall, precision // Return: {'mAP':., 'rec':., 'prec':.}'''
        self.gt_val_keys = [os.path.join(self.data_path, l) for l in self.val_keys]
        all_boxes = [[[] for _ in range(len(self.val_keys))] for _ in range(len(self.class_names))]
        print('Val key length:',len(self.gt_val_keys))
        for img_i, test_img_path in enumerate(self.gt_val_keys):
            
            test_result = self.predict(img_path=test_img_path, model_path=model_path,is_metrics=True)
            print('Finish predict the {} val image for metrics.'.format(img_i))
            #print('test_result:',test_result)
            test_result.sort(key=lambda x:float(x[4]), reverse=True)
            if len(test_result) > 58:
                test_result = test_result[:58]
            img_obj_out = image.load_img(test_img_path, target_size=(300, 300))
            img_obj_out = image.img_to_array(img_obj_out)
            for obj in test_result:
                if obj[-1]>0:
                    cv2.rectangle(img_obj_out, (int(obj[0]),int(obj[1])), (int(obj[2]),int(obj[3])), (255,0,0), 2)
            cv2.imwrite(os.path.join('./test_img_output/',os.path.split(test_img_path)[-1]),img_obj_out)
            if len(test_result)==0:
                for cls_j in range(1,len(self.class_names)):
                    all_boxes[cls_j][img_i] = np.asarray([]).reshape(0,5).astype(np.float32,copy=False)
                continue # fix bug of line 151 shape error.

            test_result = np.asarray(test_result)
            for cls_j in range(1,len(self.class_names)):
                #print ('test_result.shape:',test_result.shape)
                coords_and_label = test_result[np.where(test_result[:,-1]==cls_j)]
                all_boxes[cls_j][img_i] = coords_and_label[:,:-1].astype(np.float32, copy=False)   
        all_gt_infos = self.get_gt_info_test().copy()
        mAp,rec,prec = evaluate_detections(all_boxes, all_gt_infos, self.class_names )
        return {'mAP':mAp, 'rec':rec, 'prec':prec}
        
    def visualize_val_set(self, save_dir, model_path):
        '''Visualize val set when training model'''
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for name in self.val_keys:
            path = os.path.join(self.data_path,name)
            test_result = self.predict(img_path=path, model_path=model_path,is_metrics=True)
            test_result.sort(key=lambda x:float(x[4]), reverse=True)
            if len(test_result) > 58:
                test_result = test_result[:58]
            img = cv2.imread(path)
            for rec in test_result:
                cv2.rectangle(img, (rec[0],rec[1]),(rec[2],rec[3]),(255,0,0),thickness=2)
            cv2.imwrite(os.path.join(save_dir,name),img)

    def predict(self,img_array=None,img_path=None, model_path=None,is_metrics=False, visualize_path=None, anno_path=None):
        '''
        Predict one image.
        Return: 
            for just predict one image: [label, class_name, score, (left, top), (right, bottom)]
            for matrics: [xmin,ymin,xmax,ymax,score,label]
        Args:
            img_array -- None when img_path is not None. Image numpy array.[width, hight, channel]
            img_path -- None when img_array is not None. Image abs path.
            model_path -- SSD300 model path for prediction.
            is_metrics -- Is get info to do metrics when training.(False when you just predict image)
            visualize_path -- Visualize path.(Not None if you want to visualize image prediction results)
        '''
        if model_path is not None:
            self.model.load_weights(model_path)
        if self.class_names is None:
            assert anno_path is not None, "Set class names first."
            _, contents = decrypt_txt_file(anno_path)
            contents = contents.split('\n')
            self.class_names = contents[1].split(',')
            self.class_names = [cn.split(':')[1] for cn in self.class_names]
        inputs = []
        images = []
        try:
            if not img_path==None:
                img = cv2.imread(img_path)
                img = cv2.resize(img,(300,300),interpolation=cv2.INTER_NEAREST)
                images.append(cv2.cvtColor(cv2.imread(img_path),cv2.COLOR_BGR2RGB))
                images.append(cv2.imread(img_path))
                
                inputs.append(img.copy())
                inputs = preprocess_input(np.array(inputs))
            else:
                print('go')
                img = img_array.copy()
                img = cv2.resize(img,(300,300),interpolation=cv2.INTER_NEAREST)
                images.append(img_array)
                inputs.append(img.copy())
                inputs = preprocess_input(np.array(inputs))
        except Exception as e:
            print('img_path wrong:',e)
            return []
        
        
        preds = self.model.predict(inputs, batch_size=1, verbose=0)
        results = self.bbox_util.detection_out(preds)
        
        if len(results[0])==0:
            return []
        elif len(results)==0:
            return []

        result = []

        if not visualize_path==None:
            img_name = img_path.split(os.sep)[-1]
            print('new visual dir')
            if not os.path.exists(visualize_path):
                print('make new visual dir')
                os.mkdir(visualize_path)
            save_path = os.path.join(visualize_path, img_name)
        for i, img in enumerate (images):
            # Parse the outputs.
            det_label = results[i][:, 0]
            det_conf = results[i][:, 1]
            det_xmin = results[i][:, 2]
            det_ymin = results[i][:, 3]
            det_xmax = results[i][:, 4]
            det_ymax = results[i][:, 5]

            # Get detections with confidence higher than 0.6.
            top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.6]

            top_conf = det_conf[top_indices]
            top_label_indices = det_label[top_indices].tolist()
            top_xmin = det_xmin[top_indices]
            top_ymin = det_ymin[top_indices]
            top_xmax = det_xmax[top_indices]
            top_ymax = det_ymax[top_indices]


            for i in range(top_conf.shape[0]):
                xmin = int(round(top_xmin[i] * img.shape[1]))
                ymin = int(round(top_ymin[i] * img.shape[0]))
                xmax = int(round(top_xmax[i] * img.shape[1]))
                ymax = int(round(top_ymax[i] * img.shape[0]))
                score = top_conf[i]
                label = int(top_label_indices[i])
                if not visualize_path==None:
                    print('rec')
                    cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(255,0,0),thickness=2)
                if is_metrics==False:
                    result.append([label,self.class_names[label], score, (xmin,ymin),(xmax,ymax)])
                else:   #just for metrics.
                    result.append([xmin,ymin,xmax,ymax,score,label])
            if not visualize_path==None:
                cv2.imwrite(save_path,img)
            print('Finish predict')
            return result
    
    

    

class SSD_DataLoader(object):
    def __init__(self, anno_path,data_path, bbox_util=None,
                 batch_size=8, 
                 image_shape=(300,300),
                 do_crop = True,
                 extra_params=None
                 ):
        '''
        Manager of SSD datasets.

        Args:
            anno_path -- Path of annotation file.
            batch_size -- Num of one batch.
            data_path -- Path of dataset.
            image_shape -- The shape of the image to be resized.
            extra_params -- Custom parameter.
        '''
        self.gt = self.serval_to_dict(anno_path, data_path)
        keys = list(self.gt.keys()).copy()
        import random
        random.shuffle(keys)
        num_train = int(round(0.9 * len(keys)))
        self.train_keys = keys[:num_train]
        self.val_keys = keys[num_train:]
        self.anno_path = anno_path
        self.bbox_util = bbox_util
        self.batch_size = batch_size
        self.data_path = data_path
        self.train_batches = (len(self.train_keys)-1)//self.batch_size+1
        self.val_batches = (len(self.val_keys)-1)//self.batch_size+1
        self.image_shape = image_shape
        self.do_crop = do_crop
        
    
    def generate_train(self):
        '''Training set generator.'''
        while True:
            shuffle(self.train_keys)
            keys = self.train_keys
            inputs = []
            targets = []
            for key in keys:
                img_path = os.path.join(self.data_path, key)         
                img = cv2.imread(img_path).astype('float32')
                if len(img.shape)<3:
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                y = self.gt[key].copy()
                if self.do_crop:
                    img, y = random_sized_crop(img, y)
                img = cv2.resize(img, self.image_shape).astype('float32')
                y = self.bbox_util.assign_boxes(y)
                inputs.append(img)                
                targets.append(y)
                if len(targets) == self.batch_size:
                    tmp_inp = np.array(inputs)
                    tmp_targets = np.array(targets)
                    inputs = []
                    targets = []
                    yield preprocess_input(tmp_inp), tmp_targets
            if(len(targets)>0):
                tmp_inp = np.array(inputs)
                tmp_targets = np.array(targets)
                yield preprocess_input(tmp_inp), tmp_targets    

    def generate_vaild(self):
        '''Validation set generator.'''
        while True:
            shuffle(self.val_keys)
            keys = self.val_keys
            inputs = []
            targets = []
            for key in keys:
                img_path = os.path.join(self.data_path, key)            
                img = cv2.imread(img_path).astype('float32')
                if len(img.shape)<3:
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                y = self.gt[key].copy()
                if self.do_crop:
                    img, y = random_sized_crop(img, y)
                img = cv2.resize(img, self.image_shape).astype('float32')
                y = self.bbox_util.assign_boxes(y)
                inputs.append(img)                
                targets.append(y)
                if len(targets) == self.batch_size:
                    tmp_inp = np.array(inputs)
                    tmp_targets = np.array(targets)
                    inputs = []
                    targets = []
                    yield preprocess_input(tmp_inp), tmp_targets
            if(len(targets)>0):
                tmp_inp = np.array(inputs)
                tmp_targets = np.array(targets)
                yield preprocess_input(tmp_inp), tmp_targets    
    
    def serval_to_dict(self, anno_path, data_path, max_box=128):
        '''Extract annotation info and do preprocessing'''
        contents = ''
        self.gt_boxes = {}      #for metrices
        
        _, contents = decrypt_txt_file(anno_path)
        lines = contents.split('\n')
        self.class_count = len(lines[1].split(','))
        self.class_names = lines[1].split(',')
        self.class_names = [cn.split(':')[1] for cn in self.class_names]

        gt = {}
        annos = lines[2:]
        for anno in annos:
            self.gt_boxes_per_img = np.zeros((max_box,5),dtype='int32')     #for matrics
            x = anno.split(':')
            if(len(x)==1) or x[1]=='':
                continue
            name = x[0]
            img = cv2.imread(os.path.join(data_path,name))
            try:
                width = img.shape[0]
                height = img.shape[1]
            except:
                continue
            x = list(map(lambda a:int(float(a)), x[1].split(',')))
            i=0
            boxes = []                        
            while len(x)>0 and i<max_box:
                box = []
                self.gt_boxes_per_img[i] = [x[1],x[2],x[3],x[4],x[0]]       #for metrics
                label = np.zeros(self.class_count)
                label[x[0]] = float(1)
                xmin = float(x[1])/width
                ymin = float(x[2])/height
                xmax = float(x[3])/width
                ymax = float(x[4])/height
                box = [xmin, ymin, xmax, ymax]
                box.extend(label[1:])
                boxes.append(box)
                x = x[5:]
                i+=1
            self.gt_boxes[name] = self.gt_boxes_per_img     #for metrics
            boxes = np.asarray(boxes,dtype='float64')
            gt[name] = boxes
        return gt     #{'name':[[x1,y1,x2,y2,0,0,1]]}
    