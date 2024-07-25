import pygame

pygame.init()
d_width, d_height = 1200, 600 
screen = pygame.display.set_mode((d_width, d_height))
clock = pygame.time.Clock()
running  = True
position = set()
start = False
block_size = 20 
count = 0
update_freq = 10

def d_grid(col, fil, block_size):
    for x in range(0, col, block_size):
        for y in range(0, fil, block_size):   
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, (11, 103, 48), rect, 1)  

def d_block(position):
    for pos in position:
        col = pos[0] *20
        fil = pos[1] *20
        rect = pygame.Rect(col, fil, block_size, block_size)
        pygame.draw.rect(screen, (0, 128, 0), rect, 0)
        
def get_vecinos(pos, block_size, d_height, d_width):
    vecinos = set()
    x, y = pos

    for dx in [-1, 0, 1]:
        if (x + dx < 0) or (x + dx > d_width):
            continue

        for dy in [-1, 0, 1]:
            if (y + dy < 0) or (y + dy > d_height):
                continue

            if (dx == 0 and dy == 0):
                continue

            vec_pos_x = x + dx
            vec_pos_y = y + dy

            vecinos.add((vec_pos_x, vec_pos_y))
            
    return vecinos 

def adjust_grid(position):
    all_vecinos = set()
    new_position = set()
    
    for pos in position:
        vecinos = get_vecinos(pos, block_size, d_height, d_width)
        all_vecinos.update(vecinos)

        vecinos_vivos = [x for x in vecinos if x in position]
        
        if len(vecinos_vivos) in [2, 3]:
            new_position.add(pos)

    for pos in all_vecinos:
        vecinos = get_vecinos(pos, block_size, d_height, d_width)
        vecinos_vivos = [x for x in vecinos if x in position]

        if len(vecinos_vivos) == 3:
            new_position.add(pos)

    return new_position

d_grid(d_width, d_height, block_size)
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        #con espacio se empieza el juego y ya no permite ingresar celulas
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and start == False:
            start = True

        #el ingreso del set up inicial de las celulas
        if pygame.mouse.get_pressed(num_buttons=3)[0] and start == False:
            x,y = pygame.mouse.get_pos()
            position.add((x // block_size,y // block_size))
            d_block(position)

    #control de las reglas del juego
    if start:
        if count >= update_freq:
            count = 0
            position = adjust_grid(position)
            screen.fill((0,0,0))
            d_grid(d_width, d_height, block_size)
            d_block(position)

    count += 1

    pygame.display.flip()

    clock.tick(60)

pygame.quit()


