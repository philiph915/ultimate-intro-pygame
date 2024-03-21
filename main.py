import pygame
from sys import exit
from random import randint, choice # Functions to generate random integers and randomly choose from a list
import math

class Player(pygame.sprite.Sprite): # Player Class inherits from Sprite Class
    def __init__(self): # Constructor method: Sets class properties
        super().__init__() # this line calls the parent class constructor

        # Initialize Class Properties (self.image and self.rect are required for sprite class)

        # Get Required Global Variables
        global GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH

        # Player Graphics
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_stand  = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 # Index variable for controlling player walk animation
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        # Player Properties
        self.walk_vel = 4
        self.is_walking = False
        self.is_facing_right = 1
        self.jump_vel = 20
        self.vel_y = 0

        # Sounds
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

        # Sprite Object Properties
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))

    def update(self):
        self.player_input()
        self.player_movement()
        self.animation_state()

    def player_movement(self):
        # Apply Gravitational Acceleration
        self.vel_y -= GRAVITY
        self.rect.y -= self.vel_y

        # Resolve player collision with ground
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

        # Resolve player collision with screen edges
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def player_input(self):
        keys = pygame.key.get_pressed()
        # Jumping
        if keys[pygame.K_SPACE]:
            if self.rect.bottom==300:
                self.vel_y = self.jump_vel
                self.jump_sound.play()
        # Walking
        if keys[pygame.K_a]:
            self.is_walking = True
            self.is_facing_right = 0
            self.rect.left-=self.walk_vel 
        if keys[pygame.K_d]:
            self.is_walking = True
            self.is_facing_right = 1
            self.rect.left+=self.walk_vel 
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.is_walking = False

    def animation_state(self):
        # Display the jump surface if the player is in the air
        if self.rect.bottom < 298:
            self.image = pygame.transform.flip(self.player_jump,not self.is_facing_right, 0)
        
        else: # Play walking animation if the player is on the floor
            if self.is_walking == True:
                self.player_index += 0.1
                if self.player_index >= len(self.player_walk): self.player_index = 0
                self.image = pygame.transform.flip(self.player_walk[int(self.player_index)],not self.is_facing_right, 0)
            else:
                self.image = self.player_stand

class Obstacle(pygame.sprite.Sprite): # Obstacles
    def __init__(self, type, obstacle_vel): # include an input to the constructor (type = what type of enemies is this)
        super().__init__()
        if type == 'fly': # "type" is a local variable to this function and not a class property
            frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            y_pos = 210
        else:
            frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            y_pos = 300

        # Class properties
        self.frames = [frame1,frame2] # create a list of images representing the object's animation frames
        self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),y_pos))
        self.vel_x = obstacle_vel

    def animation_state(self):
        self.animation_index+=0.1
        if self.animation_index>=len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def check_destroy(self):
        if self.rect.right < 0: self.kill()

    def update(self):
        self.animation_state()
        self.rect.x-= self.vel_x
        self.check_destroy()

# reset game objects to initial states
def game_reset():
    global game_active, obstacle_timer, test_font, score, player_vel_y
    global score_text_rect, score_str, score_text_surface, player_health, health_text_surface, obstacle_vel, enable_voldemort
    game_active = True
    player.sprite.rect.midbottom = (80,300)
    score = 0
    player_health = 5
    score_text_rect.midbottom = midbottom = (400,50)
    player.sprite.vel_y = 0
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

def obstacle_collisions():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): # Returns list of collisions between a sprite and a sprite group
        collision = True
    else:
        collision = False
    return collision

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
# JUMP_VEL = 20
# WALK_VEL = 4
game_active = True
SCORE_TEXT_WINDOW_OFFSET_X = 50
SCORE_TEXT_WINDOW_OFFSET_Y = 10
screen_shake_timer = 0
obstacle_vel = 15
enable_voldemort = False
voldemort_thresh = 5

# Player Game Variables
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

# Create a GroupSingle (sprite group with one sprite)
player = pygame.sprite.GroupSingle()
player.add(Player()) # Add the player sprite object to the GroupSingle

# Create a Group for obstacles
obstacle_group = pygame.sprite.Group()

# Create surfaces (Graphics holders) & Create rectangles (Position holders)

# Background Graphics
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha() # convert_alpha speeds up processing time
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

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
            # Spawn Enemies
            if event.type == obstacle_timer:
                pygame.time.set_timer(obstacle_timer,int(3000*math.exp(-score*0.02))) # Update the timer duration
                if enable_voldemort: pygame.mixer.Sound.play(voldemort_sound)
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail']),obstacle_vel))
        
        # Game Over / Title State
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Reset the game
                game_reset()

    if game_active:
        # ============== Update Loop ================= #
        player.update()
        obstacle_group.update()

        if not player_is_hit:
            if obstacle_collisions():#(player,obstacle_group):
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
                    obstacle_group.empty() # deletes everything in the obstacle group
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
        pygame.draw.rect(screen,'Pink',text_window_rect)
        screen.blit(score_text_surface,score_text_rect)

        # Draw Health Text
        screen.blit(health_text_surface,health_text_rect)

        if player_is_visible: player.draw(screen)
        obstacle_group.draw(screen)
    else:
        screen.fill('Pink')
        screen.blit(game_over_text_surface,game_over_text_rect)
        score_text_rect.midbottom = midbottom = (400,390)
        screen.blit(score_text_surface,score_text_rect)
        screen.blit(restart_instruction_text_surface,restart_instruction_text_rect)
        screen.blit(pygame.transform.scale(player_stand_surf,(player_stand_rect.width*2,player_stand_rect.height*2)),player_stand_rect)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND) # Restrict game loop to 60 fps (delays the next update call by 1/60s, wraps around SDL_Delay function)