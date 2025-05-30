from Utils.Math_Utils import Vector2;
from Utils.Event import Event;
class Player (Vector2):
    _sala = "Dojo"; # define a sala de spawn do jogador
    #parametros do jogador
    _Classe = "";
    _MissaoAtual = "";
    _Model = "i"
    _inventario = [];
    _Slots = 6;
    _vida = 100;
    _stamina = 100;
    _dano = 5;
    _velocidade = 0;
    _RetaFinal = False;
    #Internos
    _EspadaL = "\\";
    _EspadaR = "/";
    #
    _ArcoL = "(";
    _ArcoR = ")";
    #Eventos
    _OnRoomChangedEvent = Event();
    #
    _position = Vector2(0,0);
    _lastDir = Vector2(0,0);
    _facingDir = Vector2(0,0);
    #
    def __init__(self,nome : str,MissaoAtual : str, classe : str, inventario : list,vida : int,stamina : int , velocidade : float, position : Vector2,sala : str):
        self.nome = nome;
        self._MissaoAtual = MissaoAtual;
        self._Classe = classe;
        self._inventario = inventario;
        self._vida = vida;
        self._stamina = stamina;
        self._position = position;
        self._sala = sala;
        self._OnRoomChangedEvent = Event();
        self._velocidade = velocidade;
    #
    def SetVida(self,amount):
        self._vida = amount;
    #
    def AddInventario(self, item):
        self._inventario.append(item);
    #
    def Damage(self,amount):
        self._vida -= amount;
    #
    def SetDamage(self,dano):
        self._dano = dano;
    #
    def GetDamage(self):
        return self._dano;
    #
    def GetMissaoAtual(self):
        return self._MissaoAtual;
    #
    def SetMissaoAtual(self,missao : str):
        self._MissaoAtual = missao;
    #
    def SetClasse(self, classe : str):
        self._Classe = classe;
    #
    def GetClasse(self):
        return self._Classe
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
        return Vector2(round(self._position.x),round(self._position.y));
    #
    def GetSala(self):
        return self._sala;
    #
    def SetSala(self,sala : str):
        self._sala = sala;
        self._OnRoomChangedEvent.Trigger(sala);
    #
    def SetPosition(self,Position : Vector2):
        self._position = Position;    
    #
    def SetStamina(self,amount):
        self._stamina = amount;
    #
    def RestoreStamina(self,frameTime,amount):
        if self._stamina < 100: 
            self._stamina += frameTime * amount;
        if self._stamina > 100:
            self._stamina == 100;
    def GetFacingDiretion(self):
        return self._facingDir;
    #
    def Andar(self,direction : Vector2):
        if (direction.x != self._lastDir.x) and direction.x != 0:
            self._lastDir.x = direction.x;
        if (direction.y != self._lastDir.y) and direction.y != 0:
            self._lastDir.y = direction.y;
        #
        self._facingDir = direction;
        # 
        self._position.x += direction.x * self._velocidade;
        self._position.y += direction.y * self._velocidade;
    #
    def GetModel(self):
        if self._lastDir.x > 0:
            if self._Classe == "Cavaleiro":
                return f"{self._Model}{self._EspadaR}";

            if self._Classe == "Arqueiro":
                return f"{self._Model}{self._ArcoR}";
        elif self._lastDir.x < 0:
            if self._Classe == "Cavaleiro":
                return f"{self._EspadaL}{self._Model}";
            
            if self._Classe == "Arqueiro":
                return f"{self._ArcoL}{self._Model}";
        return self._Model;
