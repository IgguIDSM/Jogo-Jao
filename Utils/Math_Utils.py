import math;
#Objetos
class Vector2:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
    #
    def Distance(self,toVector):
        return (math.sqrt((toVector.y - self.y)**2 + ( toVector.x - self.x)**2));
    #
    def Magnitude(self):
        return (math.sqrt(self.x**2 + self.y**2));
    #
    def Normalize(self):
        mag = self.Magnitude();
        #
        if mag == 0:
            return Vector2(0,0);
        #
        return Vector2(self.x / mag,self.y / mag);
    #
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)


#
