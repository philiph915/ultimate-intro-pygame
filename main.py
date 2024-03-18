import pygame
from sys import exit
from random import randint # Function to generate random integers
import math

def display_score():
    # PLACEHOLDER
    pass

# Function to move all the enemmies in the obstacle list
def obstacle_movement(obstacle_list):
    global obstacle_vel
    if obstacle_list: # returns 0 if list is empty

        for obstacle_rect in obstacle_list: # loops through all the items in the list
            # print(obstacle_list)
            obstacle_rect.x-=obstacle_vel

            # if the obstacle is on the ground, it is a snail, otherwise it is a fly
            if obstacle_rect.bottom == 300: screen.blit(snail_surf,(obstacle_rect.topleft[0]+shake_offset_X,obstacle_rect.topleft[1]+shake_offset_Y))
            else: screen.blit(fly_surf,(obstacle_rect.topleft[0]+shake_offset_X,obstacle_rect.topleft[1]+shake_offset_Y))

        # return each obstacle in the list whose x is greater than -100
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] 

        # return the updated list (with far left obstacles removed)
        return obstacle_list
    
    # if the list is empty, return nothing
    else:
        return []

def player_animation(player_walking):
    # specify as global variables inside the function so that we use the workspace variables
    global player_surf, player_index, player_facing_right, player_hit_timer 

    # Display the jump surface if the player is in the air
    if player_rect.bottom < 298:
        player_surf = pygame.transform.flip(player_jump,not player_facing_right, 0)
    # Play walking animation if the player is on the floor
    else:
        if player_walking == True:
            player_index += 0.1
            if player_index >= len(player_walk): player_index = 0
            player_surf = pygame.transform.flip(player_walk[int(player_index)],not player_facing_right, 0)
        else:
            player_surf = player_stand_surf

# Checks for a collision between the player and the obstacles currently in the game
def check_collisions(obstacle_rect_list,player_rect):
    collision = False
    for obst in obstacle_rect_list:
        if player_rect.colliderect(obst):
            collision = True
            break
    return collision

# reset game objects to initial states
def game_reset():
    global game_active, obstacle_rect_list, obstacle_timer, test_font, player_rect, score, player_vel_y
    global score_text_rect, score_str, score_text_surface, player_health, health_text_surface, obstacle_vel, enable_voldemort
    game_active = True
    obstacle_rect_list.clear()
    player_rect.midbottom = (80,300)
    score = 0
    player_health = 5
    score_text_rect.midbottom = midbottom = (400,50)
    player_vel_y = 0
    # Update Score text
    score_str = 'Score: {}'.format(str(score))
    score_text_surface = test_font.render(score_str,False,'Black')
    # Update Health Text
    player_health_str = 'Health: {}'.format(str(player_health))
    health_text_surface = test_font.render(player_health_str,False,'Black')
    obstacle_vel = 15
    pygame.time.set_timer(obstacle_timer,int(3000*math.exp(-score*0.02)))
    enable_voldemort = False
    
def screen_shake():
    return 2*randint(0,8)-4, 2*randint(0,8)-4


pygame.init()

# Global Variables
score = 0
score_counter = 0
score_str = 'Score: {}'.format(str(score))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FRAMES_PER_SECOND = 60
player_vel_y = 0
GRAVITY = 1 # Gravity in pixels per second squared 
JUMP_VEL = 20
WALK_VEL = 4
game_active = True
SCORE_TEXT_WINDOW_OFFSET_X = 50
SCORE_TEXT_WINDOW_OFFSET_Y = 10
screen_shake_timer = 0
obstacle_vel = 15
enable_voldemort = False
voldemort_thresh = 5

# Player State Variables
player_is_walking = False
player_facing_right = 1
player_is_hit = False
player_is_visible = True
player_health = 5
player_hit_timer = 0
player_hit_timer_s = 0
player_health_str = 'Health: {}'.format(str(player_health))

# Screen shake variables
shake_offset_X = 0
shake_offset_Y = 0

# Game Objects
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # create the game window
pygame.display.set_caption('Ultimate Pygame Tutorial') # set the window caption
clock = pygame.time.Clock() # create a clock object for controlling the framerate

# Create surfaces (Graphics holders) & Create rectangles (Position holders)

# Background Graphics
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha() # convert_alpha speeds up processing time
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Player Graphics

