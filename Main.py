import random
import math
from pygame import Rect
import sys
from pgzero.actor import Actor

WIDTH = 1360
HEIGHT = 728


current_screen = "menu"
sound_on = True

ground_y = HEIGHT - (HEIGHT * 0.2)  


alien = Actor("alien")
alien.x = 100
alien.bottom = ground_y



button_width = 200
button_height = 50
button_x = (WIDTH - button_width) // 2
button_y_start = 180  


volume_level = 0.5  


volume_button = Rect((button_x, button_y_start + 240), (button_width, button_height))  

start_button = Rect((button_x, button_y_start), (button_width, button_height))
sound_button = Rect((button_x, button_y_start + 80), (button_width, button_height))
exit_button = Rect((button_x, button_y_start + 160), (button_width, button_height))


walk_right_images = ["alien_walk1", "alien_walk2"]
walk_left_images = ["alien_walk3", "alien_walk4"]
walk_index = 0
walk_timer = 0


is_jumping = False
velocity_y = 0
gravity = 0.5
ground_y = 500


is_crouching = False


facing_right = True

game_music = sounds.load("gameplay")
game_music_playing = False  

vida = 3
vida_max = 3
invulneravel = False
invuln_timer = 0



tile_width = Actor("terrain_grass_block_top").width
water_tile_width = Actor("water_top").width
print("tile_width:", tile_width)
print("water_tile_width:", water_tile_width)

tile_width = Actor("terrain_grass_block_top").width
agua_width = tile_width * 2
agua_x = tile_width * 3    

agua_rect = Rect((agua_x, ground_y), (tile_width * 2, HEIGHT - ground_y))


fish = Actor("fish_purple_down")
fish.base_x = agua_rect.left + agua_rect.width // 2
fish.base_y = agua_rect.top + 60
fish.x = fish.base_x
fish.y = fish.base_y
fish.direction = "up"
fish_timer = 0
fish_cooldown = 300  
fish_animation_step = 0
fish.visible = True


frog = Actor("frog_idle_2")  
frog.x = WIDTH - 100        
frog.bottom = ground_y
frog.direction = "left"
frog.jump_timer = 60
frog.is_jumping = False
frog.velocity_y = 0
frog.scale = 0.7  

button_y_game_over_start = HEIGHT // 2 - 100 
retry_button = Rect((button_x, button_y_game_over_start + 60), (button_width, button_height)) 
menu_button = Rect((button_x, button_y_game_over_start + 180), (button_width, button_height))  

def draw():
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "game_over":
        draw_game_over()
    else:
        draw_background()
        alien.draw()
        draw_ground()
        draw_hearts()
        draw_water()

        if fish.visible:
            fish.draw()
        if frog:
            frog.draw()

    


def draw_menu():
    screen.fill((100, 150, 200))
    screen.draw.text("Plataform Hero Game", center=(WIDTH//2, 100), fontsize=50, color="white")

    screen.draw.filled_rect(start_button, (0, 100, 200))
    screen.draw.text("Comecar o Jogo", center=start_button.center, fontsize=30, color="white")

    screen.draw.filled_rect(sound_button, (0, 150, 100))
    sound_text = "Som: Ligado" if sound_on else "Som: Desligado"
    screen.draw.text(sound_text, center=sound_button.center, fontsize=30, color="white")

    screen.draw.filled_rect(exit_button, (150, 0, 0))
    screen.draw.text("Sair", center=exit_button.center, fontsize=30, color="white")


    screen.draw.filled_rect(volume_button, (100, 100, 200))
    screen.draw.text(f"Volume: {int(volume_level * 100)}%", center=volume_button.center, fontsize=30, color="white")

  
def draw_game_over():
    screen.fill((0, 0, 0))  
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 3), fontsize=50, color="white")
    
    screen.draw.filled_rect(retry_button, (0, 200, 0))
    screen.draw.text("Tentar Novamente", center=retry_button.center, fontsize=30, color="white")
    
    screen.draw.filled_rect(menu_button, (200, 0, 0))
    screen.draw.text("Voltar ao Menu", center=menu_button.center, fontsize=30, color="white")

def draw_hearts():
    spacing = 5
    heart_width = 70  
    x_start = WIDTH - (heart_width * 3 + spacing * 2) - 10
    y = 10

    for i in range(3):
        x = x_start + i * (heart_width + spacing)

        if vida >= i + 1:
            screen.blit("hud_heart", (x, y))
        elif vida >= i + 0.5:
            screen.blit("hud_heart_half", (x, y))
        else:
            screen.blit("hud_heart_empty", (x, y))

