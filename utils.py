import os;
import math;
import mapa;

#Objetos
class Vector2:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
    #
    def Distance(self,toVector):
        return (math.sqrt((self.x - toVector.x)**2 + (self.y - toVector.y)**2));


#Funcões utilitárias
#Limpa a tela
def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear');

#
def RenderRoom(room):
    mapSize = GetRoomSize(room=room);
    pos = Vector2(20,60);
    #Renderizamos o mapa de maneira Horizontal
    for y in range(mapSize[0]):
        #Primeiro iteramos sobre a linha -> Eixo Y
        for x in range(mapSize[1]):
            #Depois sobre a coluna -> Eixo X
            #Aqui verificamos se a posição do player é a que está sendo iterada. se for, renderizamos ele, se não, renderiza objeto do mapa
            #if pos == Vector2(20,60):
            #    print("i",end="");
            #else:
            print(f"{room[x][y]}",end="");
        print("")
#
def GetRoomSize(room):
    return (len(room[0]),len(room));
        