# Import Walk Cycle Frames and store in a list
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 # Index variable for controlling player walk animation
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index] # Put all player animation frames into a list
player_rect = player_surf.get_rect(midbottom = (80,300))

# Test Surface
# test_surface = pygame.Surface((100,200))
# test_surface.fill('Red') # fill the surface with a color

# Enemy Graphics

# Fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_ind = 0
fly_surf = fly_frames[fly_frame_ind]
# fly_rect = fly_surf.get_rect(midbottom = (800,210))

# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_ind = 0
snail_surf = snail_frames[snail_frame_ind]
# snail_rect = snail_surf.get_rect(midbottom = (800,300))

# Initialize List of Enemies
obstacle_rect_list = []

# Create Font Objects and Surfaces
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Score Text
score_text_surface = test_font.render(score_str,False,'Black')
score_text_rect = score_text_surface.get_rect(midbottom = (400,50))

# Health Text
health_text_surface = test_font.render(player_health_str,False,'Black')
health_text_rect = health_text_surface.get_rect(midbottom = (100,50))

# Game Over Text
game_over_text_surface = test_font.render("GAME OVER",False,"Black")
game_over_text_rect = score_text_surface.get_rect(midbottom = (390,100))
restart_instruction_text_surface = test_font.render("Press Enter to Play Again",False,"Black")
restart_instruction_text_rect = restart_instruction_text_surface.get_rect(midbottom = (400, 350))

text_window_rect = score_text_rect.copy()
text_window_rect.width+=SCORE_TEXT_WINDOW_OFFSET_X*2
text_window_rect.height+=SCORE_TEXT_WINDOW_OFFSET_Y*2*.4
text_window_rect.left-=SCORE_TEXT_WINDOW_OFFSET_X
text_window_rect.bottom-=SCORE_TEXT_WINDOW_OFFSET_Y*1.6*.4

# Game Over Player Sprite
player_stand_surf = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_rect = player_stand_surf.get_rect(midbottom = (360,200))

# Create Sounds
bruh_sound = pygame.mixer.Sound('audio/bruh.mp3')
bwah_sound = pygame.mixer.Sound('audio/bwaaah.mp3')
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
voldemort_sound = pygame.mixer.Sound('audio/voldemort.mp3')
hit_sound = pygame.mixer.Sound('audio/Explosion5.wav')
music_sound = pygame.mixer.music.load('audio/music.wav')

# Start the music
pygame.mixer.music.play(-1)

# Adjust SFX Volume
voldemort_sound.set_volume(0.25)
bwah_sound.set_volume(0.5)
jump_sound.set_volume(0.5)
pygame.mixer.music.set_volume(0.25)

# Timers
obstacle_timer = pygame.USEREVENT + 1 # Add a user event
pygame.time.set_timer(obstacle_timer,1500) # Assign a timer to the user event

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,100)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

