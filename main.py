import utils;
import mapa;
import time;
pause = False;

utils.ClearConsole();


def GameLoop():
    #while not pause:
        utils.ClearConsole();
        #Renderiza o Mapa
        utils.RenderRoom(mapa.Dojo);


###
if __name__ == "__main__":
    GameLoop();

