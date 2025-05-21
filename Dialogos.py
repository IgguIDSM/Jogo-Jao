import curses;
import time;
from Math_Utils import Vector2;


#Cada Diálogo é uma estrutura contendo o nome do personagem e os diálogos, sendo essa estrutura um dicionário podendo conter o personagem e as falas (se for fala unica).
#Se for diálogo de missão, terá respostas e conversas paralelas.

DIALOGOS = {
    'INTRO':
        [
            "Bem Vindo ao Dungeons Conquest!",
            "Fique a vontade para mudar as configurações no menu principal!",
            "O Jogo Possui três possíveis finais, aceita o desafio?",
            "Bom, Boa Jogatina!",
        ],
}
#



def EscreverDialogo(stdscr, falante : str, dialogo : list = [], PosicaoNaTela : Vector2 = Vector2(0,0), tempoDeFala : float = 0.05, tempoEntreFalas : int = 3, tempoDeDica : int = 3):
    curses.curs_set(0);
    stdscr.nodelay(True);
    stdscr.clear();
    stdscr.addstr("Dica: Pressione [ESPACO] para pular as falas..");
    stdscr.refresh();
    time.sleep(tempoDeDica);
    #Limpamos para mostrar a fala
    stdscr.clear();
    #
    for i, texto in enumerate(dialogo):
        msg = "";
        for char in texto:
            msg += char;
            stdscr.addstr(PosicaoNaTela.y+i, PosicaoNaTela.x,f"{falante}: {msg}");
            stdscr.refresh();
            time.sleep(tempoDeFala);
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
        timer = time.time();
        while time.time() - timer < tempoEntreFalas:
            if stdscr.getch() == ord(' '):
                break;
            time.sleep(0.05);
        # Espera o Input do Jogador para a próxima fala


