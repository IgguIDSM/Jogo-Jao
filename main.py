#Imports
from Utils.Utils import *;
from Inimigos import Inimigos;
from Utils.Math_Utils import Vector2, Projectile;
from Common.Dialogos import *;
from Common.Mapa import *;
import time;
import curses;
import keyboard;
#
mousePosition = Vector2(0,0);
#
pause = False;
debug = True;
fps = 120;
mobAttackDistance = 5;
playerMeleeDistance = 3;
Projectiles : list[Projectile] = [];
#
#Criamos o player, passamos nome, vida, stamina, posição inicial e o nome da sala inicial
player = Player("Cleitin","Nenhum","Nenhum",[],100,100,Vector2(3,6),"MAPA_TESTE");
player.SetClasse('Arqueiro');
# Missao : 'Matar Slime' = [progresso,objetivo,"estado"]
Missoes = {
    'Matar Slimes' : [0,3,'Incompleta'],
}
#
spawnedMobs: list[Inimigos.Mob] = [];
slime = Inimigos.Mob(Vector2(3,20),"Slime","*",100,"MAPA_TESTE",2,0.6,2);
slime.SetTarget(player);
spawnedMobs.append(slime);
#
#Funções De Acesso Direto
def GetFPS():
    return 1000 / fps;

#
def MissaoManager():
    if player.GetMissaoAtual() in Missoes.keys():
        missao = Missoes[player.GetMissaoAtual()];
        if missao[0] >= missao[1]:
            Missoes[player.GetMissaoAtual()][3] = "Completa";
#
def SistemaDeCombate(stdscr):
    if player.GetClasse() == "Cavaleiro":
        if keyboard.is_pressed(' '):
            winsound.Beep(500,5);
            for mob in spawnedMobs:
                if mob.DistanceToPlayer() < playerMeleeDistance:
                    mob.Damage(player.GetDamage());
                    if mob.GetVida() <= 0:
                        spawnedMobs.remove(mob);
                        del mob; #removemos a referência a este mob para wnão termos vazamento de memoria (ou memory leak).
    
    if player.GetClasse() == "Arqueiro":
        key = stdscr.getch();
        #Gerenciamos a posição do mouse por clique

        if key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse();
            global mousePosition;
            mousePosition = Vector2(x,y);
            if bstate == 0:
                winsound.Beep(500,5);
                Projectiles.append(Projectile(Vector2(player._position.x,player._position.y),1,Vector2(player.GetFacingDiretion().x,player.GetFacingDiretion().y)));



def ProjectileHandler():
    for projetil in Projectiles:
        projetil.Translate();
        if projetil.DistanceToPoint(player.GetPosition()) > 15 or DetectOtherCollision(projetil.GetPosition(),player.GetSala()):
            Projectiles.remove(projetil);
            del projetil;



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

##
def MenuDeClasse(stdscr):
    curses.curs_set(0);
    stdscr.nodelay(False);

    opcoes = ["Cavaleiro","Arqueiro"];
    selecionado = 0;
    while True:
        stdscr.clear();
        for i, opcao in enumerate(opcoes):
            if i == selecionado:
                stdscr.attron(curses.A_REVERSE);  # Destaque
                stdscr.addstr(i, 2 - 2, "➤ " + opcao);
                stdscr.attroff(curses.A_REVERSE);
            else:
                stdscr.addstr(i,2,""+opcao);
        stdscr.refresh();
        ##
        tecla = stdscr.getch();

        if tecla == ord('w'):
            selecionado = (selecionado - 1) % len(opcoes);
        elif tecla == ord("s"):
            selecionado = (selecionado + 1) % len(opcoes);
        elif tecla == ord(" ") or tecla in [10, 13]:
            if opcoes[selecionado] == "Cavaleiro":
                player.SetClasse("Cavaleiro");
                break
            elif opcoes[selecionado] == "Arqueiro":
                player.SetClasse("Arqueiro");
                break;




