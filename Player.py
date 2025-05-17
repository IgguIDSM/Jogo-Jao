from utils import Vector2;


class Player (Vector2):
    _sala = "Dojo"; # define a sala de spawn do jogador
    #parametros do jogador
    _inventario = [];
    _vida = 100;
    _stamina = 100;
    #
    _position = Vector2(0,0);
    #
    def __init__(self,nome):
        self.nome = nome;