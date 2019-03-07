#encoding=utf-8
from Network.facenet.face_dataset_management import face_manager
from scipy.spatial import KDTree
import cv2
import numpy as np 
# from Network.facenet.get_face_vec import get_vec_from_cvimg
import time
import tensorflow as tf 
import pyquaternion

import os
from Util.mylogger import MyLogger

SIMILAR_THRES = 0.8
marker_id = 0

def build_face_manager(face_db_path):#, info_que, cmd_que):
    '''
    Build face manager before detection and recognize faces.

    Args:
        face_db_path -- Faces dataset path.
                    /face_db_path
                        /people0
                            0.jpg...
                        /people1
                            0.jpg...
    '''
    import multiprocessing; multiprocessing.freeze_support()
    from Network.facenet.mxnet_mtcnn_face_detection.main import get_detector
    detector = get_detector()
    fm = face_manager()
    db_absolute_path = face_db_path
    i = 0
    # self.fm = fm
    try:
        # info_que.put('Start building face manager from {}'.format(db_absolute_path))
        print('Start building face manager from {}'.format(db_absolute_path))
        for name in os.listdir(db_absolute_path):
            print('Add {} to face manager...'.format(name))
            for pic_path in os.listdir(os.path.join(db_absolute_path,name)):
                
                pic_full_path = os.path.join(db_absolute_path,name,pic_path)
                img_origin = cv2.imread(pic_full_path)
                print('img_origin.shape:',img_origin.shape)
                img_resized = cv2.resize(img_origin,(int(img_origin.shape[1]/10),int(img_origin.shape[0]/10)))
                print('img_resized.shape:',img_resized.shape)
                results = detector.detect_face(img_resized)
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

                    chips = detector.extract_image_chips(img_resized, points, 200, 0.48)#0.37)
                    if len(chips) ==  1:
                        fm.add_name_and_img(name,chips[0])
                        #cv2.imwrite(os.path.join("debug",name+'_'+str(i)+"_origin.jpg"),chips[0])
                        i+=1
                        print ('name:',name,'crop shape:',chips[0].shape)

                    #'''
                    print ('total_boxes.shape',total_boxes.shape)
            print('Finish add {} to face manager...'.format(name))
        print ('Building kdtree!')
        fm.build_kdtree()
        print ('kdtree building finished!')
        return fm
        
    except Exception as e:
        print(e)


def detetion_and_recongnize(fm,data_path,similar_threshold=0.8):#,info_que,cmd_que):
    '''
    Detection and recongnize after built face manager.

    Args:
        similar_threshold -- The smaller the number, the stricter.(default 0.8)
        data_path -- Folder of the images to be detected and recongized.
    '''
    import multiprocessing; multiprocessing.freeze_support()
    fm.similar_threshold = similar_threshold
    from Network.facenet.mxnet_mtcnn_face_detection.main import get_detector
    detector = get_detector()
    test_path_list = map(lambda x:os.path.join(data_path,x),os.listdir(data_path))
    test_index = 0
    output_result = []
    result_dict = {}
    for path in test_path_list:
        if (path.lower().find('.png')<0 and path.lower().find('.jpeg')<0 and path.lower().find('.jpg')<0 and path.lower().find('.bmp')<0):
            continue
        time1 = time.time()
        img = cv2.imread(path)
        scale = 10
        print (img.shape)
        newy,newx = img.shape[1]//3,img.shape[0]//3
        if img.shape[0]>2000:
            newy,newx = img.shape[1]//10,img.shape[0]//10
        else:
            scale = 3
            newy,newx = img.shape[1]//3,img.shape[0]//3
        img2 = cv2.resize(img,(newy,newx))
        print (img2.shape)
        time2 = time.time()
        results = detector.detect_face(img2)
        print ('matching...')
        print ('results',results)
        time3 = time.time()
        print(path)
        result_dict[path] = []
        if True:
            if results is not None:
                total_boxes = results[0]
                points = results[1]
                time4 = time.time()
                #'''
                chips = detector.extract_image_chips(img2, points, 144, 0.37)
                time5 = time.time()
                for i, chip in enumerate(chips):
                    #cv2.imshow('chip_'+str(test_index), chip)
                    #cv2.imwrite('chip_'+str(test_index)+'.jpg',chip)
                    #name = fm.query_name_by_img(chip)
                    time6 = time.time()
                    name = fm.query_nearest_by_img(chip)
                    time7 = time.time()
                    if name is None:
                        name = 'Not found'
                    else:
                        # info_que.put([name,total_boxes[i][-1],list((total_boxes[i][:-1].astype('uint'))*scale)])
                        print([name,total_boxes[i][-1],list((total_boxes[i][:-1].astype('uint'))*scale)])
                        result_dict[path].append([name,total_boxes[i][-1],list((total_boxes[i][:-1].astype('uint'))*scale)])
                        # output_result.append([total_boxes[i][0])
                    print('chip_'+str(test_index)+':'+name)
                    test_index+=1
            time_end = time.time()
            print ('time_cost:',time_end-time1,'s per image')
            print ('img read and reshape cost:',time2-time1)
            print ('face detection time cost:',time3-time2)
            print ('extract crops cost:',time5-time4)
            print ('each face crop match cost',time7-time6)

        print (fm.name_list)
        return result_dict


