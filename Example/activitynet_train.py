from Network.activity_net.video_hdf5_generator import process_video_dir
from Network.activity_net.API import ActivityNet_Dataloader, ActivityNet_Model

'''
You have to pre process videos before you training.
It will cost huge disk space and huge memmory space.
'''
process_video_dir(r"videos/folder/path", r"pre-process/output/path")    
m = ActivityNet_Model()
d = ActivityNet_Dataloader(r"videos/folder/path",
        r"training/annotation/path", r"testing/annotation/path",   
        r"pre-process/output/path") #If you dont have a test annotation file, just set the same as the training annotation file
m.set_dataset(d)
for i in range(200):
    train_info = m.trian()
    print(train_info)
    if i % 20==0:
        save_path = "model{}.h5".format(str(i).zfill(3))
        m.model.save(path)