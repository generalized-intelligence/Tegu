from keras import backend
backend.set_image_dim_ordering('tf')
from Network.SSD300.API import SSD_Model, SSD_DataLoader

def ssd_train():
    epoch = 200    
    m = SSD_Model(class_count=2, lr=0.0004)
    d = SSD_DataLoader(anno_path=r"annotation/file/path", data_path=r"dataset/path",batch_size=4)
    m.set_dataset(d)
    for i in range(epoch):
        train_info = m.train()
        print('Epoch:{}, history:{}'.format(i,train_info.history))

        if (i)%20==0 or i+1==epoch:
            save_path = "ssd_model{}.h5".format(str(i).zfill(3))
            m.model.save(save_path)
            print('Saved')

            print('Start metrics.')
            metrics_info = m.metrics(save_path)
            print(metrics_info)

def ssd_predict():
    m = SSD_Model(class_count=2)
    print(m.predict(img_path=r"image/you/want/to/predict", model_path=r"model/path", anno_path=r"annotation/path"))
    #[[label:int, class_name:str, score:double, (xmin, ymin), (xmax, ymax)]]
    
if __name__=='__main__':
    ssd_train()
    ssd_predict()
   