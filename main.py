#Imports
from Utils.Utils import *;
from Inimigos import Inimigos;
from Utils.Math_Utils import Vector2, Projectile;
from Common.Dialogos import *;
from Common.Mapa import *;
from Common.Npc import *;
import time;
import curses;
import keyboard;
#
scr = None;
#
mousePosition = Vector2(0,0); # DESABILITADO POR BUG
#
pause = False; # define se o jogo está pausado |TODO|;

debug = True; # Define se o jogo apresentará DEBUG;

noDialog = True; # Define se jogo vai mostrar diálogos ou não, "UTILIZADO PARA DEBUG DE FUNCIONALIDADE"

fps = 120; # Define o FPS do jogo, o Pace ou Frames por Segundo.

estaNaRetaFinal = False;

mobAttackDistance = 3; # distancia de ataque dos mobs

playerMeleeDistance = 5; # distância de ataque do player;

npcTalkDistance = 3 # Distância de Interação com um NPC;

Projectiles : list[Projectile] = [];
#
#Criamos o player, passamos nome, vida, stamina, posição inicial e o nome da sala inicial
player = Player("Cleitin","Nenhum","Nenhum",[],100,100,Vector2(3,3),"Terceiro Andar");

#
player.SetClasse('Cavaleiro');



# Modelo de Missão : 'Nome' : [progresso, objetivo, 'estado'] Ex:
# Missao : 'Matar Slime' = [0,3,"Completa"] < o estado da missão será alterado automaticamente assim que o requisito do objetivo for completo
# Após o termino da missão o CallBack dessa Missão será executado! Elemento [3] => callback lambda
Missoes = {
    'Mate os Slimes' : [0,3,'Incompleta'],
    'Mate as Larvas' : [0,5,'Incompleta'],
    'Derrote Velkar' : [0,1,'Incompleta'],
}


#
spawnedMobs: list[Inimigos.Mob] = [];
#Spawnamos os mobs que não são de missão
#Zumbis
zombieSpawns = [Vector2(10,2),Vector2(10,7),Vector2(7,5)];
for i,zombieSpawn in enumerate(zombieSpawns):
    zombie = Inimigos.Mob(zombieSpawn,"Zumbi",'z',70,'Sala dos Zumbis',3,(i+1) * 0.3,1.5,None);
    zombie.SetTarget(player);
    spawnedMobs.append(zombie);
#

#
spawnedNPCS: list[Npc] = [];
spawnedNPCS.append(Npc('Ezhariel','e',[],100,100,Vector2(34,6),'Entrada')); # Ezhariel é o nosso npc da entrada (o último é o boss OOOOO)
spawnedNPCS.append(Npc('Sylveris','s',[],100,100,Vector2(22,7),'Segundo Andar'));
#
def RemoveNPC(nome):
    for npc in spawnedNPCS:
        if npc.nome == nome:
            spawnedNPCS.remove(npc);
            del npc;
            break;

#Retorna o FPS que o jogo deve rodar (frameTime)
def GetFPS():
    return (1000 / fps) * 0.01;
#

# Cuida do estado da missão
def MissaoManager():
    if player.GetMissaoAtual() in Missoes.keys():
        missao = Missoes[player.GetMissaoAtual()];
        if missao[0] >= missao[1]:
            Missoes[player.GetMissaoAtual()][2] = "Completa";
            player.SetMissaoAtual('Nenhum');
            if len(missao) > 3: # se tem mais de 3 então tem callback que no caso está no índice 3
                missao[4](missao[3]); # executamos o callback usando o index 3 como argumento (o 3 é o stdscr)

#
def SistemaDeCombate():
    if keyboard.is_pressed(' '):
        winsound.Beep(500,5);
        for mob in spawnedMobs:
            if mob.DistanceToPlayer() < playerMeleeDistance:
                mob.Damage(player.GetDamage());
                if mob.GetVida() <= 0:
                    mob.OnMobKilled();
                    spawnedMobs.remove(mob);
                    del mob; #removemos a referência a este mob para wnão termos vazamento de memoria (ou memory leak).

