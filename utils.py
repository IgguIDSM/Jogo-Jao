import os;
import curses;
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

#
def GetOpositeDoor(porta):
    if porta == "L": return "O"
    if porta == "O" : return "L"
    if porta == "N" : return "S"
    if porta == "S" : return "N";
#

#Funcões utilitárias
#Limpa a tela
def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear');

#
def RenderRoom(stdscr,room : list, PlayerPosition : Vector2,PlayerModel : str):
    mapSize = GetRoomSize(room=room);
    pos = PlayerPosition;
    #Renderizamos o mapa de maneira Horizontal
    for y in range(mapSize.y):
        #Primeiro iteramos sobre a linha -> Eixo Y
        for x in range(mapSize.x):
            #Depois sobre a coluna -> Eixo X
            #Aqui verificamos se a posição do player é a que está sendo iterada. se for, renderizamos ele, se não, renderiza objeto do mapa
            if pos.x == x and pos.y == y:
                stdscr.addstr(y,x,PlayerModel);
            else:
                stdscr.addstr(y,x,f"{room[y][x]}");
    stdscr.addstr("\n");

#
def GetRoomSize(room):
    return Vector2(len(room[0]),len(room));
        