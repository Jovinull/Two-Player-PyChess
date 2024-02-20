import pygame

pygame.init()

# Definindo Tamanho da Tela
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Define o Nome da Janela
pygame.display.set_caption('Two-Player PyChess')
# Define o Icon da Janela
icon = pygame.image.load('assets/images/black knight.png')
pygame.display.set_icon(icon)

# Criando Fontes para o Jogo
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

# Cria um Objeto para Ajudar a Controlar o Tempo
timer = pygame.time.Clock()

# Frames Mostrados por Unidade de Tempo (Segundos)
fps = 60

# Variáveis de Jogo e Imagens
# Lista das Peças que Estão no Tabuleiro
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

# Peças Capturadas
captured_pieces_white = []
captured_pieces_black = []

# Estado de Cada Turno
#   0 - Turno das Brancas, Não Selecionado
#   1 - Turno das Brancas, Peça Selecionado
#   2 - Turno das Pretas , Não Selecionado
#   3 - Turno das Pretas , Peça Selecionado
turn_step = 0

# Peça que foi Selecionado (100 porque é um número alto)
selection = 100

# Lista dos Movimentos Válidos (Quando selecionamos uma peça iremos analisar as posições possíveis)
valid_moves = []

# Carregando as Imagens das Peças
#    > Carregamos a Imagem
#    > Transformamos em uma Maior Escala para o Tabuleiro
#    > Criamos uma nova variável e reduzimos o tamanho para exibir ao lado do Tabuleiro
black_queen        = pygame.image.load('assets/images/black queen.png')
black_queen        = pygame.transform.scale(black_queen, (80, 80))
black_queen_small  = pygame.transform.scale(black_queen, (45, 45))
black_king         = pygame.image.load('assets/images/black king.png')
black_king         = pygame.transform.scale(black_king, (80, 80))
black_king_small   = pygame.transform.scale(black_king, (45, 45))
black_rook         = pygame.image.load('assets/images/black rook.png')
black_rook         = pygame.transform.scale(black_rook, (80, 80))
black_rook_small   = pygame.transform.scale(black_rook, (45, 45))
black_bishop       = pygame.image.load('assets/images/black bishop.png')
black_bishop       = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight       = pygame.image.load('assets/images/black knight.png')
black_knight       = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn         = pygame.image.load('assets/images/black pawn.png')
black_pawn         = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small   = pygame.transform.scale(black_pawn, (45, 45))
white_queen        = pygame.image.load('assets/images/white queen.png')
white_queen        = pygame.transform.scale(white_queen, (80, 80))
white_queen_small  = pygame.transform.scale(white_queen, (45, 45))
white_king         = pygame.image.load('assets/images/white king.png')
white_king         = pygame.transform.scale(white_king, (80, 80))
white_king_small   = pygame.transform.scale(white_king, (45, 45))
white_rook         = pygame.image.load('assets/images/white rook.png')
white_rook         = pygame.transform.scale(white_rook, (80, 80))
white_rook_small   = pygame.transform.scale(white_rook, (45, 45))
white_bishop       = pygame.image.load('assets/images/white bishop.png')
white_bishop       = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight       = pygame.image.load('assets/images/white knight.png')
white_knight       = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn         = pygame.image.load('assets/images/white pawn.png')
white_pawn         = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small   = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]

small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]

# Essa lista é responsável por associar a imagem de um peça com seu nome
#    > Na lista das 'images' o indice delas correspondem ao indice da 'piece_list'
#      EXEMPLO: A imagem do Knight em 'images' é o indice 3 nessa lista e em 'piece_list' também
#    > E na lista de 'pieces' o nome correspodem ao nome em 'piece_list'
#      EXEMPLO: Os nomes das peças tanto na lista de peças quanto nessa possuem o mesmo nome
# Desse modo criamos um vinculo entre a "peça" e sua imagem correspondente uma vez que ao chamar pelo
# nome na lista das peças no tabuleiro esse nome em 'piece_list' estará vinculado a um indice que é o
# da sua imagem correspondente na lista das imagens.
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# Variáveis de Checagem
counter = 0
winner = ''
game_over = False

