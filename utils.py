from Math_Utils import *;
from Player import Player;
from Mapa import *;
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
#Detecta NPCS
def DetectNPC(pPos : Vector2, player : Player):
    '''
    Detector de Colisões do Jogador baseado na posição futura dele.

    Args:
        pPos (Vector2) : posição futura do jogador para verificar colisão, caso esteja colidindo retorna True, se não, Falso.
    Returns:
        retorna o nome do npc ou falso, caso não encontre nenhum npc
    '''
    sala = MAPA[player.GetSala()];
    oldPos = player.GetPosition();
    if sala[pPos.y + oldPos.y][pPos.x + oldPos.x] in NPCS.keys(): return NPCS[sala[pPos.y + oldPos.y][pPos.x + oldPos.x]];
    return False;

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
    if sala_atual[pPos.y + oldPos.y][pPos.x + oldPos.x] in PORTAS[sala]: return sala_atual[pPos.y + oldPos.y][pPos.x + oldPos.x];
    return False;

#
def AcharPorta(porta : str, sala : dict):
    #Tentamos encontrar a porta no mapa
    mapSize = GetRoomSize(sala);
    for y in range(mapSize.y):
        for x in range(mapSize.x):
            if sala[y][x] == porta:
                return Vector2(x,y);
    return False;

#
def GetPlayerDoorPosition(porta,doorPosition):
    dp = doorPosition;
    if porta == "L": return Vector2(dp.x + 3,dp.y);
    if porta == "O": return Vector2(dp.x - 3,dp.y);
    if porta == "N": return Vector2(dp.x,dp.y + 3);
    if porta == "S": return Vector2(dp.x,dp.y - 3);

#
def GetOpositeDoor(porta):
    if porta == "L": return "O"
    if porta == "O" : return "L"
    if porta == "N" : return "S"
    if porta == "S" : return "N";
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
        