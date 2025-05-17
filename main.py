import utils;
import mapa;
import time;
pause = True;

utils.ClearConsole();


def GameLoop():

    print(utils.GetRoomSize(mapa.Dojo));
    


    while not pause:
        utils.ClearConsole();
        #Renderiza o Mapa
        utils.RenderRoom(mapa.Dojo);


###
if __name__ == "__main__":
    GameLoop();

