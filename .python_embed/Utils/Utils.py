from Utils.Math_Utils import *;
from Common.Player import Player;
from Common.Mapa import *;
#Detecta Colisões
def DetectCollision(pPos : Vector2, player : Player):
    '''
    Detector de Colisões do Jogador baseado na posição futura dele.

    Args:
        pPos (Vector2) : posição futura do jogador para verificar colisão, caso esteja colidindo retorna True, se não, Falso.
    '''
    sala = MAPA[player.GetSala()];
    oldPos = player.GetPosition();
    if sala[pPos.y + oldPos.y][pPos.x + oldPos.x] in OBJETOS_DE_COLISAO: return True;
    return False;
#
def DetectOtherCollision(pPos : Vector2, roomName : str):
    '''
    Detector de Colisões do Jogador baseado na posição futura dele.

    Args:
        pPos (Vector2) : posição futura do jogador para verificar colisão, caso esteja colidindo retorna True, se não, Falso.
    '''
    sala = MAPA[roomName];
    if sala[round(pPos.y)][round(pPos.x)] in OBJETOS_DE_COLISAO: return True;
    return False;
#
def GetClosestDoor(player : Player):
    doors = ['N','S','L','O'];
    for porta in doors:
        porta_pos = AcharPorta(porta,MAPA[player.GetSala()]);
        if porta_pos.x != -1 and porta_pos.y != -1:
            if porta_pos.Distance(player.GetPosition()) < 3:
                return porta;
    return None;
#
def IsPlayerOnDoor(pPos: Vector2,player : Player):
    '''
    Retorna se o jogador está colidindo com uma porta baseado na nova posição desejada

    Args:
        pPos(Vector2): Posição futura do jogador.
        sala(str): Nome da sala atual do jogador (pode ser adquirido usando player.GetSala())

    Returns: retorna a porta da sala que o jogador se encontra, podendo ser (N,S,L,O), se não estiver em uma porta, retorna falso.
    '''
    sala = player.GetSala();
    sala_atual = MAPA[sala];
    oldPos = player.GetPosition();
    if PORTAS.__contains__(sala):
        if sala_atual[pPos.y + oldPos.y][pPos.x + oldPos.x] in PORTAS[sala]: return sala_atual[pPos.y + oldPos.y][pPos.x + oldPos.x];
    return False;
#
SPAWN_PORTAS = {'N': '0','S': '1','L': '2','O': '3'};
#
def AcharSpawn(spawnPoint : str, sala : dict):
    # N - 0, S - 1, L - 2, O - 3, s - Spawn de cena
    #Tentamos achar o spawn no mapa
    mapSize = GetRoomSize(sala);
    for y in range(mapSize.y):
        for x in range(mapSize.x):
            if sala[y][x] == spawnPoint:
                return Vector2(x,y);
    return False;
#
def IsSalaTrancada(nomeDaSala):
    if nomeDaSala in PORTAS_TRANCADAS.keys():
        return True;
    return False;
#
def AcharPorta(porta : str, sala : dict):
    #Tentamos encontrar a porta no mapa
    mapSize = GetRoomSize(sala);
    for y in range(mapSize.y):
        for x in range(mapSize.x):
            if sala[y][x] == porta:
                return Vector2(x,y);
    return Vector2(-1,-1);

#
def GetPlayerDoorPosition(porta,doorPosition):
    dp = doorPosition;
    if porta == "L": return Vector2(dp.x + 3,dp.y);
    if porta == "O": return Vector2(dp.x - 3,dp.y);
    if porta == "N": return Vector2(dp.x,dp.y - 3);
    if porta == "S": return Vector2(dp.x,dp.y + 3);

#
def GetOpositeDoor(porta):
    if porta == "L": return "O";
    if porta == "O" : return "L";
    if porta == "N" : return "S";
    if porta == "S" : return "N";
#


#
def GetRoomSize(room):
    return Vector2(len(room[0]),len(room));
        