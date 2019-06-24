import pgzrun
import os
import random
import time
import datetime
import ctypes

user32 = ctypes.windll.user32
WIDTH =  user32.GetSystemMetrics(0)  # nech sa rozhodnut
HEIGHT = user32.GetSystemMetrics(1)  # nech sa rozhodnut

alien = Actor('alien')
fireball = Actor('fireball') # Nechaj ich si vybrat
alien.topright = round(WIDTH/2), round(HEIGHT/2)
background = Actor('background')

player_name = ''
cas_hry = 30 # nechaj ich si vybrat
score = 0
direction = 0
change_dir_count = 0
change_dan_count = 0
is_alien_danger = False
is_alien_hurt = False
is_fireball_active = False

def draw():
    screen.clear()
    background.draw()
    alien.draw()
    if (is_fireball_active):
        fireball.draw()
    zostavajuci_cas = cas_hry - round(time.clock() - time_counter)
    screen.draw.text("Skóre: "+str(score),(10,10),color="white")
    screen.draw.text("Hráč: "+player_name,(10,30),color="white")             # nechaj ich spravit
    screen.draw.text("Zostava: "+str(zostavajuci_cas),(90,10),color="white") # nechaj ich spravit

def update():
    global direction
    rand_change()
    decide_to_change()
    if direction == 0:
        alien.left += 2
        if alien.left > WIDTH:
            pick_direction()
            set_alien_to_proper_start()
    if direction == 1:
        alien.left -= 2
        if alien.right < 0:
            pick_direction()
            set_alien_to_proper_start()
    if direction == 2:
        alien.top += 2
        if alien.top > HEIGHT:
            pick_direction()
            set_alien_to_proper_start()
    if direction == 3:
        alien.top -= 2
        if alien.bottom < 0:
            pick_direction() 
            set_alien_to_proper_start()

def decide_to_change():
    global change_dan_count
    global is_alien_danger
    global is_alien_hurt
    global is_fireball_active
    if (is_alien_hurt):
        return
    if (not is_alien_danger):
        if (change_dan_count < 120):
            change_dan_count += 1
            return
        alien.image = 'alien_danger'
        is_alien_danger = True
        change_dan_count = random.randint(50,90)
        if (not is_fireball_active):
            is_fireball_active = True
            fireball.top = alien.top
            fireball.right = alien.right
            fireball.draw()
        return
    if (change_dan_count > 0):
        change_dan_count -= 1
        return
    is_alien_danger = False
    alien.image = 'alien'
    
def on_mouse_move(pos):
    global is_fireball_active
    if (not is_fireball_active):
        return
    if ((fireball.right - fireball.width/2 - pos[0])<0):
        fireball.right = fireball.right + 1
    elif ((fireball.right + fireball.width/2 - pos[0])>0):
        fireball.right = fireball.right - 1
    if (fireball.top + fireball.height/2 - pos[1]>0):
        fireball.top = fireball.top - 1
    elif (fireball.top + fireball.height/2 -pos[1]<0):
        fireball.top = fireball.top + 1
    if (fireball.collidepoint(pos)):
        miss(1)
        is_fireball_active = False

def rand_change():
    global change_dir_count
    if (change_dir_count < 50):
        change_dir_count += 1
        return
    pick_direction()
    change_dir_count = 0
            
def pick_direction():
    global direction
    direction = random.randint(0,3)

def set_alien_to_proper_start():
    global direction
    if direction == 0:
        alien.right = 0
        alien.top = random.randint(1,HEIGHT - alien.height)
    if direction == 1:
        alien.left = WIDTH
        alien.top = random.randint(1,HEIGHT - alien.height)
    if direction == 2:
        alien.bottom = 0
        alien.left = random.randint(1,WIDTH - alien.width)
    if direction == 3:
        alien.top = HEIGHT
        alien.left = random.randint(1,WIDTH - alien.width)

        
def on_mouse_down(pos):
    global is_alien_hurt
    global is_alien_danger
    if alien.collidepoint(pos):
        if ((not is_alien_hurt) and (not is_alien_danger)):
            set_alien_hurt()
            apply_score()
        elif (is_alien_danger):
            miss(2)
    else:
        miss(1)

def set_alien_hurt():
    global is_alien_hurt
    is_alien_hurt = True
    alien.image = 'alien_hurt'
    sounds.eep.play()
    clock.schedule_unique(set_alien_normal, 1.0)
    
def set_alien_normal():
    global is_alien_hurt
    alien.image = 'alien'
    is_alien_hurt = False
    
def miss(points):
    global score
    score -= points
    if score < 0:
        score = 0

def apply_score():
    global score
    score += 1

def load_player():
    global player_name
    while (len(player_name)<3 or len(player_name)>11):
        print('Zadaj svoje meno (3 az 10 znakov):') # nechaj ich spravit
        player_name = input()

def end_game():
    music.fadeout(3)
    print('********************************')
    print("Hrac " + player_name + " ziskal skore: " + str(score))
    print('********************************')
    f = open("skore.txt", "a")
    x = str(datetime.datetime.now())
    f.write("Meno: %-10s | Skore: %-2s | Datum: %-16s\n" % (player_name,score,x[:len(x)-10]))
    input("Stkac ENTER pre ukoncenie hry...")
    exit()

load_player()
music.play('song')    # nechaj ich spravit
music.set_volume(0.3) # nechaj ich spravit
clock.schedule_unique(end_game, cas_hry)
time_counter = time.clock()
pgzrun.go()
