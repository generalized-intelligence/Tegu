class Annotation:
    def __init__(self, labelId, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.labelId = labelId
    def identStr(self):
        return "{0}-{1}-{2}-{3}-{4}".format(str(self.labelId),str(self.x1),str(self.y1),
                                            str(self.x2),str(self.y2))
    def width(self):
        return abs(self.x2-self.x1)
    def height(self):
        return abs(self.y2-self.y1)
    def __lt__(self, other):
        if isinstance(other,Annotation):
            if self.x1 != other.x1:
                return self.x1 < other.x1
            elif self.y1 < other.y1:
                return True
            else:
                return False
        else:
            raise Exception("other must be Annotation")
    def __gt__(self, other):
        if isinstance(other,Annotation):
            if self.x1 != other.x1:
                return self.x1 > other.x1
            elif self.y1 > other.y1:
                return True
            else:
                return False
        else:
            raise Exception("other must be Annotation")
    def __eq__(self, other):
        if isinstance(other,Annotation):
            return self.labelId == other.labelId and self.x1 == other.x1 and self.x2 == other.x2 and self.y1 == other.y1 and self.y2 == other.y2
        else:
            raise Exception("other must be Annotation")
