import math;
#Objetos
class Vector2:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
    #
    def Distance(self,ToPoint):
        return (math.sqrt((ToPoint.y - self.y)**2 + ( ToPoint.x - self.x)**2));
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
class Projectile:
    _model = ['^','v','<','>'];
    _direction = Vector2(0,0);
    _spawnPosition = Vector2(0,0);
    _position = Vector2(0,0);
    _velocity = 0;
    _maxDistance = 0;
    
    def __init__(self,spawnPosition : Vector2,velocity : int, direction : Vector2, maxDistance : int = 15):
        self._position = spawnPosition;
        self._spawnPosition = spawnPosition;
        self._velocity = velocity;
        self._direction = direction;
        self._maxDistance = maxDistance;
    #
    def GetSpawnPosition(self):
        return self._spawnPosition;
    #
    def GetMaxDistance(self):
        return self._maxDistance;
    #
    def GetPosition(self):
        return self._position;
    #
    def DistanceToPoint(self,point : Vector2):
        return self._position.Distance(point);
    #
    def Translate(self):
        self._position.x += self._direction.x * self._velocity;
        self._position.y += self._direction.y * self._velocity;
    #
    def GetModel(self):
        if self._direction.x > 0:
            return self._model[3];
        elif self._direction.x < 0:
            return self._model[2];
        elif self._direction.y > 0:
            return self._model[0];
        elif self._direction.y < 0:
            return self._model[1];