def draw_background():
    tile_width = 512
    tile_height = 512

  
    num_tiles_x = math.ceil(WIDTH / tile_width)

  
    for i in range(num_tiles_x):
        x = i * tile_width
        screen.blit("background_clouds", (x, 0)) 


    for i in range(num_tiles_x):
        x = i * tile_width
        screen.blit("background_solid_sky", (x, tile_height)) 

def draw_ground():
    tile_top_left = Actor("terrain_grass_block_top_left")
    tile_top = Actor("terrain_grass_block_top")
    tile_top_right = Actor("terrain_grass_block_top_right")

    tile_left = Actor("terrain_grass_block_left")
    tile_center = Actor("terrain_grass_block_center")
    tile_right = Actor("terrain_grass_block_right")

    tile_width = tile_top.width
    tile_height = tile_top.height

    ground_start_y = ground_y

    rows = math.ceil((HEIGHT - ground_start_y) / tile_height)
    cols = math.ceil(WIDTH / tile_width)

    for row in range(rows):
        y = ground_start_y + row * tile_height
        for col in range(cols):
            x = col * tile_width

           
            tile_rect = Rect((x, y), (tile_width, tile_height))
            if tile_rect.colliderect(agua_rect):
                continue  
          
            if row == 0: 
                if agua_rect.left - tile_width < x < agua_rect.left + tile_width:
                    sprite = tile_top_right  
                elif agua_rect.right - tile_width <= x <= agua_rect.right:
                    sprite = tile_top_left   
                elif col == 0:
                    sprite = tile_top_left
                elif col == cols - 1:
                    sprite = tile_top_right
                else:
                    sprite = tile_top
            else:  
                if agua_rect.left - tile_width < x < agua_rect.left + tile_width:
                    sprite = tile_right
                elif agua_rect.right - tile_width <= x <= agua_rect.right:
                    sprite = tile_left
                elif col == 0:
                    sprite = tile_left
                elif col == cols - 1:
                    sprite = tile_right
                else:
                    sprite = tile_center

            sprite.pos = (x + tile_width / 2, y + tile_height / 2)
            sprite.draw()

