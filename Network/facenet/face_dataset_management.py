#encoding=utf-8
import cv2
import numpy as np
from scipy.spatial import KDTree # can be replaced by :from scipy.spatial import cKDTree as KDTree; Cython needed.
import Network.facenet.facenet.facenet as facenet

import time
import tensorflow as tf
import pyquaternion
import multiprocessing
SIMILAR_THRES = 0.8 #1.0

class face_manager: 
    def __init__(self):
        self.name_to_face_vec_list = {}
        self.name_to_face_img_list = {}
        '''
        for example:
            username1:[face_vec1,face_vec2,face_vec3,....]
        '''
        #self.pca_processed_name_to_face_vec_list = {}
        self.kd_tree = None
        self.vec_to_name_dict = {}
        self.vec_list = None
        self.name_list = None
        self.similar_threshold = SIMILAR_THRES
    def build_kdtree(self):
        #step1 build inversed mapping.
        self.vec_list = []
        self.name_list = []
        for name in self.name_to_face_vec_list:
            for vec in self.name_to_face_vec_list[name]:
                self.vec_to_name_dict[vec] = name
                self.vec_list.append(np.array(vec))
                self.name_list.append(name)
        vec_mat = np.array(self.vec_list)
        self.kd_tree = KDTree(vec_mat)

    def add_name_and_img(self,name,cv_img_bgr_origin):
        from Network.facenet.get_face_vec import get_vec_from_cvimg
        # if self.name_to_face_img_list.has_key(name):
        if name in self.name_to_face_img_list.keys():
            self.name_to_face_img_list[name].append(cv_img_bgr_origin)
            self.name_to_face_vec_list[name].append(get_vec_from_cvimg(cv_img_bgr_origin))
        else:
            self.name_to_face_img_list[name] = [cv_img_bgr_origin]
            self.name_to_face_vec_list[name] = [get_vec_from_cvimg(cv_img_bgr_origin)]

    def query_name_by_img(self,cv_img_bgr_origin):
        if self.kd_tree is None:
            self.build_kdtree()
        from Network.facenet.get_face_vec import get_vec_from_cvimg
        vec = get_vec_from_cvimg(cv_img_bgr_origin)
        similar_vecs = self.kd_tree.query_ball_point(vec,self.similar_threshold)
        similar_vecs = map(lambda x:np.array(x),similar_vecs)
        if len(similar_vecs)>0:
            if len(similar_vecs) == 1:
                return self.name_list[int(similar_vecs[0])]  # one match.return it.
            elif len(similar_vecs)>1:
                min_dist,min_id = self.similar_threshold+1,0  # ensures that any of them smaller than THRES+1.
                for i in range(len(similar_vecs)):
                    dist = np.sqrt(np.sum(np.square(np.array(similar_vecs[i]) - np.array(vec))))
                    if dist <min_dist:
                        min_dist = dist
                        min_id = i
                print ('similar_vecs',similar_vecs)
                return self.name_list[int(similar_vecs[min_id])]
        else:
            return None  # no matching.
    def query_nearest_by_img(self,cv_img_bgr_origin,return_score=False):
        if self.kd_tree is None:
            self.build_kdtree()
        from Network.facenet.get_face_vec import get_vec_from_cvimg
        time0 = time.time()
        vec = get_vec_from_cvimg(cv_img_bgr_origin)
        time1 = time.time()
        dist,nearest_vec_id = self.kd_tree.query([vec])
        time2 = time.time()
        print ('vec calc time cost:',time1-time0)
        print ('kdtree query time cost:',time2-time1)
        dist,nearest_vec_id = dist[0],nearest_vec_id[0]
        print ('dist square:',dist*dist)
        if dist*dist < self.similar_threshold:
          if return_score:
            return self.name_list[nearest_vec_id],dist*dist
          else:
            return self.name_list[nearest_vec_id]
        else:
          if return_score:
            return None,None
          else:
            return None



marker_id = 0

