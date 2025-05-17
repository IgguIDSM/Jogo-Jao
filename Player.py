class Player:
    
    #parametros do jogador
    _inventario = [];
    _vida = 100;
    _stamina = 100;
    #
    def __init__(self,nome):
        self.nome = nome;