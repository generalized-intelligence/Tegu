from model.AnnotateImageModel import *
if __name__=="__main__":
    aim=AnnotatedImageModel()
    aim.initWithSerializeString("0:__background__,1:Label-1,2:标签-2\na.png:1,2,3,99,99,2,100,100,120,120\n")
    #print(aim.userDefinedLabelCount())
    assert aim.userDefinedLabelCount()==2,"count error"
    aim.initWithSerializeString("0:__background__,1:,2:标签-2,3:Hahaha\na.png:1,2,3,99,99,2,100,100,120,120\n")
    assert aim.userDefinedLabelCount() == 3, "count error"
    aim.initWithSerializeString(
        "0:__background__,1:Label-one,2:标签-2,4:Four,3:Sanity\na.png:1,2,3,99,99,2,100,100,120,120\n")
    assert aim.userDefinedLabelCount() == 4, "count error"
    aim.initWithSerializeString("0:__background__,1:Label-one,2:标签-2,4:Four,3:Sanity\n"
        "a.png:1,2,3,99,99,2,100,100,120,120\n"
        "b.png:1,2,3,99,99,2,100,100,120,120\n"
        "b.png:2,2,3,99,99,3,100,100,120,120\n"
        "c.png:1,2,3,99,99,2,100,100,120,120\n"
        "c.png:2,2,3,99,99,3,100,100,120,120\n"
        "c.png:1,20,30,40,50,2,120,130,140,150,3,2,3,99,99,4,100,100,120,120\n")
    assert aim.userDefinedLabelCount() == 4, "count error"
    assert aim.getAnnotatedImageCount() == 3,"count error"
    imgNameA='c.png'
    assert aim.getAnnotationCountForImage(imgNameA)==8,"count error"
    aim.initWithSerializeString(
        "0:__background__,1:Label-one,2:标签-2,4:Four,3:Sanity\n"
        "a.png:1,2,3,99,99,2,100,100,120,120\n"
        "b.png:2,2,3,99,99,3,100,100,120,120\n"
        "c.png:1,20,30,40,50,2,120,130,140,150,3,2,3,99,99,4,100,100,120,120\n")
    assert aim.getAnnotatedImageCount()==3,"count error"
    assert aim.getAnnotationCountForImage(imgNameA)==4,"count error"
    imgNameB='b.png'
    aim.removeAnnotation(imgNameB,Annotation(1,2,3,99,99))
    aim.removeAnnotation(imgNameB, Annotation(2, 2, 3, 99, 99))
    aim.appendNewLabel()
    print(aim.toSerializeString())
    aim.appendNewLabel()
    print(aim.toSerializeString())