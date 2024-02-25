import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400)) # create the game window
pygame.display.set_caption('Ultimate Pygame Tutorial') # set the window caption
clock = pygame.time.Clock() # create a clock object for controlling the framerate

# Create surfaces (Graphics holders) & Create rectangles (Position holders)

# Background Graphics
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha() # convert_alpha speeds up processing time
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Player Graphics
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

# Test Surface
# test_surface = pygame.Surface((100,200))
# test_surface.fill('Red') # fill the surface with a color

# Enemy Graphics
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (800,300))

# Snail Position
snail_x_pos = 800

# Create Font Object and Surface
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
text_surface = test_font.render('Score: ',False,'Black')

# Create Sounds
bruh_sound = pygame.mixer.Sound('audio/bruh.mp3')

# Global Variables
player_is_hit = False

# Game Loop
while True:
    # Update everything

    # Move the snail
    if snail_rect.right>0:
        snail_rect.right-=6
    else:
        snail_rect.left = 800

    # collision detection on player
    if player_rect.colliderect(snail_rect) and player_is_hit==False:
        print('bruh you hit da snail')
        player_is_hit = True
        pygame.mixer.Sound.play(bruh_sound)
    elif not player_rect.colliderect(snail_rect) and player_is_hit==True:
        player_is_hit = False


    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # draw all our elements
    # screen.blit(test_surface,(0,0)) # BLIT = Block Image Transform (draw a surface onto another surface)

    # Draw background
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))

    # Draw Text
    screen.blit(text_surface,(300,50))

    # Draw Enemies
    screen.blit(snail_surf,snail_rect)

    # Draw Player
    screen.blit(player_surf,player_rect)


    pygame.display.update()
    clock.tick(60) # Restrict game loop to 60 fps (delays the next update call by 1/60s, wraps around SDL_Delay function)