def draw_water():
    tile_top = Actor("water_top")
    tile_fill = Actor("water")
    tile_width = tile_top.width
    tile_height = tile_top.height

    cols = math.ceil(agua_rect.width / tile_width)
    rows = math.ceil(agua_rect.height / tile_height)

    for col in range(cols):
        x = agua_rect.left + col * tile_width + tile_width // 2

    
        tile_top.pos = (x, agua_rect.top + tile_height // 2)
        tile_top.draw()

        
        for row in range(1, rows):
            y = agua_rect.top + row * tile_height + tile_height // 2
            tile_fill.pos = (x, y)
            tile_fill.draw()

def check_game_over():
    global current_screen

    if vida <= 0:
        current_screen = "game_over" 

def update():
    if current_screen == "jogo":
        update_game()
        check_game_over()
        play_game_music() 
    elif current_screen == "menu":
        stop_music() 


def play_game_music():
    global game_music_playing

    if not game_music_playing:
        game_music.play(loops=-1)  
        game_music.set_volume(volume_level)  
        game_music_playing = True  


def stop_music():
    global game_music_playing
    game_music.stop()  
    game_music_playing = False  


def update_game():
    global walk_index, walk_timer, is_jumping, velocity_y, is_crouching, facing_right
    global vida, invulneravel, invuln_timer
    global fish_timer

    
    if invulneravel:
        invuln_timer -= 1
        if invuln_timer <= 0:
            invulneravel = False
    
    moving = False

   
    if keyboard.s and not is_jumping:
        is_crouching = True
        if facing_right:
            alien.image = "alien_crouch"
        else:
            alien.image = "alien_crouch2"
    else:
        is_crouching = False

  
    if keyboard.a:
        alien.x -= 6
        if facing_right and is_jumping:
            alien.image = "alien_jump2"
        facing_right = False
        moving = True

    
    elif keyboard.d:
        alien.x += 6
        if not facing_right and is_jumping:
            alien.image = "alien_jump"
        facing_right = True
        moving = True

   
    if keyboard.space and not is_jumping and not is_crouching:
        velocity_y = -14
        is_jumping = True
        if facing_right:
            alien.image = "alien_jump"
        else:
            alien.image = "alien_jump2"

        if sound_on:
            sounds.sfx_jump.play()

   
    if moving and not is_jumping and not is_crouching:
        walk_timer += 1
        if walk_timer % 10 == 0:
            walk_index = (walk_index + 1) % 2
        if facing_right:
            alien.image = walk_right_images[walk_index]
        else:
            alien.image = walk_left_images[walk_index]
    elif not is_jumping and not is_crouching and not moving:
        alien.image = "alien"

    
    velocity_y += gravity
    if velocity_y > 10:
        velocity_y = 10

    alien.y += velocity_y

    if alien.bottom >= ground_y:
       
        if alien.colliderect(agua_rect):
            pass  
        else:
            alien.bottom = ground_y
            velocity_y = 0
            is_jumping = False
        


    
    if alien.left < 0:
        alien.left = 0
    if alien.right > WIDTH:
        alien.right = WIDTH

   
    if alien.colliderect(agua_rect) and alien.y > agua_rect.top + 30 and not invulneravel:
        vida -= 1
        alien.x = 100
        alien.bottom = ground_y
        velocity_y = 0
        is_jumping = False
        alien.image = "alien"
        invulneravel = True
        invuln_timer = 60  

        if sound_on:
            sounds.sfx_hurt.play()
    
    update_fish()
    update_frog()

def update_fish():
    global fish_timer, fish_animation_step, vida, invulneravel, invuln_timer

    if fish_timer <= 0:
        
        if fish.direction == "up":
            fish.y -= 10
            fish.image = "fish_purple_up"
            if fish.y < agua_rect.top - 250:
                fish.direction = "down"
        else:
            fish.y += 4
            fish.image = "fish_purple_down"
            if fish.y >= fish.base_y:
                fish.y = fish.base_y
                fish_timer = fish_cooldown
                fish.direction = "up"
                fish.visible = False  
    else:
        fish_timer -= 1
        if fish_timer == 0:
            fish.visible = True  

   
    if fish.visible and fish.colliderect(alien) and not invulneravel:
        vida -= 0.5
        invulneravel = True
        invuln_timer = 60
        alien.image = "alien_purple_hit"
       
        if alien.x < fish.x:
            alien.x -= 40
        else:
            alien.x += 40
        if sound_on:
            sounds.sfx_hurt.play()
    
def update_frog():
    global vida, invulneravel, invuln_timer

    if frog.jump_timer > 0:
        frog.jump_timer -= 1
    else:
        if not frog.is_jumping:
            frog.velocity_y = -10  
            frog.is_jumping = True
            frog.jump_timer = 30   
            if frog.direction == "left":
                frog.image = "frog_jump"
            else:
                frog.image = "frog_jump_2"

    
    if frog.is_jumping:
        if frog.direction == "left":
            frog.x -= 3
        else:
            frog.x += 3

  
    frog.velocity_y += gravity
    frog.y += frog.velocity_y

    if frog.y >= ground_y:
        frog.bottom = ground_y
        frog.velocity_y = 0
        frog.is_jumping = False
        if frog.direction == "left":
            frog.image = "frog_idle"
        else:
            frog.image = "frog_idle_2"

   
    borda_agua_esquerda = agua_rect.left
    borda_agua_direita = agua_rect.right

    if frog.direction == "left" and frog.x < borda_agua_esquerda + 20:
        frog.direction = "right"
        frog.image = "frog_idle_2"
    elif frog.direction == "right" and frog.right > WIDTH - 50:
        frog.direction = "left"
        frog.image = "frog_idle"

    
    margin_x = 10
    margin_y = 10
    frog_hitbox = Rect(
    frog.left + margin_x,
    frog.top  + margin_y,
    frog.width  - 2 * margin_x,
    frog.height - 2 * margin_y
    )

    alien_hitbox = Rect(alien.left, alien.top, alien.width, alien.height)
    if frog_hitbox.colliderect(alien_hitbox) and not invulneravel:
        vida -= 1
        invulneravel = True
        invuln_timer = 60
        alien.image = "alien_purple_hit"
        if alien.x < frog.x:
            alien.x -= 40
        else:
            alien.x += 40
        if sound_on:
            sounds.sfx_hurt.play()



def on_mouse_down(pos):
    global current_screen, sound_on, volume_level, vida

    if current_screen == "menu":
        if start_button.collidepoint(pos):
            if sound_on:
                sounds.sfx_select.play()
            current_screen = "jogo"
            vida = vida_max  
        elif sound_button.collidepoint(pos):
            if sound_on:
                sounds.sfx_select.play()
            sound_on = not sound_on
        elif exit_button.collidepoint(pos):
            if sound_on:
                sounds.sfx_select.play()
            sys.exit()
        elif volume_button.collidepoint(pos):  
            volume_level += 0.1
            if volume_level > 1: 
                volume_level = 0
            game_music.set_volume(volume_level) 
    if current_screen == "game_over":
        if retry_button.collidepoint(pos):
            current_screen = "jogo"
            vida = vida_max  
        elif menu_button.collidepoint(pos):
            current_screen = "menu"
            vida = vida_max  
