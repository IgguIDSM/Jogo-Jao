import curses;
import keyboard;
import time;
import winsound;
from Common.Player import Player;
from Utils.Math_Utils import Vector2;

PROLOGO = {
    'Narrador1' : [
        "{playerName}, morador do reino de Valdaryen era um jovem que seguiu os passos de sua familia",
        "e se tornou um mercador, após ganhar sua própria carruagem dada de presente por seu pai,",
        "ele foi em busca de conseguir seu próprio dinheiro.",
        "Chegando na vila de mercadores ele foi a procura de sua primeira missão, e observou que no mural",
        "havia um pedido de carregamento de suprimentos para o reino de Lunareth, que era um forte aliado do seu reino",
        "e que estava passando por dificuldades já que estava em meio a uma guerra contra os goblins que estavam se espalhando pelo mundo",
        "sendo assim ele decidiu aceitar a missão para ajudar um forte aliado de seu reino."
    ],
    'Narrador2' : [
        "Então {playerName} teve um dia para se preparar para a missão e partir logo de manhã",
        "no outro dia, por recomendação da vila, ele teria quatro aventureiros fazendo sua escolta para manter sua segurança",
        "pois o caminho era repleto de bandidos e monstros mágicos perigosos",
        "Chegando o próximo dia, eles partiram em direção ao Reino de Lunareth.",
        "após algumas horas os aventureiros perceberam que a viagem estava tranquila demais...",
        "de repente escutam um barulho na mata, e quanto pensam em entrar em formação de batalha",
        "já era tarde demais...",
        "O monstro que saiu da mata lançou uma bola de fogo contra {playerName}, atingindo sua carruagem e o nocauteando",
        "caído no chao {playerName} assim que recuperou a consciência viu uma pedra brilhante que jamais havia visto",
        "sem pensar muito {playerName} pegou a pedra para jogar em direção ao monstro",
        "mas um brilho muito forte começou a emanar da pedra, e quando os aventureiros tentaram ajudar",
        "{playerName} já não estava mais lá...."
    ]
}

DICAS = {
    'DICA_COMBATE':
    [
        "Pressione [ESPACO] para atacar os inimigos",
        "A Sua distância de ataque é de 5 metros",
        "Os Mobs conseguem te atacar se chegarem muito perto!",
    ] 
}


#

DIALOGOS = {
    'INTRO':
        [
            "Bem Vindo ao Dungeons Conquest!",
            "Fique a vontade para mudar as configurações no menu principal!",
            "O Jogo Possui Dois possíveis finais, aceita o desafio?",
            "Bom, Boa Jogatina!",
        ],
    'Ezhariel':
        [
            [
                'Ezhariel',
                [
                    "Olá jovem aventureiro, seja bem vindo a Dungeon da Luminária Perdida, eu me chamo Ezhariel, o Portador da Luz Esquecida.",
                    "Eu serei seu guia, mas vejo que você veio sem qualquer preparo prévio..."
                ]
            ],
            [
                'PLAYER',
                [
                    "Sim, sou apenas um mercador que estava em uma missão de entrega de suprimentos..."
                ]
            ],
            [
                'Ezhariel',
                [
                    "Bom, Sendo assim, eu lhe tornarei um bravo guerreiro",
                    "Para poder se defender dos perigos que encontrará pelo caminho...",
                    "Mas antes de prosseguir...",
                    "Terá que passar por esse simples desafio:",
                    "Você terá que eliminar os três Slimes que invocarei nesta sala",
                    "Se você derrotá-los, será honrado como Cavaleiro da luz!",
                    "Está pronto?, então vamos começar...",
                ]
            ],
            [
                'MISSAO', # esse parametro é para informar ao script que aqui acontece alguma interpretação no código (Missao,Item,etc...)... (NÃO É INTERPRETADO COMO FALA!!!!)
            ],
        ],
    'Ezhariel1':
        [
            [
                'Ezhariel',
                [
                    "Parabéns!, vejo que você leva jeito para ser um grande aventureiro...",
                    "Percebi que sofreu alguns danos, mas não se preocupe, irei recuperar sua vida!",
                    "Pronto, Novo em folha!",
                    "Bom... irei explicar como funcionam as coisas por aqui",
                    "esta dungeon é bem mais antiga que todas as que estão estão espalhadas por ai...",
                    "aqui possuímos quatro andares, contendo cada um seu próprio desafio...",
                    "sendo o último andar, dominado pelo Homem Sombra...",
                    "de onde nenhum guerreiro saiu vivo....",
                ],
            ],
            
        ],
    'Sylveris':
        [
            [
                'Sylveris',
                [
                    "",
                ]
            ]
        ]
}

#



#Cada Diálogo é uma estrutura contendo o nome do personagem e os diálogos, sendo essa estrutura um dicionário podendo conter o personagem e as falas (se for fala unica).
#Se for diálogo de missão, terá respostas e conversas paralelas.

def EscreverDialogo(stdscr, player : Player, falante : str, dialogo : list = [], PosicaoNaTela : Vector2 = Vector2(0,0), tempoDeFala : float = 0.05, tempoEntreFalas : int = 3, tempoDeDica : int = 3, textoPermanente = False):
    curses.curs_set(0);
    stdscr.nodelay(True);
    stdscr.clear();
    stdscr.addstr("Dica: Pressione [F] para pular as falas..");
    stdscr.refresh();
    time.sleep(tempoDeDica);
    #Limpamos para mostrar a fala
    stdscr.clear();
    #
    while stdscr.getch() != -1:
        pass;
    #
    for i, texto in enumerate(dialogo):
        msg = "";
        texto = texto.format(playerName = player.nome)
        for char in texto:
            msg += char;
            if textoPermanente == True :
                stdscr.addstr(PosicaoNaTela.y+i, PosicaoNaTela.x,f"{falante}: {msg}");
            else:
                stdscr.addstr(PosicaoNaTela.y, PosicaoNaTela.x,f"{falante}: {msg}");
            stdscr.refresh();
            winsound.Beep(1300,1);
            time.sleep(tempoDeFala);
            #Aqui deixamos o jogador apertar espaço para pular a fala
            if stdscr.getch() == ord('f'):
                msg = texto;
                if textoPermanente == True :
                    stdscr.addstr(PosicaoNaTela.y+i, PosicaoNaTela.x,f"{falante}: {msg}");
                else:
                    stdscr.addstr(PosicaoNaTela.y, PosicaoNaTela.x,f"{falante}: {msg}");
                stdscr.refresh();
                break;
        #Mostramos a mensagem para o Jogador saber que pode pular o tempo de espera 
        if textoPermanente == True :
            stdscr.addstr(PosicaoNaTela.y+i, PosicaoNaTela.x,f"{falante}: {msg}");
        else:
            stdscr.addstr(PosicaoNaTela.y, PosicaoNaTela.x,f"{falante}: {msg}");
        stdscr.refresh();
        #Esperamos o tempo normal, ou o jogador aperta o espaco para pular
        timer = time.time();
        while time.time() - timer < tempoEntreFalas:
            if stdscr.getch() == ord('f'):
                break;
            time.sleep(0.05);
        if textoPermanente == False:
            stdscr.clear();
            # Espera o Input do Jogador para a próxima fala
#########################################################################################################################





