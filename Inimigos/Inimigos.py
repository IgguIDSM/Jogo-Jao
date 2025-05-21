from Common.Player import Player;
from Utils.Math_Utils import Vector2;

class Mob (Vector2):

    _nome = "";
    _sala = "";
    _model = "*"
    _vida = 0;
    _dano = 0;
    _velocidade = 0;
    _tempoDeAtaque = 0;
    _position = Vector2(0,0);
    _target = Player;
    #
    def __init__(self,spawnPosition : Vector2, nome : str, modelo : str, vida : int, sala : str, dano : int, velocidade : int, tempoDeAtaque : float):
        self._position = spawnPosition;
        self._model = modelo;
        self._nome = nome;
        self._vida = vida;
        self._sala = sala;
        self._dano = dano;
        self._velocidade = velocidade;
        self._tempoDeAtaque = tempoDeAtaque;
    #
    def GetVelocity(self):
        return self._velocidade
    #
    def GetNome(self):
        return self._nome;
    #
    def SetTarget(self,player : Player):
        self._target = player;
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
    def DistanceToPlayer(self):
        return self._position.Distance(self._target.GetPosition());
    #
    def Andar(self,direction : Vector2):
        self._position.x += direction.x;
        self._position.y += direction.y;
    #
    def GetModel(self):
        return self._model;
#----------------------------------------------------------------