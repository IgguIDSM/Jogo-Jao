from utils import Vector2;


class Player (Vector2):
    _sala = "Dojo"; # define a sala de spawn do jogador
    #parametros do jogador
    _Model = "i"
    _inventario = [];
    _Slots = 6;
    _vida = 100;
    _stamina = 100;
    #
    _position = Vector2(0,0);
    #
    def __init__(self,nome : str,inventario : list,vida : int,stamina : int ,position : Vector2,sala : str):
        self.nome = nome;
        self._inventario = inventario;
        self._vida = vida;
        self._stamina = stamina;
        self._position = position;
        self._sala = sala;
    #
    def GetInventario(self):
        return self._inventario
    #
    def GetStamina(self):
        return self._stamina;
    #
    def GetVida(self):
        return self._vida;
    #
    def GetPosition(self):
        return self._position;
    #
    def GetSala(self):
        return self._sala;
    #
    def SetSala(self,sala : str):
        self._sala = sala;
    #
    def SetPosition(self,Position : Vector2):
        self._position = Position;    
    #
    def Andar(self,direction : Vector2):
        self._position.x += direction.x;
        self._position.y += direction.y;
    #
    def GetModel(self):
        return self._Model;