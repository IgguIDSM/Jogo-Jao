import utils;
#mostra o menu inicial
def prompt():
    print("\t\t\tBem vindo ao Dungeons Conquest!\n\nVocê deve coletar todos os seis items antes de lutar com o chefão que se encntra no Dojo.\n\n" \
    "Movimentos:\t'mover {direcao}' (mover norte, sul, leste, oeste)\n" \
    "\t'pegar {item}' (adiciona o item próximo ao inventário)\n\n");
#
    input("Pressione qualquer tecla para continuar...");

#mapa
salas = {
    'Espaco Liminal' : {'Norte': 'Labirinto de Espelhos', 'Sul': 'Bat Caverna', 'Leste': 'Bazar'},
    
    'Labirinto de Espelhos' : {'Sul' : 'Espaco Liminal', 'Item': 'Cristal'},

    'Bat Caverna' : {'Norte': 'Espaco Liminal', 'Leste': 'Vulcao', 'Item': 'Cajado'},

    'Bazar' : {'Oeste': 'Espaco Liminal', 'Norte': 'Armazen de Carne', 'Leste': 'Dojo', 'Item': 'Jujubas'},

    'Armazen de Carne' : {'Sul': 'Bazar', 'Leste': 'Poço de Areia Movediça', 'Item':'Figurinha'},

    'Vulcao': {'Oeste': 'Bat Caverna', 'Item': 'Corda'},

    'Dojo': {'Leste': 'Bazar', 'Chefao': 'Homem Sombra'},
}

#Acoes
acoes = ['Mover','Pegar','Sair'];
#
inventario = [];

#
sala_atual = 'Espaco Liminal';

#
msg = '';

utils.ClearConsole();
prompt();

#gameplay loop

while True:
    utils.ClearConsole();

    #mostra a informação para o player
    print(f"Você está Atualmente em {sala_atual}\nInventário : {inventario}\n{'-'*27}")

    #Mostra msg
    print(f"{msg}\n");

    #indicador de item
    if 'Item' in salas[sala_atual].keys():

        item_proximo = salas[sala_atual]['Item'];
        
        # se tem item perto do player, mostra pra ele
        if item_proximo not in inventario:
            print(f"Você vê um(a) {item_proximo}\n");
    
    
    #Encontro com o BOSSSS
    if "Chefao" in salas[sala_atual].keys():

        #perdey playboy
        if len(inventario) < 6:
            print(f"Você Perdeu a Batalha conta o {salas[sala_atual]['Chefao']}.");
            break;
        #É TETRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        else:
            print(f"Você Ganhou a batalha contra o {salas[sala_atual]['Chefao']}!!");
            break;

    #Movimetação
    movimento = input("Digite sua ação:\n");
    
    #dividimos o movimento em palavras separadas
    
    proxima_acao = movimento.split(" ");
    
    #a primeira palavra é a acão;
    acao = proxima_acao[0].title();
    #    
    #    
    # se tem mais de uma palavra, sabemos que o jogador quer algo
    if len(proxima_acao) > 1:
        item = proxima_acao[1:];
        direcao = proxima_acao[1].title();
        #
        item = ' '.join(item).title();
    # Movimento entre salas (Checa se a acao existe)
    if acao in acoes:
        if acao == "Mover":

            try:
                sala_atual = salas[sala_atual][direcao];
                msg = f"Você foi para a direção {direcao}"
            except:
                msg = "Você não pode se mover nesta direção!"
        #Pegar items
        if acao == 'Pegar': 
            try:
                if item == salas[sala_atual]['Item']:

                    if item not in inventario:

                        inventario.append(salas[sala_atual]['Item']);
                        msg = f"Você pegou um(a) {item}.";

                    else:
                        msg = f"Você já possui um(a) {item}.";
            except:
                msg = f"Não foi possível encontrar um(a) {item}."
        #Sair
        if acao == "Sair":
            break;

    #qualquer outra coisa digitada:
    else:
        msg = "Comando Inválido";