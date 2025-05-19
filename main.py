#Imports
from curses import *;
from Dialogos import *;
import Player;
from utils import *;
from mapa import *;
import keyboard;
from time import *;
#
pause = False;
debug = True;
fps = 120;
#
#Criamos o player, passamos nome, vida, stamina, posição inicial e o nome da sala inicial
player = Player.Player("Cleitin",[],100,100,Vector2(20,10),"Dojo");

#Funções De Acesso Direto
def GetFPS():
    return 1000 / fps;

#Controla o Movimento do Player
def PlayerMovement():
    '''
    Movimentação do Jogador, famoso WASD.
    '''
    dir = Vector2(0,0);
    if keyboard.is_pressed('w') : 
        if not DetectCollision(Vector2(dir.x,dir.y -1),player): dir = Vector2(dir.x,dir.y -1);
    if keyboard.is_pressed('s') : 
        if not DetectCollision(Vector2(dir.x,dir.y +1),player): dir = Vector2(dir.x,dir.y +1);
    if keyboard.is_pressed('a') : 
        if not DetectCollision(Vector2(dir.x -1,dir.y),player): dir = Vector2(dir.x -1,dir.y);
    if keyboard.is_pressed('d') : 
        if not DetectCollision(Vector2(dir.x +1,dir.y),player): dir = Vector2(dir.x +1,dir.y);
    return dir;

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

#
def EscreverDialogo(stdscr, falante : str, dialogo : list = [], PosicaoNaTela : Vector2 = Vector2(0,0), tempoDeFala : float = 0.05, tempoEntreFalas : int = 3, tempoDeDica : int = 3):
    curses.curs_set(0);
    stdscr.nodelay(True);
    stdscr.clear();
    stdscr.addstr("Dica: Pressione [ESPACO] para pular as falas..");
    stdscr.refresh();
    sleep(tempoDeDica);
    #Limpamos para mostrar a fala
    stdscr.clear();
    #
    for i, texto in enumerate(dialogo):
        msg = "";
        for char in texto:
            msg += char;
            stdscr.addstr(PosicaoNaTela.y+i, PosicaoNaTela.x,f"{falante}: {msg}");
            stdscr.refresh();
            sleep(tempoDeFala);
            #Aqui deixamos o jogador apertar espaço para pular a fala
            if stdscr.getch() == ord(' '):
                msg = texto;
                stdscr.addstr(PosicaoNaTela.y+i, PosicaoNaTela.x,f"{falante}: {msg}");
                stdscr.refresh();
                break;
        #Mostramos a mensagem para o Jogador saber que pode pular o tempo de espera 
        stdscr.addstr(PosicaoNaTela.y+i, PosicaoNaTela.x,f"{falante}: {msg}");
        stdscr.refresh();
        #Esperamos o tempo normal, ou o jogador aperta o espaco para pular
        timer = time();
        while time() - timer < tempoEntreFalas:
            if stdscr.getch() == ord(' '):
                break;
            sleep(0.05);
        # Espera o Input do Jogador para a próxima fala

#
def TesteAnimacao(stdscr):
    curses.curs_set(0);
    stdscr.nodelay(True);

    spinner = ['-', '\\', '|', '/'];
    i = 0;
    EscreverDialogo(stdscr,"Modelo",DIALOGOS['Modelo'],Vector2(0,0),0.02,3);
    

    #Responsavel pela animação
    # while True:
        # stdscr.addstr(10, 10, spinner[i % len(spinner)]);
        # stdscr.refresh();
        # time.sleep(0.1);
        # stdscr.addstr(10, 10, ' ');  # apaga o anterior
        # i += 1;







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

        porta = IsPlayerOnDoor(newPlayerPos,player);

        if porta is not False:
            player.SetSala(PORTAS[player.GetSala()][porta]);
            posicao_porta = AcharPorta(GetOpositeDoor(porta),MAPA[player.GetSala()]);
            if posicao_porta is not False:
                player.SetPosition(GetPlayerDoorPosition(porta,posicao_porta));
        
        #Renderiza a Tela
        RenderRoom(stdscr,room=MAPA[player.GetSala()],PlayerPosition=player.GetPosition(),PlayerModel=player.GetModel());
        
        #Renderiza o DEBUG se estiver habilitado
        if debug:
            stdscr.addstr(f"\nPlayerPos: {player.GetPosition().x},{player.GetPosition().y} | NewPlayerPos: {newPlayerPos.x + player.GetPosition().x},{newPlayerPos.y + player.GetPosition().y} | Colliding: {DetectCollision(newPlayerPos,player)}\n");
        #
        
        #Renderiza a Hud
        Hud(stdscr);
        
        stdscr.refresh(); # damos refresh

        time.sleep(frameTime*0.01); # esperamos o próximo frame

###
if __name__ == "__main__":
    #curses.wrapper(GameLoop)
    curses.wrapper(TesteAnimacao)