def draw_board():
    """
    Desenha o tabuleiro principal do jogo de xadrez.

    O tabuleiro é composto por quadrados de 100x100 pixels, alternando entre 'light gray' e 'gray'.
    As linhas e colunas são desenhadas para delimitar os quadrados.
    Além disso, existem retângulos dourados nas bordas e um texto de status na parte inferior.

    Parametros:
        Nenhum

    Retorna:
        Nenhum
    """

    # Itera sobre os 32 quadrados do tabuleiro
    for i in range(32):
        column = i % 4
        row = i // 4

        # Determina a cor do quadrado baseado na linha e coluna
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])

    # Desenha as linhas horizontais e verticais do tabuleiro
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

    # Desenha os retângulos dourados nas bordas
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
    pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
    pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)

    # Exibe o texto de status na parte inferior
    status_text = ['Brancas: Selecione uma Peça!', 'Brancas: Selecione um Local!',
                   'Pretas: Selecione uma Peça!', 'Pretas: Selecione um Local']
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))

    # Exibe o botão "EMPATE" na parte superior direita
    screen.blit(medium_font.render('EMPATE', True, 'black'), (810, 830))

def draw_pieces():
    """
    Desenha as peças no tabuleiro.

    Para cada peça branca e preta, a função verifica o tipo de peça e desenha a imagem correspondente
    nas coordenadas específicas do tabuleiro. Além disso, destaca a peça selecionada com uma borda colorida.

    Parâmetros:
        Nenhum

    Retorna:
        Nenhum
    """

    # Desenha as peças brancas no tabuleiro
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])

        # Verifica se a peça é um peão e desenha a imagem apropriada
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))

        # Destaca a peça selecionada com uma borda vermelha se for a vez das brancas
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)

    # Desenha as peças pretas no tabuleiro
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])

        # Verifica se a peça é um peão e desenha a imagem apropriada
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))

        # Destaca a peça selecionada com uma borda azul se for a vez das pretas
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)

def check_options(pieces, locations, turn):
    """
    Verifica todas as opções válidas de movimento para as peças no tabuleiro.

    Para cada peça no tabuleiro, a função chama a função apropriada de verificação de movimento
    com base no tipo de peça ('pawn', 'rook', 'knight', 'bishop', 'queen', 'king'). As opções de movimento
    são armazenadas em uma lista e, no final, uma lista contendo todas as listas de movimento é retornada.

    Parâmetros:
        pieces (list): Lista contendo os tipos de peças ('pawn', 'rook', 'knight', 'bishop', 'queen', 'king').
        locations (list): Lista contendo as coordenadas das peças no tabuleiro.
        turn (int): Indica de quem é a vez de jogar (0 para brancas, 1 para pretas).

    Retorna:
        all_moves_list (list): Lista de listas, onde cada lista contém as opções de movimento para uma peça.
    """

    moves_list = []  # Lista para armazenar as opções de movimento de uma peça
    all_moves_list = []  # Lista que conterá todas as listas de opções de movimento

    # Itera sobre todas as peças no tabuleiro
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]

        # Chama a função apropriada de verificação de movimento com base no tipo de peça
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)

        # Adiciona a lista de opções de movimento à lista geral
        all_moves_list.append(moves_list)

    # Retorna a lista de todas as opções de movimento
    return all_moves_list

def check_king(position, color):
    """
    Verifica as opções de movimento para o rei em uma determinada posição.

    O rei pode mover-se para qualquer uma das 8 posições adjacentes, incluindo diagonais e horizontais/verticais.
    A função verifica se a posição alvo está dentro dos limites do tabuleiro e não contém uma peça amiga.

    Parâmetros:
        position (tuple): Tupla contendo as coordenadas (x, y) do rei no tabuleiro.
        color (str): Cor do rei ('white' para branco, 'black' para preto).

    Retorna:
        moves_list (list): Lista contendo as opções de movimento para o rei na posição dada.
    """

    moves_list = []  # Lista para armazenar as opções de movimento para o rei

    # Determina as listas de coordenadas das peças amigas e inimigas com base na cor do rei
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Define as 8 posições possíveis para o rei se mover
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

    # Itera sobre as posições possíveis
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])

        # Verifica se a posição alvo está dentro dos limites do tabuleiro e não contém uma peça amiga
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    # Retorna a lista de opções de movimento para o rei
    return moves_list