def build_face_maneger(db_path):
    #multiprocessing.freeze_support()
    import mxnet_mtcnn_face_detection.main
    # db_absolute_path = '/home/gi/gi_beijing_face/indexed'
    db_absolute_path = db_path
    fm = face_manager()
    i = 0
    import os

    for name in os.listdir(db_absolute_path):
        for pic_path in os.listdir(os.path.join(db_absolute_path,name)):
            pic_full_path = os.path.join(db_absolute_path,name,pic_path)
            img_origin = cv2.imread(pic_full_path)
            print('img_origin.shape:',img_origin.shape)
            img_resized = cv2.resize(img_origin,(int(img_origin.shape[1]/10),int(img_origin.shape[0]/10)))
            print('img_resized.shape:',img_resized.shape)
            results = mxnet_mtcnn_face_detection.main.detector.detect_face(img_resized)
            if results is not None:
                '''
                total_boxes = results[0] # bboxes: numpy array, n x 5 (x1,y1,x2,y2,score)
                points = results[1]
                if total_boxes.shape[0] ==1:
                    crop = face_crop(total_boxes[0],img_resized)
                    fm.add_name_and_img(name,crop)
                    cv2.imwrite(os.path.join("debug",name+'_'+str(i)+"_origin.jpg"),crop)
                    i+=1
 
                    fm.add_name_and_img(name,crop)
                    cv2.imwrite(os.path.join("debug",name+'_'+str(i)+"_origin.jpg"),crop)
                    i+=1
                    print ('name:',name,'crop shape:',crop.shape)
                   
                '''
                total_boxes = results[0] # bboxes: numpy array, n x 5 (x1,y1,x2,y2,score)
                points = results[1]

                chips = mxnet_mtcnn_face_detection.main.detector.extract_image_chips(img_resized, points, 200, 0.48)#0.37)
                if len(chips) ==  1:
                    fm.add_name_and_img(name,chips[0])
                    cv2.imwrite(os.path.join("debug",name+'_'+str(i)+"_origin.jpg"),chips[0])
                    i+=1
                    print ('name:',name,'crop shape:',chips[0].shape)

                #'''
                print ('total_boxes.shape',total_boxes.shape)
    print ('building kdtree!')
    fm.build_kdtree()
    print ('kdtree building finished!')

def detetion_and_recongnize(test_path):
    test_path_list = map(lambda x:os.path.join(test_path,x),os.listdir(test_path))
    test_index = 0
    for path in test_path_list:
      time1 = time.time()
      img = cv2.imread(path)
      print (img.shape)
      newy,newx = img.shape[1]//3,img.shape[0]//3
      if img.shape[0]>2000:
          newy,newx = img.shape[1]//10,img.shape[0]//10
      img2 = cv2.resize(img,(newy,newx))
      print (img2.shape)
      time2 = time.time()
      results = mxnet_mtcnn_face_detection.main.detector.detect_face(img2)
      print ('matching...')
      print ('results',results)
      time3 = time.time()
      if results is not None:
        total_boxes = results[0]
        points = results[1]
        time4 = time.time()
        #'''
        chips = mxnet_mtcnn_face_detection.main.detector.extract_image_chips(img2, points, 144, 0.37)
        time5 = time.time()
        for i, chip in enumerate(chips):
            #cv2.imshow('chip_'+str(test_index), chip)
            cv2.imwrite('chip_'+str(test_index)+'.jpg',chip)
            #name = fm.query_name_by_img(chip)
            time6 = time.time()
            name = fm.query_nearest_by_img(chip)
            time7 = time.time()
            if name is None:
                name = 'Not found'
            print('chip_'+str(test_index)+':'+name)
            test_index+=1
            #cv2.waitKey(0)
      time_end = time.time()
      print ('time_cost:',time_end-time1,'s per image')
      print ('img read and reshape cost:',time2-time1)
      print ('face detection time cost:',time3-time2)
      print ('extract crops cost:',time5-time4)
      print ('each face crop match cost',time7-time6)


    print (fm.name_list)

