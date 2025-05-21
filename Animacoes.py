import curses;
#
def TesteAnimacao(stdscr):
    curses.curs_set(0);
    stdscr.nodelay(True);

    spinner = ['-', '\\', '|', '/'];
    i = 0;
    
    #Responsavel pela animação
    # while True:
        # stdscr.addstr(10, 10, spinner[i % len(spinner)]);
        # stdscr.refresh();
        # time.sleep(0.1);
        # stdscr.addstr(10, 10, ' ');  # apaga o anterior
        # i += 1;





