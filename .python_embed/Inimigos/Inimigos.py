from Common.Player import Player;
from Utils.Math_Utils import Vector2;
from Utils.Event import Event;

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
    _mobTick = 0;
    _OnMobDamage = Event();
    #CallBacks
    _onMobKilledCallBack = None;
    #
    def __init__(self,spawnPosition : Vector2, nome : str, modelo : str, vida : int, sala : str, dano : int, velocidade : int, tempoDeAtaque : float, OnMobKilledCallBack = None, target : Player = None):
        self._position = spawnPosition;
        self._model = modelo;
        self._nome = nome;
        self._vida = vida;
        self._sala = sala;
        self._dano = dano;
        self._velocidade = velocidade;
        self._tempoDeAtaque = tempoDeAtaque;
        self._onMobKilledCallBack = OnMobKilledCallBack;
        self._OnMobDamage = Event();
        self._target = target;
    #
    def MobTick(self,frameTime):
        self._mobTick += frameTime;
    #
    def ResetMobTick(self):
        self._mobTick = 0;
    #
    def Damage(self,amount):
        self._vida -= amount;
        self._OnMobDamage.Trigger(self.GetPosition(),self._vida);
    #
    def GetDamage(self):
        return self._dano;
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
    def OnMobKilled(self):
        if self._onMobKilledCallBack != None:
            self._onMobKilledCallBack();
    #
    def Andar(self,direction : Vector2):
        self._position.x += direction.x;
        self._position.y += direction.y;
    #
    def _getRelativeValue(value,minimum,maximum):
        return (value-minimum)/(maximum/minimum);
    #
    def GetModel(self):
        return self._model;
    #
    def GetBarraDeVida(self):
        am = self._vida//25;
        return f"{'-'*am}";

#----------------------------------------------------------------