def check_queen(position, color):
    """
    Verifica as opções de movimento para a rainha em uma determinada posição.

    A rainha pode se mover tanto na diagonal quanto horizontal/vertical. A função utiliza as
    funções de verificação de movimento da bispa (check_bishop()) e da torre (check_rook()) para
    obter as opções de movimento da rainha.

    Parâmetros:
        position (tuple): Tupla contendo as coordenadas (x, y) da rainha no tabuleiro.
        color (str): Cor da rainha ('white' para branco, 'black' para preto).

    Retorna:
        moves_list (list): Lista contendo as opções de movimento para a rainha na posição dada.
    """

    # Obtém as opções de movimento da rainha combinando as opções da bispa e da torre
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)

    # Adiciona as opções da torre à lista de opções da rainha
    for i in range(len(second_list)):
        moves_list.append(second_list[i])

    # Retorna a lista de opções de movimento para a rainha
    return moves_list

def check_bishop(position, color):
    """
    Verifica as opções de movimento para o bispo em uma determinada posição.

    O bispo pode se mover ao longo das diagonais. A função verifica as quatro direções diagonais
    (cima-direita, cima-esquerda, baixo-direita, baixo-esquerda) e adiciona as opções de movimento à lista.

    Parâmetros:
        position (tuple): Tupla contendo as coordenadas (x, y) do bispo no tabuleiro.
        color (str): Cor do bispo ('white' para branco, 'black' para preto).

    Retorna:
        moves_list (list): Lista contendo as opções de movimento para o bispo na posição dada.
    """

    moves_list = []  # Lista para armazenar as opções de movimento para o bispo

    # Determina as listas de coordenadas das peças amigas e inimigas com base na cor do bispo
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Itera sobre as quatro direções diagonais
    for i in range(4):
        path = True
        chain = 1

        # Define os valores de x e y com base na direção diagonal atual
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1

        # Verifica as opções de movimento ao longo da diagonal
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))

                # Se encontrar uma peça inimiga, interrompe a verificação naquela direção
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False

                chain += 1
            else:
                path = False

    # Retorna a lista de opções de movimento para o bispo
    return moves_list

def check_rook(position, color):
    """
    Verifica as opções de movimento para a torre em uma determinada posição.

    A torre pode se mover ao longo das direções horizontal e vertical. A função verifica as
    quatro direções (cima, baixo, direita, esquerda) e adiciona as opções de movimento à lista.

    Parâmetros:
        position (tuple): Tupla contendo as coordenadas (x, y) da torre no tabuleiro.
        color (str): Cor da torre ('white' para branco, 'black' para preto).

    Retorna:
        moves_list (list): Lista contendo as opções de movimento para a torre na posição dada.
    """

    moves_list = []  # Lista para armazenar as opções de movimento para a torre

    # Determina as listas de coordenadas das peças amigas e inimigas com base na cor da torre
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Itera sobre as quatro direções (cima, baixo, direita, esquerda)
    for i in range(4):
        path = True
        chain = 1

        # Define os valores de x e y com base na direção atual
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0

        # Verifica as opções de movimento ao longo da direção
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))

                # Se encontrar uma peça inimiga, interrompe a verificação naquela direção
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False

                chain += 1
            else:
                path = False

    # Retorna a lista de opções de movimento para a torre
    return moves_list

def check_pawn(position, color):
    """
    Verifica as opções de movimento para o peão em uma determinada posição.

    As opções de movimento do peão incluem avançar uma ou duas casas na direção vertical, capturar
    peças diagonais e condições específicas para o avanço inicial de duas casas. A função verifica as
    condições de movimento com base na cor do peão.

    Parâmetros:
        position (tuple): Tupla contendo as coordenadas (x, y) do peão no tabuleiro.
        color (str): Cor do peão ('white' para branco, 'black' para preto).

    Retorna:
        moves_list (list): Lista contendo as opções de movimento para o peão na posição dada.
    """
    
    moves_list = [] # Lista para armazenar as opções de movimento para o peão
    
    # Determina as listas de coordenadas das peças brancas e pretas com base na cor do peão
    if color == 'white':
        # Movimento para frente (uma casa)
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        
        # Movimento inicial para frente (duas casas) se o peão estiver na linha inicial
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        
        # Captura de peças inimigas na diagonal direita
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        
        # Captura de peças inimigas na diagonal esquerda
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        # Movimento para frente (uma casa)
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        
        # Movimento inicial para frente (duas casas) se o peão estiver na linha inicial
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
            
        # Captura de peças inimigas na diagonal direita
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
            
        # Captura de peças inimigas na diagonal esquerda
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

