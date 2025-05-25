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
    'DICA_PORTAS':
    [
        "As letras Presentes nas laterais do mapa representam Portas!",
        "Cada letra representa a direção que essa porta irá te levar",
        "Sendo as Possíveis portas (N,S,L,O) [Norte, Sul, Leste, Oeste]!",
        "Caso tenha dúvidas, é só chegar perto de uma porta.",
        "Que a dica de interação irá te dizer para qual sala ela te leva..",
    ],
    'DICA_COMBATE':
    [
        "Pressione [ESPACO] para atacar os inimigos",
        "A Sua distância de ataque é de 5 metros",
        "Os Mobs conseguem te atacar se chegarem muito perto!",
    ],
    'DICA_COMBATE1':
    [
        "As larvas não são muito rápidas, mas causam muito dano",
        "Talves atacar de uma distância segura seja mais adequado..",
    ],
    'DICA_LAMINA_LUZ':
    [
        "Nova Habilidade: Lâmina da Luz!",
        "Essa habilidade concentra toda a sua força em um único corte, causando um impacto poderoso",
        "E muito dano!, porém ao custo de 75 pontos de Stamina.",
        "é capaz de reduzir a vida do Monstro pela metade, e se caso o monstro tenha 50 pontos de vida",
        "será eliminado.."
    ]
}


#

