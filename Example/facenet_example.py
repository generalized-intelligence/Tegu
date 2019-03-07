import sys
sys.path.append('..')
from Network.facenet.API import  build_face_manager, detetion_and_recongnize

'''
You have to build face manager before you start detection and recongnize.
'''

face_manager = build_face_manager(r"face/dataset/path")
result = detetion_and_recongnize(face_manager, r"images/path/you/want/to/detect")
print(result)
