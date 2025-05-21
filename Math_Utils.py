import math;
#Objetos
class Vector2:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
    #
    def Distance(self,toVector):
        return (math.sqrt((self.x - toVector.x)**2 + (self.y - toVector.y)**2));
#