DIALOGOS = {
    'INTRO':
        [
            "Bem Vindo ao Dungeons Conquest!",
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
                    "Olá jovem aventureiro, Bem vindo ao segundo andar, eu sou Sylveris, a Guardiã da Lâmina da Luz",
                    "eu te darei a próxima missão e se completar, você ganhará um item de sua escolha.",
                    "mas não pense que será fácil...",
                    "essas larvas são bem traiçoeiras...",
                    "Quero que você elimine essas larvas nojentas do meu jardim!"
                ]
            ],
            [
                'MISSAO'
            ]
        ],
    'Sylveris1':
        [
            [
                'Sylveris',
                [
                    "Parabéns aventureiro, você foi incrivel nessa missão derrotando esses monstros.. ",
                    "Como prometido você tem duas opções de escolha: O Anel da Emersão e o Colar de Vínculo",
                    "Qual você escolhe?"
                ],
                [
                    "Pobre aventureiro, não sabe o destino que lhe aguarda...",
                ]
            ]
        ],
    'Narrador_Terceiro_Andar':
        [
            [
                'Narrador',
                [
                    "Ao chegar no terceiro andar {playerName} se depara com um ambiente extremamente frio, onde a neve tomava conta...",
                    "de repende uma forte nevasca atinge {playerName}, e dessa nevasca aparece Gorzhak, um Orc de gelo.",
                ],
                [
                    "Antes que {playerName} pudesse perguntar qualquer coisa, Gorzhak some diante da neve espessa...",
                ],
                
            ]
        ],
    'Narrador_Morte_Velkar':
        [
            [
                'Narrador',
                [
                    "Antes de terminar sua fala, Velkar se desfaz como poeira ao vento..., deixando cair o primeiro fragmento de voz gélida."
                ]
            ]
        ],
    'Gorzhak':
        [
            [
                'Gorzhak',
                [
                    "Olá aventureiro, vejo que conseguiu vencer o desafio de Sylveris, eu sou Gorzhak, o Coração Congelado da Montanha Partida",
                    "Eu lhe darei sua última missão, e se provar que é dígno, lhe concederei a magia dos guardiões da luz, junto com a Espada Celeste.",
                    "Caso tenha sucesso neste desafio, peço que tome cuidado ao partir para enfrentar o Homem Sombra...",
                ],
                [
                    "O seu primeiro desafio será Velkar, dono da Lâmina Partida, um espectro sorrateiro, que utiliza ataques rápidos e cria cópias falsas de si mesmo..",
                    "O segundo e último e mais Forte é Thornak, o Indomável, Um Gigante de gelo com uma força descomunal...",
                ],
                [
                    "Após derrotar Velkar, poderá seguir adiante para o Thornak",
                    "Cada um deixará contigo um fragmento de voz gélida",
                    'Quando estiver com os dois fragmentos eu retornarei....',
                ]
            ]
        ],
    'Velkar':
        [
            [
                'Velkar',
                [
                    "Vejo que teve coragem o suficiente para me enfrentar, mas saiba que fui um grande guerreiro quando vivo e não serei derrotado facilmente...",
                    "VENHA AVENTUREIRO!!!",
                ],
                [
                    "Você foi incrível batalhando, obrigado por me libertar dessa prisão sem fim....",
                    "boa sorte com seus próximos desafios aventureiro....",
                    "Mais uma coisa....... tenha cuidado..........",
                    "esta dungeon é...............................",
                ]
            ]
        ],
    'Narrador_Thornak':
        [
            [
                'Narrador',
                [
                    "logo ao entrar na sala {playerName} acaba pisando em alguns galhos secos no chão acordando Thornak",
                    "Thornak olha para {playerName} com um olhar de desprezo e diz...",
                ]
            ]
        ],
    'Thornak':
        [
            [
                'Thornak',
                [
                    "Criatura insolente, você tem coragem de vir me enfrentar? Saiba que eu irei destrui-lo sem piedade...",
                ],
                [
                    "Incrivel aventureiro, você saiu vitorioso desse combate mas tem algo que preciso te contar...",
                    "cuidado com essa dungeon, ela não é uma dungeon normal, essa é uma dungeon viva...",
                    "que consome aos pouco todos dentro dela e os transformam em seus servos...",
                    "o monstro no ultimo andar é.....",
                ]
            ]
        ],
    'Narrador_Morte_Thornak': 
        [
            [
                'Narrador',
                [
                    "Depois de Thornak revelar um segredo da dungeon para {playerName} ele vira poeira, e de seu corpo cai o ultimo fragmento de voz gélida...",
                    "de repente os dois fragmentos começam a voar na frente de {playerName} virando uma runa extremamente brilhante",
                    "dessa runa aparece Gorzhak, que diz:",
                ]
            ]
        ],
    'Gorzhak1':
        [
            [
                'Gorzhak',
                [
                    "Realmente você é forte caro aventureiro, lutou contra três espectros e retornou com vida, bem, aqui está sua recompensa..."
                ],
                [
                    "Vejo que você está pronto para enfrentar o ultimo andar dessa dungeon, boa sorte aventureiro!"
                ]
            ]
        ],
    'Ezhariel2':
        [
            [
                'Ezhariel',
                [
                    "Ola grande aventureiro, vejo que sobreviveu ate o último andar, mas tem algo que eu não o contei, eu sou o chefe desta dungeon",
                    "Mais conhecido como Homem Sombra, mas pode me chamar de Litch...",
                ],
            ]
        ],
    'Litch':
        [
            [
                'Litch',
                [
                    "Agora a brincadeira acabou caro guerreiro, você me divertiu esse tempo que esteve nessa dungeon",
                    "mas agora eu irei destruí-lo e irei roubar sua alma",
                ],
                [
                    "Litch Invocando seu cajado encara {playerName} com um olhar feroz e diz:",
                ],
                [
                    "VOCÊ ESTÁ MORTO! MUAHAHAHAHA",
                ]
            ]
        ],
    'Final_1':
        [
            [
                'Narrador',
                [
                    "Litch, após ser derrotado cai de joelhos em frente a {playerName}",
                    "Aceitando seu destino, Litch é arrastado por correntes espectrais que surgem do chão, levando Litch",
                    "e o selando novamente...",
                    "{playerName} horrorizado com o que presenciou, percebe que o seu Anel da Emersão, começa a vibrar em seu dedo",
                    "e começa a voar bem a sua frente, de repente um portal surge e uma voz diz a {playerName} que essa é a saída.",
                    "ao retornar ao seu mundo, percebeu que havia retornado com todo o seu equipamento adquirido",
                    "{playerName} tenta explicar brevemente o que havia acontecido, pois na visão dos seus companheiros...",
                    "ele simplesmente havia tocado na pedra, sumido, e logo depois de alguns segundos, retornado...",
                ],
            ]
        ],
    'Final_2':
        [
            [
                'Narrador',
                [
                    "Litch, Após de ser derrotado, cai de joelhos em frente a {playerName}",
                    "Aceitando seu destino, Litch aguarda que as correntes apareçam para o levar...",
                    "Mas algo surpreendente acontece...",
                    "As correntes surgem do chão prendendo {playerName}",
                ],
                [
                    "Você me derrotou, mas por conta desse colar, você será forçado pela dungeon a se tornar o Novo Homem Sombra...",
                    "Até que seja derrotado, por um bravo guerreiro como você... e que tenha... escohido.... esse colar.....",
                ],
                [
                    "Após muita dificuldade para terminar sua fala, Litch perde totalmente suas forças, e é levado por uma luz intensa..",
                    "Litch é Liberto após séculos preso naquela dimensão e finalmente retorna para o seu mundo,",
                    "Do momento que tinha sido preso pela dungeon...",
                    "Enquanto {playerName} desmaiado, é transformado no novo Homem Sombra...",
                ],
                [
                    "Que pena, perdi o meu melhor guerreiro..., mas não tem problema...",
                    "Chegou mais um para a minha coleção......"
                ]
            ]
        ],
    'Creditos':
        [
            [
                'Creditos',
                [
                    "Desenvolvido por: Rafael Cardoso e Igor dos Santos Moura.",
                    "Sistema de Combate e movimentação: Igor dos Santos Moura.",
                    "História, Mapa e Personagens: Rafael Cardoso.",
                    "Sistema de Diálogos: Igor dos Santos Moura.",
                    "Habilidades e Items do Personagem: Rafael Cardoso.",
                    "Produção Geral: Rafael Cardoso.",
                    "Chefe de Desenvolvimento: Igor dos Santos Moura."
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