# Shoot a projectile
def ShootProjectile(startPosition: Vector2, direction : Vector2, velocity : int, maxDistance : int):
    winsound.Beep(500,5);
    Projectiles.append(Projectile(startPosition,velocity,direction,maxDistance));
#

# Handles all the projectiles on the scene
def ProjectileHandler():
    for projetil in Projectiles:
        projetil.Translate();
        # só removemos o projétil se ele atingiu alguma coisa ou chegou na sua distância máxima..
        if projetil.DistanceToPoint(player.GetPosition()) > projetil.GetMaxDistance() or DetectOtherCollision(projetil.GetPosition(),player.GetSala()):
            Projectiles.remove(projetil);
            del projetil;
#
def DetectNPC():
    for npc in spawnedNPCS:
        if npc.GetSala() == player.GetSala():
            if npc._position.Distance(player.GetPosition()) < npcTalkDistance:
                return npc;
    return None;
#
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
def MenuEscolha(stdscr, items : list):
    curses.curs_set(0);
    stdscr.nodelay(False);
    #retiramos o buffer de tecla
    opcoes = items;
    selecionado = 0;
    #
    while True:
        stdscr.clear();
        for i , opcao in enumerate(opcoes):
            if i == selecionado:
                stdscr.attron(curses.A_REVERSE);  # Destaque
                stdscr.addstr(i, 2 - 2, "➤ " + opcao);
                stdscr.attroff(curses.A_REVERSE);
            else:
                stdscr.addstr(i,2,'' + opcao);
        stdscr.refresh();
        
        tecla = stdscr.getch();
        
        if tecla == ord('w'):
            selecionado = (selecionado - 1) % len(opcoes);
        elif tecla == ord('s'):
            selecionado = (selecionado + 1) % len(opcoes);
        elif tecla == ord(' ') or tecla in [10,13]:
            stdscr.clear();
            stdscr.addstr(0, 0, f"Você escolheu: {opcoes[selecionado]} (pressione Qualquer tecla para continuar)");
            stdscr.refresh();
            stdscr.getch();
            return opcoes[selecionado];
##
def Menu(stdscr,isGameRunning: bool = False):
    #TODO: colocar alteração de menu, para que caso o player tenha aberto o menu durante o jogo, apareça "Continuar" ao invés de "Iniciar".
    #TODO: caso o jogador tenha algum save, aparecerá uma opção de continuar o ultimo save.
    #
    curses.curs_set(0)  # Escondemos o Cursor
    stdscr.nodelay(False); # sempre aguardamos uma tecla pro próximo Update
    #
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
                if noDialog == False:
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
NO_RENDER = ['0','1','2','3','9'];
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
                if mob.GetSala() == player.GetSala():
                    p = mob.GetPosition();
                    stdscr.addstr(round(p.y),round(p.x),f"{mob.GetModel()}");
                    stdscr.addstr(round(p.y)+1,round(p.x)-2,f"{mob.GetBarraDeVida()}"); # renderizamos a barra de vida abaixo
            #
            for projetil in Projectiles:
                pP = projetil.GetPosition();
                stdscr.addstr(round(pP.y),round(pP.x),f"{projetil.GetModel()}"); # renderizamos o projetil para facilitar nossas lifes :D
            #Renderizamos os NPC
            for npc in spawnedNPCS:
                if npc.GetSala() == player.GetSala():
                    np = npc.GetPosition();
                    stdscr.addstr(round(np.y),round(np.x),f"{npc.GetModel()}");
            # Renderizamos por ultimo o player
            stdscr.addstr(pos.y,pos.x,PlayerModel);
            #após renderizálos, renderizamos o resto do mapa
            if room[y][x] not in NO_RENDER: # se o que estamos renderizando não estiver na lista de Não renderizar, então mostramos
                stdscr.addstr(y,x,f"{room[y][x]}");
    stdscr.addstr("\n");

