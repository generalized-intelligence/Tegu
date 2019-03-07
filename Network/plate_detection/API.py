#encoding=utf-8
import cv2
import os
from Util.mylogger import MyLogger
import time

def detection_plate(data_dir):
    '''
    Detect images in data dir.
    
    Args:
        img_array -- The numpy array of image to be predicted.
    '''
    try:
        from hyperlpr import HyperLPR_PlateRecogntion
        print(os.path.split(os.path.realpath(__file__))[0])
        print('Start')
        print('dir:',data_dir)
        result_list = []
        for img_name in os.listdir(data_dir):
            print('img name:',img_name)
            if (img_name.lower().find('.png')<0 and img_name.lower().find('.jpeg')<0 and img_name.lower().find('.jpg')<0 and img_name.lower().find('.bmp')<0):
                continue
            img_path = os.path.join(data_dir, img_name)
            print('Start read img')
            image = cv2.imread(img_path)
            print('Start lpr detection')
            result = HyperLPR_PlateRecogntion(image,path=os.path.join(os.path.split(os.path.realpath(__file__))[0],'hypercar'))
            result_list.append(result)
    except Exception as e:
        print(e)

        
def detection_plate_one_img(img_array):
    '''
    Detect one image.
    
    Args:
        img_array -- The numpy array of image to be predicted.
    '''
    try:
        from hyperlpr import HyperLPR_PlateRecogntion
        result_list = HyperLPR_PlateRecogntion(img_array,path=os.path.join(os.path.split(os.path.realpath(__file__))[0],'hypercar'))
        return result_list
    except Exception as e:
        print(e)