def check_knight(position, color):
    """
    Verifica as opções de movimento para o cavalo em uma determinada posição.

    O cavalo pode se mover em um padrão "L", indo duas casas em uma direção e uma em outra.
    A função verifica as oito posições possíveis para o cavalo e adiciona as opções de movimento à lista.

    Parâmetros:
        position (tuple): Tupla contendo as coordenadas (x, y) do cavalo no tabuleiro.
        color (str): Cor do cavalo ('white' para branco, 'black' para preto).

    Retorna:
        moves_list (list): Lista contendo as opções de movimento para o cavalo na posição dada.
    """
    
    moves_list = [] # Lista para armazenar as opções de movimento para o cavalo
    
    # Determina as listas de coordenadas das peças amigas e inimigas com base na cor do cavalo
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations

    # Define as 8 posições possíveis para o cavalo se mover
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    
    # Itera sobre as posições possíveis
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        
        # Verifica se a posição alvo está dentro dos limites do tabuleiro e não contém uma peça amiga
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    # Retorna a lista de opções de movimento para o cavalo
    return moves_list

def check_valid_moves():
    """
    Verifica as opções de movimento válidas para a peça atualmente selecionada.

    A função verifica a vez de quem está jogando (brancas ou pretas) e obtém a lista de opções
    de movimento correspondente. Em seguida, retorna a lista de opções de movimento válidas para a
    peça atualmente selecionada.

    Parâmetros:
        Nenhum

    Retorna:
        valid_options (list): Lista contendo as opções de movimento válidas para a peça selecionada.
    """
    # Verifica a vez de quem está jogando
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options

    # Obtém a lista de opções de movimento para a peça atualmente selecionada
    valid_options = options_list[selection]

    # Retorna a lista de opções de movimento válidas
    return valid_options

def draw_valid(moves):
    """
    Desenha os movimentos válidos na tela.

    A função recebe uma lista de posições de movimentos válidos e desenha círculos nessas posições
    na tela. A cor do círculo é determinada com base na vez de quem está jogando (vermelho para brancas,
    azul para pretas).

    Parâmetros:
        moves (list): Lista contendo as posições de movimentos válidos a serem desenhados.

    Retorna:
        Nenhum
    """
    
    # Determina a cor dos círculos com base na vez de quem está jogando
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'

    # Itera sobre as posições de movimentos válidos e desenha círculos nelas
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

def draw_captured():
    """
    Desenha as peças capturadas na lateral da tela.

    A função desenha as peças capturadas pelos jogadores na lateral da tela. As peças capturadas
    brancas são representadas por pequenas imagens pretas, enquanto as peças capturadas pretas são
    representadas por pequenas imagens brancas.

    Parâmetros:
        Nenhum

    Retorna:
        Nenhum
    """

    # Desenha as peças capturadas brancas
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))

    # Desenha as peças capturadas pretas
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))

# draw a flashing square around king if in check
def draw_check():
    """
    Desenha um quadrado piscante ao redor do rei se estiver em xeque.

    A função verifica se o rei de um jogador está em xeque, e se estiver, desenha um quadrado
    piscante ao redor dele. A cor do quadrado é vermelha se as brancas estiverem em xeque, e azul
    se as pretas estiverem em xeque.

    Parâmetros:
        Nenhum

    Retorna:
        Nenhum
    """
    
    # Verifica a vez de quem está jogando
    if turn_step < 2:
        # Verifica se o rei branco está em xeque
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            
            # Verifica se o rei branco está em uma posição de movimento das peças pretas
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    
                    # Desenha um quadrado piscante ao redor do rei branco se estiver em xeque
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        # Verifica se o rei preto está em xeque
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]

            # Verifica se o rei preto está em uma posição de movimento das peças brancas
            for i in range(len(white_options)):
                if king_location in white_options[i]:

                    # Desenha um quadrado piscante ao redor do rei preto se estiver em xeque
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)

def draw_game_over():
    """
    Desenha a tela de fim de jogo na tela.

    A função desenha um retângulo preto na tela com uma mensagem indicando o vencedor do jogo e
    instruções para reiniciar. A mensagem exibe o nome do vencedor, e o texto adicional instrui
    o jogador a pressionar ENTER para reiniciar o jogo.

    Parâmetros:
        Nenhum

    Retorna:
        Nenhum
    """
    
    # Desenha um retângulo preto na tela
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    
    # Exibe a mensagem indicando o vencedor do jogo
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    
    # Exibe a mensagem adicional instruindo a pressionar ENTER para reiniciar
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()