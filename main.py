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

# Function to check all pieces valid options on board
def check_options():
    pass

# Loop Principal
run = True
while run:
    # Ajusta o Limite da Velocidade de Execução do Jogo
    timer.tick(fps)
    # Preenche a Tela com uma Cor Sólida
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    
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
