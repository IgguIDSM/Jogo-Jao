#Imports
from Utils import *;
from Math_Utils import Vector2;
import Dialogos;
import Mapa;
import time;
import curses;
import keyboard;
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
        if not  DetectCollision(Vector2(dir.x -1,dir.y),player): dir = Vector2(dir.x -1,dir.y);
    if keyboard.is_pressed('d') : 
        if not  DetectCollision(Vector2(dir.x +1,dir.y),player): dir = Vector2(dir.x +1,dir.y);
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
def Menu(stdscr,isGameRunning: bool = False):
    #TODO: colocar alteração de menu, para que caso o player tenha aberto o menu durante o jogo, apareça "Continuar" ao invés de "Iniciar".
    #TODO: caso o jogador tenha algum save, aparecerá uma opção de continuar o ultimo save.

    curses.curs_set(0)  # Escondemos o Cursor
    stdscr.nodelay(False); # sempre aguardamos uma tecla pro próximo Update

    opcoes = ["Iniciar", "Carregar", "Salvar", "Opções", "Sair"] # OPÇÔESS!
    if isGameRunning : opcoes[0] = "Continuar";
    selecionado = 0;

    while True:
        stdscr.clear();
        
        for i, opcao in enumerate(opcoes):
            if i == selecionado:
                stdscr.attron(curses.A_REVERSE);  # Destaque
                stdscr.addstr(i, 2 - 2, "➤ " + opcao);
                stdscr.attroff(curses.A_REVERSE);
            else:
                stdscr.addstr(i, 2, "" + opcao);

        stdscr.refresh();

        tecla = stdscr.getch();

        if tecla == ord('w'):
            selecionado = (selecionado - 1) % len(opcoes);
        elif tecla == ord("s"):
            selecionado = (selecionado + 1) % len(opcoes);
        elif tecla == ord(" ") or tecla in [10, 13]:
            if opcoes[selecionado] == "Sair":
                break
            elif opcoes[selecionado] == "Iniciar":
                break;
            elif opcoes[selecionado] == "Carregar":
                #mostra opções de saves...
                pass;
            elif opcoes[selecionado] == "Salvar":
                #mostra que o player salvou o jogo
                pass;
            else:
                stdscr.clear();
                stdscr.addstr(0, 0, f"Você selecionou: {opcoes[selecionado]}");
                stdscr.refresh();
                stdscr.getch();



























# Loop Principal do Game
def GameLoop(stdscr):

    frameTime = GetFPS();
    # 60,10 -- posição do npc teste
    # Antes mesmo de começarmos, carregamos a intro e o menu principal
    Dialogos.EscreverDialogo(stdscr,'INTRO',Dialogos.DIALOGOS['INTRO'], Vector2(0,0));
    #Menu
    #rodamos o menu e a partir dele fazemos o resto
    Menu(stdscr);
    #Rodamos o GAMEE! (mas primeiro configuramos o curses pra não dar piri-paque)
    curses.curs_set(0);
    stdscr.nodelay(True);
    stdscr.clear();
    stdscr.refresh();
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

        porta =  IsPlayerOnDoor(newPlayerPos,player);

        if porta is not False:
            player.SetSala(Mapa.PORTAS[player.GetSala()][porta]);
            posicao_porta =  AcharPorta( GetOpositeDoor(porta),Mapa.MAPA[player.GetSala()]);
            if posicao_porta is not False:
                player.SetPosition( GetPlayerDoorPosition(porta,posicao_porta));
        
        #antes de renderizar qualquer coisa, damos prioridade as camadas de tela
        #diálogo
        npc_proximo = DetectNPC(newPlayerPos,player);
        if npc_proximo != False:
            Dialogos.EscreverDialogo(stdscr,npc_proximo,Dialogos.DIALOGOS[npc_proximo], Vector2(0,0));
        







        #Renderiza a Tela
        RenderRoom(stdscr,room=Mapa.MAPA[player.GetSala()],PlayerPosition=player.GetPosition(),PlayerModel=player.GetModel());
        
        #Renderiza o DEBUG se estiver habilitado
        if debug:
            stdscr.addstr(f"\nPlayerPos: {player.GetPosition().x},{player.GetPosition().y} | NewPlayerPos: {newPlayerPos.x + player.GetPosition().x},{newPlayerPos.y + player.GetPosition().y} | Colliding: { DetectCollision(newPlayerPos,player)}\n");
        #
        
        #Renderiza a Hud
        Hud(stdscr);
        
        stdscr.refresh(); # damos refresh

        time.sleep(frameTime*0.01); # esperamos o próximo frame (como é em segundos, multiplicamos por 0.01) para ficar em milisegundos

###
#iniciamos o game mas garantimos que nada vai dar errado ;-;
if __name__ == "__main__":
    try:
        curses.wrapper(GameLoop);
    except Exception as e:
        print("Ocorreu um erro:");
        print(e);
        input("Pressione Enter para sair...");
