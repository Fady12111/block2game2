import pygame
from copy import deepcopy
from  random import choice , randrange


W , H = 10 ,15
TILE = 45
GAME_REC = W * TILE , H * TILE
fps = 60
REC = 750 , 700

pygame.init()
sc = pygame.display.set_mode(REC)
game_sc = pygame.Surface(GAME_REC)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE , y * TILE , TILE , TILE ) for x in range(W)  for y in range(H) ]

figuers_pos = [[(-1,0),(-2,0),(0,0),(1,0)],
               [(0,-1),(-1,-1),(-1,0),(0,0)],
               [(-1,0),(-1,1),(0,0),(0,-1)],
               [(0,0),(-1,0),(0,1),(-1,-1)],
               [(0,0),(0,-1),(0,1),(-1,-1)],
               [(0,0),(0,-1),(0,1),(-1,-1)],
               [(0,0),(0,-1),(0,1),(-1,0)]]

figuers = [[pygame.Rect(x + W //2 , y + 1 ,1,1) for x,y in fig_pos] for fig_pos in figuers_pos]

figure_rect = pygame.Rect(0,0 , TILE - 2, TILE - 2)

field = [[0 for i in range(W)] for j in range(H)]

bg = pygame.image.load('bg.jpg').convert()
game_bg = pygame.image.load('bg2.jpg').convert()

get_color = lambda: (randrange(30 , 256) , randrange(30 , 256) , randrange(30 , 256))
color , next_color = get_color() , get_color()
figure , next_figure = deepcopy(choice(figuers)) , deepcopy(choice(figuers))

score = 0



main_font = pygame.font.Font('font.ttf' , 65)
font = pygame.font.Font('font.ttf' , 45)

tetris_font = main_font.render('TETRIS' , True , pygame.Color('darkorange'))
title_score = font.render('Score:' , True , pygame.Color('green'))


anim_count , anim_speed , anim_limet = 0,60,2000 




def chik_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx , rotate  = 0 , False
    sc.blit(bg , (0,0))
    sc.blit(game_sc , (20,20))
    game_sc.blit(game_bg , (0,0))






    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limet = 100
            elif event.key == pygame.K_UP:
                rotate = True            

    
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not chik_borders():
            figure = deepcopy(figure_old)
            break 

    anim_count += anim_speed
    if anim_count > anim_limet:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
          figure[i].y += 1
          if not chik_borders():
            for i in range(4):
               field[figure_old[i].y][figure_old[i].x] = color
            figure , color = next_figure , next_color


            next_figure , next_color = deepcopy(choice(figuers)) , get_color()
            anim_limet = 2000
            break         
    
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:   
       for i in range(4):
           x = figure[i].y - center.y
           y = figure[i].x  - center.x
           figure[i].x = center.x - x
           figure[i].y = center.y + y
           if not chik_borders():
               figure = deepcopy(figure_old)
               break
    line   = H - 1 
    for row in range(H - 1, -1 , -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            score += 100
                

               
       

 
  
    
    
    
    [pygame.draw.rect(game_sc , (40,40,40) , i_rect , 1) for i_rect in grid]

    for i in range(4):
        figure_rect.x = figure[i].x * TILE 
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc , color , figure_rect)         
   
    for y , raw in enumerate(field):
        for x , col in enumerate(raw):
            if col:
                figure_rect.x , figure_rect.y = x * TILE , y * TILE
                pygame.draw.rect(game_sc , col , figure_rect)
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380 
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc , next_color , figure_rect)            
    
    
    
    
    sc.blit(tetris_font , (485 , 0))
    sc.blit(title_score , (485 , 550))
    sc.blit(font.render(str(score) , True , pygame.Color('white') ), (485 , 600))
    
    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count , anim_speed , anim_limet = 0 , 60 ,2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc , get_color() , i_rect)
                sc.blit(game_sc , (20,20))
                pygame.display.flip()
                clock.tick(200)



    pygame.display.flip()
    clock.tick(fps)
