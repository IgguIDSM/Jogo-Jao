import os;
#Limpa a tela
def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear');

#
def RenderRoom(room):
    for line in room:
        print(f"{line}\n");

#
def GetRoomSize(room):
    nCol = len(room);
    return (len(room[0]),len(room));
        