def detetion_one_img(fm,img_array=None, img_path=None):    
    '''
    Detection one image.

    Args:
        img_array -- Numpy image numpy array.[width, hight, channel], None when img_path is not None
        img_path -- Image path you want to detect. None when img_array is not None
    '''
    try:
        print('Upload img:{}'.format(img_array.shape))
        # import multiprocessing; multiprocessing.freeze_support()
        time10 = time.time()
        
        detector = get_detector()
        test_index = 0
        result_list = []
        if True:
            time1 = time.time()
            img = None
            if img_array is not None:
                img = img_array
            else:
                img = cv2.imread(img_path)
            assert img is not None, "Open image wrong."
            scale = 10
            print (img.shape)
            if img.shape[0]>2000:
                newy,newx = img.shape[1]//10,img.shape[0]//10
            else:
                scale = 3
                newy,newx = newy,newx = img.shape[1]//3,img.shape[0]//3
            img2 = cv2.resize(img,(newy,newx))
            print (img2.shape)
            time2 = time.time()
            results = detector.detect_face(img2)
            print ('matching...')
            print ('results',results)
            time3 = time.time()
            
            if True:
                if results is not None:
                    total_boxes = results[0]
                    print('total boxes:',total_boxes)
                    print('total boxes type:',type(total_boxes[0][0]))
                    points = results[1]
                    time4 = time.time()
                    #'''
                    chips = detector.extract_image_chips(img2, points, 144, 0.37)
                    print('len chips:',len(chips))
                    time5 = time.time()
                    for i, chip in enumerate(chips):
                        #cv2.imshow('chip_'+str(test_index), chip)
                        #cv2.imwrite('chip_'+str(test_index)+'.jpg',chip)
                        #name = fm.query_name_by_img(chip)
                        time6 = time.time()
                        name = fm.query_nearest_by_img(chip)
                        time7 = time.time()
                        if name is None:
                            name = 'Not found'
                        else:
                            print('i chip:',total_boxes[i][0])
                            result_list.append([name,(total_boxes[i][:-1].astype('uint'))*scale,total_boxes[i][-1]])
                            # output_result.append([total_boxes[i][0])
                        #print('chip_'+str(test_index)+':'+name)
                        test_index+=1
                        #cv2.waitKey(0)
                time_end = time.time()
                print ('time_cost:',time_end-time1,'s per image')
                print ('img read and reshape cost:',time2-time1)
                print ('face detection time cost:',time3-time2)
                print ('extract crops cost:',time5-time4)
                print ('each face crop match cost',time7-time6)
                print('load detector:',time1-time10)
                print ('real time cost:',time_end-time10)

            return result_list
    except Exception as e:
        print(e)


