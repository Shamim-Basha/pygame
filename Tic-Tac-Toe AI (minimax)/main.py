import pygame,random,copy
import numpy as np
pygame.init()

BOARD_ROWS = BOARD_COL = 3
WIDTH = 600
HEIGHT = WIDTH
SQR_SIZE = WIDTH // 3

CIRCLE_RADIUS = SQR_SIZE // 3
CIRCLE_WIDTH = 15

SPACE = SQR_SIZE // 4
CROSS_WIDTH = 23

WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(BLACK)
pygame.display.update()

board = np.zeros((BOARD_ROWS,BOARD_COL))
print(board)

def draw_start_menu():
    screen.fill((0,0,0))
    font = pygame.font.SysFont('arial',40)
    title = font.render('Tic-Tac-Toe',True,WHITE)
    pvp = font.render('(1) Player vs Player',True,WHITE)
    ran_ai = font.render('(2) Dumb AI',True,WHITE)
    ai = font.render('(3) AI',True,WHITE)
    quit = font.render('(Q) Quit',True,WHITE)

    screen.blit(title,(WIDTH // 2 - title.get_width()//2 , HEIGHT // 8 - title.get_height()//2 ))
    screen.blit(pvp,(WIDTH // 2 - pvp.get_width()//2 , HEIGHT // 8 - pvp.get_height()//2 + 2*HEIGHT//8))
    screen.blit(ran_ai,(WIDTH // 2 - pvp.get_width()//2 , HEIGHT // 8 - ran_ai.get_height()//2 + 3*HEIGHT//8))
    screen.blit(ai,(WIDTH // 2 - pvp.get_width()//2 , HEIGHT // 8 - ran_ai.get_height()//2 +4* HEIGHT//8))
    screen.blit(quit,(WIDTH // 2 - pvp.get_width()//2 , HEIGHT // 8 - quit.get_height()//2 + 5* HEIGHT//8 ))

    pygame.display.update()

def draw_lines(screen):
    #vertical line
    for k in range(1,3):
        pygame.draw.line(screen,WHITE,(k * SQR_SIZE, 0),(k * SQR_SIZE, HEIGHT),width=10)
        pygame.draw.line(screen,WHITE,(0, k * SQR_SIZE),(WIDTH, k * SQR_SIZE),width=10)

    pygame.display.update()

def draw_cross(screen,row,col):
    pygame.draw.line(screen,WHITE,(col*SQR_SIZE + SPACE, row*SQR_SIZE +SQR_SIZE - SPACE),(col*SQR_SIZE + SQR_SIZE - SPACE, row*SQR_SIZE + SPACE),CROSS_WIDTH)
    pygame.draw.line(screen,WHITE,(col*SQR_SIZE + SPACE, row*SQR_SIZE +SPACE),(col*SQR_SIZE + SQR_SIZE - SPACE, row*SQR_SIZE +SQR_SIZE - SPACE),CROSS_WIDTH)

def draw_circle(screen,row,col):
    pygame.draw.circle(screen,WHITE,(int(col*SQR_SIZE + SQR_SIZE / 2),int(row*SQR_SIZE + SQR_SIZE / 2)),CIRCLE_RADIUS,CIRCLE_WIDTH)

def draw_fig(board,screen):
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                draw_cross(screen,row,col)
            elif board[row][col] != 0:
                draw_circle(screen,row,col)
            
    pygame.display.update()

def is_available(board,row,col):
    return True if board[row][col] == 0 else False

def is_full(board):
    for i in range(len(board)):
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True

def check_win(board):
    #vertical win
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:    
            pygame.draw.line(screen,WHITE,( i*SQR_SIZE + SQR_SIZE // 2, SQR_SIZE//8),(i*SQR_SIZE + SQR_SIZE // 2, HEIGHT-SQR_SIZE//8),SQR_SIZE//8)
            return int(board[0][i])
        
    #horizontal win
    for j in range(3):
        if board[j][0] == board[j][1] == board[j][2] and board[j][0] != 0:
            pygame.draw.line(screen,WHITE, (SQR_SIZE // 8,j*SQR_SIZE + SQR_SIZE // 2) , (WIDTH - SQR_SIZE // 8,j*SQR_SIZE + SQR_SIZE // 2),SQR_SIZE // 8)    
            return int(board[j][0])
        
    #asc_diagonal win
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != 0:    
        pygame.draw.line(screen,WHITE, (SQR_SIZE // 8,HEIGHT - SQR_SIZE // 8) , (WIDTH - SQR_SIZE // 8,SQR_SIZE // 8),SQR_SIZE // 8)
        return int(board[1][1])
    
    #dsc_diagonal win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        pygame.draw.line(screen,WHITE, (SQR_SIZE // 8,SQR_SIZE // 8) , (WIDTH - SQR_SIZE // 8, HEIGHT - SQR_SIZE // 8 ),SQR_SIZE // 8)
        return int(board[2][2])
    
    # return False
def get_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                moves.append((i,j))
    return moves
def ai(board):

    eval,move = minimax(board,False)
    print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')
    board[move[0]][move[1]] = 3
    draw_fig(board,screen)
    print(board)
    
def dumb_ai(board):
    moves = get_moves(board)
    move = moves[random.randint(0,len(moves))-1]
    board[move[0]][move[1]] = 3
    draw_fig(board,screen)

def check_state(board):
    #vertical win
    for bar in range(3):
        if board[0][bar] == board[1][bar] == board[2][bar] and board[0][bar] != 0:    
            return int(board[0][bar])
        
    #horizontal win
    for foo in range(3):
        if board[foo][0] == board[foo][1] == board[foo][2] and board[foo][0] != 0:
            return int(board[foo][0])
        
    #asc_diagonal win
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != 0:    
        return int(board[1][1])
    
    #dsc_diagonal win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return int(board[2][2])
    
def minimax(board,maximizing):
    #checks terminal state
    case = check_state(board)
    if case == 1:
        return 1,None
    if case == 3:
        return -1,None
    if is_full(board):
        return 0,None
    
    if maximizing:
        max_eval = -100
        best_move = None
        moves = get_moves(board)
        for (row,col) in moves:
            tmp_board = copy.deepcopy(board)
            tmp_board[row][col] = 1
            eval = minimax(tmp_board,False)[0]
            if eval > max_eval:
                max_eval = eval
                best_move = (row,col)
        return max_eval,best_move
    
    if not maximizing:
        min_eval = 100
        best_move = None
        moves = get_moves(board)
        for (row,col) in moves:
            tmp_board = copy.deepcopy(board)
            tmp_board[row][col] = 3
            eval = minimax(tmp_board,True)[0]
            if eval < min_eval:
                min_eval = eval
                best_move = (row,col)
        return min_eval,best_move
    
game_state = 'start_menu'
draw_start_menu() 
while game_state == 'start_menu':
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_state = 'pvp'
                
            if event.key == pygame.K_2:
                game_state = 'ran_ai'
                
            if event.key == pygame.K_3:
                game_state = 'ai'
            if event.key == pygame.K_q:
                pygame.quit()
                

screen.fill(BLACK)
draw_lines(screen)    

game = True
player = 1
gamemode = game_state
while game == True:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONUP :
            mouse_x, mouse_y = event.pos[0], event.pos[1]
            clicked_row = int(mouse_y // SQR_SIZE)
            clicked_col = int(mouse_x // SQR_SIZE)

            if is_available(board,clicked_row,clicked_col):
                board[clicked_row][clicked_col] = player
                print(board)
                draw_fig(board,screen)

                if check_win(board):
                    pygame.display.update()
                    # print(minimax(board,False))
                    pygame.time.delay(1000)
                    game = False

                if is_full(board):
                    pygame.time.delay(1000)
                    game = False

                player = 1 if player == 2  else 2 
            
   
        if gamemode == 'ai' and player == 2 and game == True:
            ai(board)
            player = 1 
            if check_win(board):
                pygame.display.update()
                pygame.time.delay(1000)
                game = False

            if is_full(board):
                pygame.time.delay(1000)
                game = False
        if gamemode == 'ran_ai' and player == 2 and game == True:
            dumb_ai(board)
            player = 1 
            if check_win(board):
                pygame.display.update()
                pygame.time.delay(1000)
                game = False

            if is_full(board):
                pygame.time.delay(1000)
                game = False
           

                    

                
            
                


