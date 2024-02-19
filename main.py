from ctypes import pointer
import select
import pygame

pygame.init()

# Definindo Tamanho da Tela
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Define o Nome da Janela
pygame.display.set_caption('Two-Player PyChess')
# Define o Icon da Janela
icon = pygame.image.load('assets/images/black knight.png')
pygame.display.set_icon(icon)

# Criando Fontes para o Jogo
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)

# Cria um Objeto para Ajudar a Controlar o Tempo
timer = pygame.time.Clock()
# Frames Mostrados por Unidade de Tempo (Segundos)
fps = 60

# Variáveis de Jogo e Imagens
# Lista das Peças que Estão no Tabuleiro
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn'  , 'pawn'  , 'pawn', 'pawn' , 'pawn'  , 'pawn'  , 'pawn']

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn'  , 'pawn'  , 'pawn', 'pawn' , 'pawn'  , 'pawn'  , 'pawn']

# Lista da Localização das Peças
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1) , (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                  (0, 6) , (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

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
    Desenha o tabuleiro de xadrez usando o Pygame.

    A função desenha as casas do tabuleiro em cores alternadas, adiciona linhas e
    destaca a borda do tabuleiro. Além disso, desenha linhas de grade para indicar
    as posições no tabuleiro.

    Parâmetros:
    - Nenhum

    Retorno:
    - Nenhum
    """

    # Loop para desenhar as 32 casas do tabuleiro
    for i in range(32):
        column = i % 4
        row = i // 4

        # Verifica se a linha é par ou ímpar para alternar as cores das casas
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])

    # Desenha a linha horizontal inferior do tabuleiro
    pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])

    # Desenha a borda dourada ao redor do tabuleiro
    pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)

    # Loop para desenhar linhas horizontais e verticais que formam a grade do tabuleiro
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

def draw_pieces():
    """
    Desenha as peças no tabuleiro de xadrez usando o Pygame.

    A função utiliza informações sobre as posições e tipos de peças para desenhar
    as peças brancas e pretas no tabuleiro. Além disso, destaca a peça selecionada
    com uma borda colorida, dependendo da etapa do turno.

    Parâmetros:
    - Nenhum

    Retorno:
    - Nenhum
    """

    # Loop para desenhar peças brancas
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])

        # Desenha peão branco
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            # Desenha outras peças brancas
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))

        # Destaca a peça selecionada na primeira etapa do turno
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)

    # Loop para desenhar peças pretas
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])

        # Desenha peão preto
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            # Desenha outras peças pretas
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))

        # Destaca a peça selecionada na segunda etapa do turno
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)

def check_options(pieces, locations, turn):
    """
    Verifica todas as opções válidas de movimento para as peças no tabuleiro de xadrez.

    A função itera sobre as peças fornecidas, chamando funções específicas para cada tipo
    de peça (peão, torre, cavalo, bispo, rainha, rei) para determinar os movimentos possíveis
    em um único turno. O resultado é uma lista contendo todas as opções de movimento para
    cada peça.

    Parâmetros:
    - pieces: Lista contendo os tipos de peças no tabuleiro.
    - locations: Lista contendo as localizações das peças no tabuleiro.
    - turn: Indicação do turno atual no jogo.

    Retorno:
    - all_moves_list: Lista contendo listas de movimentos válidos para cada peça.
    """

    # Lista para armazenar os movimentos de cada peça
    moves_list = []
    # Lista para armazenar os movimentos de todas as peças
    all_moves_list = []
    
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        
        # OBS: Passamos de quem é o turno, pois uma peça de mesma cor não pode se mover contra uma peça aliada
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

        # Adiciona a lista de movimentos da peça atual à lista global
        all_moves_list.append(moves_list)

    # Retorna a lista global de movimentos de todas as peças
    return all_moves_list

# Verifica os movimentos válidos apenas para a peça selecionada
def check_valid_moves():
    """
    Verifica os movimentos válidos apenas para a peça atualmente selecionada no jogo de xadrez.

    A função determina a lista de opções válidas com base no estado do turno e na peça atualmente
    selecionada. Se o turno estiver na primeira etapa, a função utiliza as opções para as peças
    brancas; caso contrário, utiliza as opções para as peças pretas.

    Parâmetros:
    - Nenhum

    Retorno:
    - valid_options: Lista de tuplas representando as posições válidas para a peça selecionada se mover.
    """

    # Verifica o turno atual para determinar a lista de opções
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options

    # Obtém as opções válidas para a peça atualmente selecionada
    valid_options = options_list[selection]

    # Retorna a lista de opções válidas
    return valid_options

def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
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
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# draw valid moves on  screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'

    else:
        color = 'blue'

    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 500), 5)

def check_pawn(position, color):
    """
    Verifica os movimentos válidos de um peão no tabuleiro de xadrez.

    A função recebe a posição atual e a cor do peão e determina os movimentos possíveis,
    incluindo avançar uma ou duas casas, capturar peças na diagonal e outros movimentos
    específicos para peões.

    Parâmetros:
    - position: Tupla representando a posição atual do peão no formato (x, y).
    - color: Cor do peão ('white' ou 'black').

    Retorno:
    - moves_list: Lista de tuplas representando as posições válidas para o peão se mover.
    """

    moves_list = []

    if color == 'white':
        # Avançar uma casa para frente
        if (position[0], position[1] + 1) not in white_locations and \
        (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))

        # Avançar duas casas para frente, caso seja o primeiro movimento
        if (position[0], position[1] + 2) not in white_locations and \
        (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))

        # Capturar peça na diagonal direita
        if (position[0] + 1, position[1] + 1) not in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))

        # Capturar peça na diagonal esquerda
        if (position[0] - 1, position[1] + 1) not in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))

    else:
        # Avançar uma casa para frente
        if (position[0], position[1] - 1) not in white_locations and \
        (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))

        # Avançar duas casas para frente, caso seja o primeiro movimento
        if (position[0], position[1] - 2) not in white_locations and \
        (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))

        # Capturar peça na diagonal direita
        if (position[0] + 1, position[1] - 1) not in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))

        # Capturar peça na diagonal esquerda
        if (position[0] - 1, position[1] - 1) not in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
            
    return moves_list

black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

# Loop Principal
run = True
while run:
    # Ajusta o Limite da Velocidade de Execução do Jogo
    timer.tick(fps)
    # Preenche a Tela com uma Cor Sólida
    screen.fill('dark gray')
    draw_board()
    draw_pieces()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    # Tratamento de Eventos
    for event in pygame.event.get():
        # Verifica se o X da Janela do Jogo foi Clicada
        if event.type == pygame.QUIT:
            run = False
            
        # Verificando o Click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            
            # Selecionando uma peça Branca
            if turn_step <= 1:
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1

            # Selecionando um movimento das Brancas
            if click_coords in valid_moves and selection != 100:
                white_locations[selection] = click_coords
                # Verificando se é uma captura
                if click_coords in black_locations:
                    black_piece = black_locations.index(click_coords)
                    captured_pieces_white.append(black_pieces[black_piece])
                    black_pieces.pop(black_piece)
                    black_locations.pop(black_piece)

                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 2
                selection = 100
                valid_moves = []
                
            # Selecionando uma peça Preta
            if turn_step > 1:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3

            # Selecionando um movimento das Pretas
            if click_coords in valid_moves and selection != 100:
                black_locations[selection] = click_coords
                # Verificando se é uma captura
                if click_coords in white_locations:
                    white_piece = white_locations.index(click_coords)
                    captured_pieces_black.append(white_pieces[white_piece])
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)

                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                selection = 100
                valid_moves = []

    # Atualiza a Tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