#---------------------------INIMIGOS DO FINAL DO JOGO----------------------------------#
def VelkarKilledCallback(stdscr):
    EscreverDialogo(stdscr,player,'Velkar',DIALOGOS['Velkar'][0][2],Vector2(0,0),0.05,2,3,True);
    EscreverDialogo(stdscr,player,'Narrador',DIALOGOS['Narrador_Terceiro_Andar'][0][2],Vector2(0,0),0.05,2,3,True);
    player.AddInventario('Voz Gelida(frag)');
#
def Velkar(stdscr):
    spawnPoint = AcharSpawn('9',MAPA['Velkar']);
    _velkar = Inimigos.Mob(spawnPoint,'Velkar','§',250,'Velkar',15,1.5,4,AdicionarProgresso);
    _velkar.SetTarget(player);
    #
    player.SetMissaoAtual("Derrote Velkar");
    #
    Missoes["Derrote Velkar"].append(stdscr);
    Missoes["Derrote Velkar"].append(VelkarKilledCallback);
    #
    spawnedMobs.append(_velkar);
    #attack Pattern













#--------------------------------------------------------------------------------------#


#
def WillCollideWithOtherMobs(checkMobPosition : Vector2, futureMobPosition : Vector2):
    for mob in spawnedMobs:
        if (mob.GetPosition() != checkMobPosition) and (mob.GetPosition().Distance(futureMobPosition) < 1):
            return True;
    return False;



#------------------------------------------------------------------------#


# Adiciona progresso a missão que o player está atribuido
def AdicionarProgresso():
    Missoes[player.GetMissaoAtual()][0] = Missoes[player.GetMissaoAtual()][0] + 1;



#CUIDA DOS CALLBACKS DE MISSÃO COMPLETA
def MatarSlimeCompleta(stdscr):
    EscreverDialogo(stdscr,player,'Ezhariel',DIALOGOS['Ezhariel1'][0][1],Vector2(0,0),0.05,3,3,False);
    #restauramos a vida do player, como recompensa
    player.SetVida(100);
    RemoveNPC("Ezhariel") # sumimos com ele
    EscreverDialogo(stdscr,player,'DICA',DICAS['DICA_PORTAS'],Vector2(0,0),0.02,3,3,True);

#
def MatarLarvasCompleta(stdscr):
    EscreverDialogo(stdscr,player,'Sylveris',DIALOGOS['Sylveris1'][0][1],Vector2(0,0),0.05,3,3,False);
    #damos a escolha do item e depois removemos ela
    escolha = MenuEscolha(stdscr,['Anel da Emersão','Colar do Vínculo Eterno']);
    if escolha == "Colar do Vínculo Eterno":
        EscreverDialogo(stdscr,player,'Sylveris',DIALOGOS['Sylveris2'][0][2]);
    player.AddInventario(escolha);
    #
    RemoveNPC("Sylveris") # sumimos com ela


#Precisamos de uma função só para o terceiro andar porque as coisas aqui são muito específicas
def TerceiroAndar(stdscr):
    if noDialog == False:
        EscreverDialogo(stdscr,player,'Narrador',DIALOGOS['Narrador_Terceiro_Andar'][0][1],Vector2(0,0),0.03,3,3,False);
        EscreverDialogo(stdscr,player,'Gorzhak',DIALOGOS['Gorzhak'][0][1],Vector2(0,0),0.03,3,3,False);
        EscreverDialogo(stdscr,player,'Gorzhak',DIALOGOS['Gorzhak'][0][2],Vector2(0,0),0.03,3,3,False);
        EscreverDialogo(stdscr,player,'Gorzhak',DIALOGOS['Gorzhak'][0][3],Vector2(0,0),0.03,3,3,False);
    Velkar(stdscr);
    pass;
#

def OnRoomChanged(sala : str):
    if sala == "Velkar":
        EscreverDialogo(scr,player,'Velkar',DIALOGOS['Velkar'][0][1],Vector2(0,0),0.05,3,3,True);        

