from math  import sqrt

class coor_2D:
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y
		
    def __sub__(self, other):
        return coor_2D(self.x - other.x, self.y - other.y)
        
    def norm(self):
        return sqrt(self.x ** 2 + self.y ** 2)
        
    def cos_2D(self, other):#cos
        if self.norm()*other.norm() != 0:
            return (self.x * other.x + self.y * other.y) / (self.norm()*other.norm())
        else:
            return 0