##
def Menu(stdscr,isGameRunning: bool = False):
    #TODO: colocar alteração de menu, para que caso o player tenha aberto o menu durante o jogo, apareça "Continuar" ao invés de "Iniciar".
    #TODO: caso o jogador tenha algum save, aparecerá uma opção de continuar o ultimo save.
    #
    curses.curs_set(0)  # Escondemos o Cursor
    stdscr.nodelay(False); # sempre aguardamos uma tecla pro próximo Update

    opcoes = ["Novo Jogo", "Carregar", "Salvar", "Opções", "Sair"] # OPÇÔESS!
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
            elif opcoes[selecionado] == "Novo Jogo":
                if debug == False:
                    EscreverDialogo(stdscr,player,"Narrador",PROLOGO["Narrador1"],Vector2(0,0),0.02,2,3,True);
                    EscreverDialogo(stdscr,player,"Narrador",PROLOGO["Narrador2"],Vector2(0,0),0.02,2,3,True);
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
#

# Renderiza a sala (Não consegui manter no Utils.py porque python é cheio de palhaçada)
def RenderRoom(stdscr,room : list, PlayerPosition : Vector2, PlayerModel : str):
    mapSize = GetRoomSize(room);
    pos = PlayerPosition;
    #Aqui geramos a posição dos Mobs
    #Renderizamos o mapa de maneira Horizontal
    for y in range(mapSize.y):
        #Primeiro iteramos sobre a linha -> Eixo Y
        for x in range(mapSize.x):
            #Depois sobre a coluna -> Eixo X
            #Tentamos renderizar os mobs
            for mob in spawnedMobs:
                p = mob.GetPosition();
                stdscr.addstr(round(p.y),round(p.x),f"{mob.GetModel()}");
                stdscr.addstr(round(p.y)+1,round(p.x)-2,f"{mob.GetBarraDeVida()}"); # renderizamos a barra de vida abaixo
            #
            for projetil in Projectiles:
                pP = projetil.GetPosition();
                stdscr.addstr(round(pP.y),round(pP.x),f"{projetil.GetModel()}"); # renderizamos o projetil para facilitar nossas lifes :D
            # Renderizamos por ultimo o player
            stdscr.addstr(pos.y,pos.x,PlayerModel);
            #
            #após renderizálos, renderizamos o resto do mapa
            stdscr.addstr(y,x,f"{room[y][x]}");
    stdscr.addstr("\n");


#-----------------------------------------------------------------------#