# Game Loop
while True:

    # ============== Event Loop ====================#
    for event in pygame.event.get():
        # Check for window closing
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Game Playing State
        if game_active:
            # Check for Keyboard Inputs
            if event.type == pygame.KEYDOWN:
                # print('key down')
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom==300:
                        player_vel_y = JUMP_VEL
                        pygame.mixer.Sound.play(jump_sound)
                        # player_index = 0
            
            # Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() # Get current mouse position
                if player_rect.collidepoint(mouse_pos): # Test if mouse is inside player rectangle
                    pygame.mixer.Sound.play(bruh_sound) 

            # Spawn Enemies
            if event.type == obstacle_timer:
                pygame.time.set_timer(obstacle_timer,int(3000*math.exp(-score*0.02)))#int(1500*math.exp(-score*0.009))) # Update the timer duration
                if enable_voldemort: pygame.mixer.Sound.play(voldemort_sound)
                # print(obstacle_timer,int(1500*math.exp(-score*0.009)))
                if randint(0,2): # random integer (either 0 or 1)
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300))) # spwan a snail
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210))) # spwan a fly
                
            # Animate Enemies

            # Fly animation
            if event.type == fly_animation_timer:
                if fly_frame_ind < len(fly_frames)-1: fly_frame_ind += 1
                else: fly_frame_ind = 0

            # Snail animation
            if event.type == snail_animation_timer:
                if snail_frame_ind < len(snail_frames)-1: snail_frame_ind += 1
                else: snail_frame_ind = 0
        
        # Game Over / Title State
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Reset the game
                game_reset()

    if game_active:
        # ============== Update Loop ================= #
        
        # Player Movement
        player_vel_y -= GRAVITY  # Acceleration due to gravity
        player_rect.bottom-=player_vel_y;

        # Resolve player collision with ground
        if player_rect.bottom > 300:
            player_rect.bottom = 300

        # Resolve player collision with screen edges
        if player_rect.left < 0:
            player_rect.left = 0
        elif player_rect.right > SCREEN_WIDTH:
            player_rect.right = SCREEN_WIDTH

        if not player_is_hit:
            if check_collisions(obstacle_rect_list,player_rect):
                # Player Got Hit
                player_is_hit = True
                player_health-=1

                # Update Health Text
                player_health_str = 'Health: {}'.format(str(player_health))
                health_text_surface = test_font.render(player_health_str,False,'Black')

                # Check if player is out of health
                if player_health <= 0:
                    game_active = False
                    pygame.mixer.Sound.play(bruh_sound)
                else:
                    pygame.mixer.Sound.play(bwah_sound)
                    pygame.mixer.Sound.play(hit_sound)
                    # Trigger Player blink and screen shake effects
                    player_hit_timer = 60*3*2
                    screen_shake_timer = 30

        if player_hit_timer > 0:
            player_hit_timer-= 2
            player_hit_timer_s =  float(player_hit_timer/60)
            player_hit_timer_s -= round(player_hit_timer_s)
            player_is_visible = (player_hit_timer_s<0)
        else:
            player_is_hit = False
            player_is_visible = 1

        # User Inputs (handled in update loop)
        # Should use this method for class-specific input handling
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_rect.left-=WALK_VEL 
            player_is_walking = True
            player_facing_right = 0
        if keys[pygame.K_d]:
            player_rect.left+=WALK_VEL
            player_is_walking = True
            player_facing_right = 1
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player_is_walking = False
        
        # Update Score
        score_counter+=1
        if score_counter > FRAMES_PER_SECOND-1:
            score_counter = 0
            score+=1
            score_str = 'Score: {}'.format(str(score))
            score_text_surface = test_font.render(score_str,False,'Black')
            obstacle_vel*=1.01
            if score> voldemort_thresh and enable_voldemort == False:
                enable_voldemort = True

        # Handle Screen Shake
        if screen_shake_timer>0:
            screen_shake_timer-=1
            shake_offset_X, shake_offset_Y = screen_shake()
        else:
            shake_offset_X = shake_offset_Y = 0

        # ============== Draw Loop ======================= #
                
         # screen.blit(test_surface,(0,0)) # BLIT = Block Image Transform (draw a surface onto another surface)
        # Draw background
        screen.blit(sky_surface,(0+shake_offset_X,0+shake_offset_Y))
        screen.blit(ground_surface,(0+shake_offset_X,300+shake_offset_Y))

        # Draw the score text
        # pygame.draw.rect(screen,'Pink',text_window_rect,10) # Draw text box
        pygame.draw.rect(screen,'Pink',text_window_rect)
        screen.blit(score_text_surface,score_text_rect)

        # Draw Health Text
        screen.blit(health_text_surface,health_text_rect)

        # pygame.draw.line(screen,'Blue',(0,0),(SCREEN_WIDTH,SCREEN_HEIGHT))

        # Draw Enemies
        snail_surf = snail_frames[snail_frame_ind]
        # screen.blit(snail_surf,snail_rect)

        fly_surf = fly_frames[fly_frame_ind]
        # screen.blit(fly_surf,fly_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Draw Player
        player_animation(player_is_walking) # update player animation state
        if player_is_visible: screen.blit(player_surf,(player_rect.topleft[0] + shake_offset_X,player_rect.topleft[1] + shake_offset_X))
    else:
        screen.fill('Pink')
        screen.blit(game_over_text_surface,game_over_text_rect)
        score_text_rect.midbottom = midbottom = (400,390)
        screen.blit(score_text_surface,score_text_rect)
        screen.blit(restart_instruction_text_surface,restart_instruction_text_rect)
        screen.blit(pygame.transform.scale(player_stand_surf,(player_stand_rect.width*2,player_stand_rect.height*2)),player_stand_rect)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND) # Restrict game loop to 60 fps (delays the next update call by 1/60s, wraps around SDL_Delay function)