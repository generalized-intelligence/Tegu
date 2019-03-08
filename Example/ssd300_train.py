import sys
sys.path.append('..')
from keras import backend
backend.set_image_dim_ordering('tf')
from Network.SSD300.API import SSD_Model, SSD_DataLoaders

def ssd_train():
    epoch = 200    
    m = SSD_Model(class_count=2, base_lr=0.0004)
    d = SSD_DataLoader(anno_path=r"annotation/path", data_path=r"dataset/path",batch_size=32)
    m.set_dataset(d)
    for i in range(epoch):
        train_info = m.train()
        print('Epoch:{}, history:{}'.format(i,train_info.history))

        if i%20==0: 
            save_path = "ssd_model{}.h5".format(str(i).zfill(3))
            m.model.save(save_path)
            print('Saved')

            print('Start metrics.')
            metrics_info = m.metrics(path)
            print(metrics_info)

if __name__=='__main__':
    ssd_train()
   