# Loop Principal do Game
def GameLoop(stdscr):
    #Se a tela estiver muito pequena pedimos para o jogador aumentar o tamanho do console (40x130);
    curses.curs_set(0);
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    frameTime = GetFPS();
    y,x = 0,0;
    while x <= 130 and y <= 40:
        y,x = stdscr.getmaxyx();
        stdscr.clear();
        stdscr.addstr(f"Por Favor Aumente o Tamanho do console para (40x130)\n Tamanho Atual :({y}x{x})");
        stdscr.refresh();
    # se a tela está de acordo comemos batata frita
    stdscr.clear();
    stdscr.addstr(f"O Tamanho da tela Está Adequado!\n");
    stdscr.addstr(f"Iniciando o Jogo...");
    stdscr.refresh();
    time.sleep(2);
    #

    # 60,10 -- posição do npc teste
    # Antes mesmo de começarmos, carregamos a intro e o menu principal
    if debug == False:
        EscreverDialogo(stdscr,player,'INTRO',DIALOGOS['INTRO'], Vector2(0,0));

    #Menu
    #rodamos o menu e a partir dele fazemos o resto
    Menu(stdscr);

    #Rodamos o GAMEE! (mas primeiro configuramos o curses pra não dar piri-paque)
    stdscr.clear();
    stdscr.refresh();
    stdscr.nodelay(True);
    while not pause:
    #Enquanto não está pausado
        stdscr.clear();
        #
        newPlayerPos = PlayerMovement(); # pegamos a nova posição desejada
        #
        #Colisões |  o jogador só se movimenta se não bater em nada
        player.Andar(newPlayerPos);
        #SISTEMA DE COMBATE

        SistemaDeCombate(stdscr=stdscr);
        ProjectileHandler();
        # Faz os mobs andarem em direcao ao player e atacarem
        for mob in spawnedMobs:
            mobWalkDirection = (player._position.__sub__(mob.GetPosition())).Normalize();
            if not DetectCollision(Vector2(round(mobWalkDirection.x),round(mobWalkDirection.y)),player) and mob.DistanceToPlayer() > mobAttackDistance:
                mob.Andar(Vector2(mobWalkDirection.x * mob.GetVelocity(),mobWalkDirection.y * mob.GetVelocity()));
        #Verifica se o player está em alguma porta, se estiver muda de cena

        porta =  IsPlayerOnDoor(newPlayerPos,player);

        if porta is not False:
            player.SetSala(PORTAS[player.GetSala()][porta]);
            posicao_porta =  AcharPorta(GetOpositeDoor(porta),MAPA[player.GetSala()]);
            if posicao_porta is not False:
                player.SetPosition(GetPlayerDoorPosition(porta,posicao_porta));
        
        #antes de renderizar qualquer coisa, damos prioridade as camadas de tela
        #diálogo
        npc_proximo = DetectNPC(newPlayerPos,player);
        # SE O NPC FOR O EZHARIEL
        if npc_proximo != False:
            if npc_proximo == "Ezhariel":
                for dialStruct in DIALOGOS['Ezhariel']:
                    if dialStruct[0] == "PLAYER":
                        EscreverDialogo(stdscr,player,player.nome,dialStruct[1],Vector2(0,0),0.05,3,3,False);
                    elif dialStruct[0] == "ESCOLHA":
                        #Aqui terá a escolha referente ao personagem específico!
                        MenuDeClasse(stdscr);
                        #Após escolher a classe, faz o resto do diálogo:

                        #Ao fim da escolha atribui a primeira missão
                        player.SetMissaoAtual("Matar Slimes");
                        pass;
                    else:
                        EscreverDialogo(stdscr,player,dialStruct[0],dialStruct[1],Vector2(0,0),0.05,3,3,False);
        #-----------------------------------------------------------------------------------------------------------------------#
            
            #Cuida dos Dialogos Durante o Jogo 
            else:
                if len(DIALOGOS[npc_proximo]) == 1:
                    EscreverDialogo(stdscr,npc_proximo,DIALOGOS[npc_proximo], Vector2(0,0));
                if len(DIALOGOS[npc_proximo]) > 1:
                    for falante,dialogo in DIALOGOS[npc_proximo].items():
                        if falante == "PLAYER":
                            EscreverDialogo(stdscr,player,player.nome,dialogo,Vector2(0,0),0.05,3,3,False);
                        else:
                            EscreverDialogo(stdscr,player,npc_proximo,dialogo,Vector2(0,0),0.05,3,3,False);

        
            
        #--------------------------------------------------------------------------------------------------------#
        #CUIDA DA MISSAO ATUAL

        MissaoManager();

        #Renderiza a Tela
        RenderRoom(stdscr,MAPA[player.GetSala()],player.GetPosition(),player.GetModel());
        #
        if player.GetMissaoAtual() != "Nenhum":
            stdscr.addstr(f"\nMissão Atual: {Missoes[player.GetMissaoAtual()]._nome} | {Missoes[player.GetMissaoAtual()]._progresso}/{Missoes[player.GetMissaoAtual()]._objetivo}\n");
        else:
            stdscr.addstr(f"\nMissão Atual: {player.GetMissaoAtual()}\n");
        #Renderiza o DEBUG se estiver habilitado
        if debug:
            stdscr.addstr(f"\nPlayerPos: {player.GetPosition().x},{player.GetPosition().y} | MousePos: x:{mousePosition.x} y: {mousePosition.y} | NewPlayerPos: {newPlayerPos.x + player.GetPosition().x},{newPlayerPos.y + player.GetPosition().y} | Colliding: { DetectCollision(newPlayerPos,player)})\n");
            pass;
        #
        #Renderiza a Hud
        Hud(stdscr);
        #
        stdscr.refresh(); # damos refresh
        #
        time.sleep(frameTime*0.01); # esperamos o próximo frame (como é em segundos, multiplicamos por 0.01) para ficar em milisegundos

###
#iniciamos o game mas garantimos que nada vai dar errado ;-;

if __name__ == '__main__':
    curses.wrapper(GameLoop);



# if __name__ == "__main__":
    # try:
        # curses.wrapper(GameLoop);
    # except Exception as e:
        # print("Ocorreu um erro:");
        # print(e);
        # input("Pressione Enter para sair...");
