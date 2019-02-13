from model.ImageAnnotation import Annotation
a=Annotation(1, 1, 1, 99, 99)
b=Annotation(1, 1, 2, 29, 49)
c=Annotation(2, 2, 2, 33, 29)
d=Annotation(2, 2, 2, 49, 89)

assert a<b
assert b>a
assert b<c
assert c!=d

ls_anno=[]
ls_anno.append(a)
ls_anno.append(b)
ls_anno.append(c)
ls_anno.append(d)

ls_anno.sort()
assert ls_anno[0].x1==1
assert ls_anno[0].y1==1
assert ls_anno[0].x2==99
assert ls_anno[0].y2==99