#
def GameLoop(stdscr):
    #Se a tela estiver muito pequena pedimos para o jogador aumentar o tamanho do console (40x130);
    global scr;
    scr = stdscr;
    curses.curs_set(0);
    frameTime = GetFPS();
    y,x = 0,0;
    player._OnRoomChangedEvent.subscribe(OnRoomChanged);
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
    #
    # 60,10 -- posição do npc teste
    # Antes mesmo de começarmos, carregamos a intro e o menu principal
    if noDialog == False:
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

        SistemaDeCombate();
        ProjectileHandler();

        # Faz os mobs andarem em direcao ao player e atacarem
        for mob in spawnedMobs:
            if mob.GetSala() == player.GetSala():
                mob.MobTick(frameTime); # a cada update damos um MobTick usando o FrameTime
                mobWalkDirection = (player._position.__sub__(mob.GetPosition())).Normalize();

                if not DetectCollision(Vector2(round(mobWalkDirection.x),round(mobWalkDirection.y)),player) and mob.DistanceToPlayer() > 1:
                    if not WillCollideWithOtherMobs(mob.GetPosition(),mobWalkDirection):
                        mob.Andar(Vector2(mobWalkDirection.x * mob.GetVelocity(),mobWalkDirection.y * mob.GetVelocity()));

                if mob.DistanceToPlayer() < mobAttackDistance:
                    if mob._mobTick > mob._tempoDeAtaque:
                        mob.ResetMobTick();
                        winsound.Beep(5000,1);
                        player.Damage(mob.GetDamage());
        
        #Verifica se o player está em alguma porta, se estiver muda de cena
        porta = GetClosestDoor(player);
        #
        if porta != None:
            if keyboard.is_pressed('f'):
                player.SetSala(PORTAS[player.GetSala()][porta]);
                porta_spawn =  AcharSpawn(SPAWN_PORTAS[GetOpositeDoor(porta)],MAPA[player.GetSala()])
                if porta_spawn != False:
                    player.SetPosition(porta_spawn);
        
        #antes de renderizar qualquer coisa, damos prioridade as camadas de tela
        #diálogo
        npc_proximo = DetectNPC();
        if npc_proximo != None:
            if keyboard.is_pressed('f') and npc_proximo.canInteract():
                npc_proximo.SetInteracted();
                # SE O NPC FOR O EZHARIEL (CUIDAREMOS DAS MISSÕES AQ)
                if npc_proximo.nome == "Ezhariel":
                    for dialStruct in DIALOGOS['Ezhariel']:
                        if dialStruct[0] == "PLAYER":
                            if noDialog == False:
                                EscreverDialogo(stdscr,player,player.nome,dialStruct[1],Vector2(0,0),0.05,3,3,False);
                        elif dialStruct[0] == "MISSAO":
                            #Mostramos a dica de combate:
                            if noDialog == False:
                                EscreverDialogo(stdscr,player,"DICA",DICAS['DICA_COMBATE'],Vector2(0,0),0.02,3,3,True);

                            #Após isso dizemos qual é o callback da missão completa e adicionamos ao index 3 da missão
                            #para que nosso código saiba que no index 3 tem um callback
                            Missoes["Mate os Slimes"].append(stdscr);
                            Missoes["Mate os Slimes"].append(MatarSlimeCompleta);
                            #
                            spawns = [Vector2(10,2),Vector2(10,7),Vector2(7,5)];
                            for i,spawn in enumerate(spawns):
                                slime = Inimigos.Mob(spawn,"Slime","*",100,player.GetSala(),2,((i+1) * 0.15),2, AdicionarProgresso);
                                slime.SetTarget(player);
                                spawnedMobs.append(slime);
                            player.SetMissaoAtual("Mate os Slimes");
                        else:
                            if noDialog == False:
                                EscreverDialogo(stdscr,player,dialStruct[0],dialStruct[1],Vector2(0,0),0.05,3,3,False);
                # SE O NPC FOR O EZHARIEL (CUIDAREMOS DAS MISSÕES AQ)
                elif npc_proximo.nome == 'Sylveris':
                    for dialStruct in DIALOGOS['Sylveris']:
                        if dialStruct[0] == "PLAYER":
                            if noDialog == False:
                                EscreverDialogo(stdscr,player,player.nome,dialStruct[1],Vector2(0,0),0.05,3,3,False);
                        elif dialStruct[0] == "MISSAO":
                            #Mostramos a dica de combate:
                            if noDialog == True: # Trocar depois
                                EscreverDialogo(stdscr,player,"DICA",DICAS['DICA_COMBATE1'],Vector2(0,0),0.02,3,3,True);
                            #
                            Missoes["Mate as Larvas"].append(stdscr);
                            Missoes["Mate as Larvas"].append(MatarLarvasCompleta);
                            #
                            spawns = [Vector2(11,1),Vector2(14,6),Vector2(20,8),Vector2(21,10),Vector2(25,3)]
                            for i,spawn in enumerate(spawns):
                                larva = Inimigos.Mob(spawn,"Larva","-=-",150,player.GetSala(),6,(i+1) * 0.3,3.5, AdicionarProgresso);
                                larva.SetTarget(player);
                                spawnedMobs.append(larva);
                            player.SetMissaoAtual("Mate as Larvas");
                        else:
                            if noDialog == True:
                                EscreverDialogo(stdscr,player,"Sylveris",dialStruct[1],Vector2(0,0),0.02,3,3,True);
                elif npc_proximo.name == 'Gorzhak':

                    pass;
        #---------------------------------------------------------------------------------------------------------------------------#

                #Cuida dos Dialogos Durante o Jogo 
                else:
                    if len(DIALOGOS[npc_proximo.nome]) == 1:
                        if noDialog == False:
                            EscreverDialogo(stdscr,npc_proximo.nome,DIALOGOS[npc_proximo.nome], Vector2(0,0));
                    if len(DIALOGOS[npc_proximo.nome]) > 1:
                        for falante,dialogo in DIALOGOS[npc_proximo.nome].items():
                            if falante == "PLAYER":
                                if noDialog == False:
                                    EscreverDialogo(stdscr,player,player.nome,dialogo,Vector2(0,0),0.05,3,3,False);
                            else:
                                if noDialog == False:
                                    EscreverDialogo(stdscr,player,npc_proximo.nome,dialogo,Vector2(0,0),0.05,3,3,False);

        
            
        #--------------------------------------------------------------------------------------------------------#
        #Cuida do Final do Jogo
        if player.GetSala() == 'Terceiro Andar' and player._RetaFinal == False:
            player._RetaFinal = True;
            TerceiroAndar(stdscr);
        
        
        
        #CUIDA DA MISSAO ATUAL

        MissaoManager();

        #Renderiza a Tela
        RenderRoom(stdscr,MAPA[player.GetSala()],player.GetPosition(),player.GetModel());
        #Mostra o NPC Próximo
        if porta != None:
            if porta in PORTAS[player.GetSala()]:
                stdscr.addstr(f"\nPressione [F] para acessar a(o) {PORTAS[player.GetSala()][porta]}");
        if npc_proximo != None:
            stdscr.addstr(f"\nPressione [F] para interagir com {npc_proximo.nome}");
        #
        if player.GetMissaoAtual() != "Nenhum":
            stdscr.addstr(f"\nMissão Atual: {player.GetMissaoAtual()} | {Missoes[player.GetMissaoAtual()][0]}/{Missoes[player.GetMissaoAtual()][1]}\n");
        else:
            stdscr.addstr(f"\nMissão Atual: {player.GetMissaoAtual()}\n");
        #Renderiza o DEBUG se estiver habilitado
        if debug:
            stdscr.addstr(f"\nPlayerPos: {player.GetPosition().x},{player.GetPosition().y} | NewPlayerPos: {newPlayerPos.x + player.GetPosition().x},{newPlayerPos.y + player.GetPosition().y} | Colliding: { DetectCollision(newPlayerPos,player)})\n");
            pass;
        #
        #Renderiza a Hud
        Hud(stdscr);
        #
        stdscr.refresh(); # damos refresh
        #
        time.sleep(frameTime); # esperamos o próximo frame (como é em segundos, multiplicamos por 0.01) para ficar em milisegundos

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
