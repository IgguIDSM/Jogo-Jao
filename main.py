#Imports
from curses import *;
from Player import Player;
from utils import *;
from mapa import *;
import keyboard;
import time;
#
pause = False;
debug = True;
fps = 120;
#
#Criamos o player, passamos nome, vida, stamina, posição inicial e o nome da sala inicial
player = Player("Cleitin",[],100,100,Vector2(20,10),"Dojo");

#Funções De Acesso Direto
def GetFPS():
    return 1000 / fps;

#Detecta Colisões
def DetectCollision(pPos : Vector2):
    '''
    Detector de Colisões do Jogador baseado na posição futura dele.

    Args:
        pPos (Vector2) : posição futura do jogador para verificar colisão, caso esteja colidindo retorna True, se não, Falso.
    '''
    sala = MAPA[player.GetSala()];
    oldPos = player.GetPosition();
    if sala[pPos.y + oldPos.y][pPos.x + oldPos.x] in OBJETOS_DE_COLISAO: return True;
    return False;

#Controla o Movimento do Player
def PlayerMovement():
    '''
    Movimentação do Jogador, famoso WASD.
    '''
    dir = Vector2(0,0);
    if keyboard.is_pressed('w') : 
        if not DetectCollision(Vector2(dir.x,dir.y -1)): dir = Vector2(dir.x,dir.y -1);
    if keyboard.is_pressed('s') : 
        if not DetectCollision(Vector2(dir.x,dir.y +1)): dir = Vector2(dir.x,dir.y +1);
    if keyboard.is_pressed('a') : 
        if not DetectCollision(Vector2(dir.x -1,dir.y)): dir = Vector2(dir.x -1,dir.y);
    if keyboard.is_pressed('d') : 
        if not DetectCollision(Vector2(dir.x +1,dir.y)): dir = Vector2(dir.x +1,dir.y);
    return dir;

#
def IsPlayerOnDoor(pPos: Vector2,sala):
    '''
    Retorna se o jogador está colidindo com uma porta baseado na nova posição desejada

    Args:
        pPos(Vector2): Posição futura do jogador.
        sala(str): Nome da sala atual do jogador (pode ser adquirido usando player.GetSala())

    Returns: retorna a porta da sala que o jogador se encontra, podendo ser (N,S,L,O), se não estiver em uma porta, retorna falso.
    '''
    sala_atual = MAPA[sala];
    oldPos = player.GetPosition();
    if sala_atual[pPos.y + oldPos.y][pPos.x + oldPos.x] in PORTAS[sala]: return sala_atual[pPos.y + oldPos.y][pPos.x + oldPos.x];
    return False;


#Mostra as Infos do Player
def Hud(stdscr):
    '''
    Exibe as Informações do Jogador, como Nome da Sala, Nome do Jogador, Vida, Stamina e Inventário.
    '''
    stdscr.addstr(f"\n");
    stdscr.addstr(f"Nome: {player.nome}\n");
    stdscr.addstr(f"Vida: {player.GetVida()}\n");
    stdscr.addstr(f"Stamina: {player.GetStamina()}\n");
    stdscr.addstr(f"Inventario: {player.GetInventario()}\n");
    stdscr.addstr(f"Sala Atual: {player.GetSala()}\n");








# Loop Principal do Game
def GameLoop(stdscr):
    curses.curs_set(0);
    stdscr.nodelay(True);
    stdscr.clear();
    frameTime = GetFPS();
    while not pause:
    #Enquanto não está pausado
        stdscr.clear();
        #
        newPlayerPos = PlayerMovement(); # pegamos a nova posição desejada
        #
        #Colisões |  o jogador só se movimenta se não bater em nada
        player.Andar(newPlayerPos);
        #
        #Verifica se o player está em alguma porta, se estiver muda de cena

        door = IsPlayerOnDoor(newPlayerPos,player.GetSala());

        if door is not False:
            player.SetSala(PORTAS[player.GetSala()][door]);
            doorPos = FindDoor(GetOpositeDoor(door),MAPA[player.GetSala()]);
            if doorPos is not False:
                player.SetPosition(GetPlayerDoorPosition(door,doorPos));
        
        #Renderiza a Tela
        RenderRoom(stdscr,room=MAPA[player.GetSala()],PlayerPosition=player.GetPosition(),PlayerModel=player.GetModel());
        
        #Renderiza o DEBUG se estiver habilitado
        if debug:
            stdscr.addstr(f"\nPlayerPos: {player.GetPosition().x},{player.GetPosition().y} | NewPlayerPos: {newPlayerPos.x + player.GetPosition().x},{newPlayerPos.y + player.GetPosition().y} | Colliding: {DetectCollision(newPlayerPos)}\n");
        #
        
        #Renderiza a Hud
        Hud(stdscr);
        
        stdscr.refresh(); # damos refresh

        time.sleep(frameTime*0.01); # esperamos o próximo frame

###
if __name__ == "__main__":
    curses.wrapper(GameLoop)

