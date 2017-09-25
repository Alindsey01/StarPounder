#musical credit link: https://opengameart.org/content/evolutius-music

# Shmup game
import pygame
import random
from os import path

img_dir =  path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

#diminsional vars
WIDTH = 480
HEIGHT = 600
FPS = 60
POWER_TIME = 5000

#colors and graphics etc------------
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow =(255, 255, 0)
lime = (0, 255, 64)


#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Star Pounder: A Rough Ride")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = ( x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def newenemy():
    e = Craft()
    all_sprites.add(e)
    crafts.add(e)

def checkshield(level):
    if level <= 0:
            player_die_sound.play()
            player_die_scream.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
            return death_explosion

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    #draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    title_rect = title_img.get_rect()
    title_rect.centerx = WIDTH / 2
    title_rect.centery = 125
    screen.blit(title_img, title_rect)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH /2, HEIGHT /2, lime)
    draw_text(screen, "Press a key to begin", 18, WIDTH /2, HEIGHT * 3 /4, lime)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        #timeout for powerups
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWER_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            #motivate_eastwood[player.lives -1].play() add when game over screen is made
            random.choice(motivate_eastwood).play()
            
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
                
    def hide(self):
        #hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * .9) / 2)
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            #below code fixes jitter in rotation
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT +10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Craft(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemy_images) #change image make list below
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * .9) / 2)
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 5)
        
        
    def update(self):
        self.rect.y += self.speedy
        #figure out sine wave movement
        if self.rect.top > HEIGHT +10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (5,29))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        #kill if goes off screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4
    def update(self):
        self.rect.y += self.speedy
        #kill if goes off screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 65

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
#load all game graphx
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
title_img = pygame.image.load(path.join(img_dir, 'title_text.png'))
title_img.set_colorkey(black)
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25,19))
player_mini_img.set_colorkey(black)
laser_img = pygame.image.load(path.join(img_dir, "laserGreen03.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
                'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

enemy_images = []
enemy_list = ['enemyRed1.png', 'enemyRed2.png', 'enemyRed3.png']
for img in enemy_list:
    enemy_img = pygame.image.load(path.join(img_dir, img)).convert()
    enemy_img_new = pygame.transform.scale(enemy_img, (40,25))
    enemy_img_new.set_colorkey(black)
    enemy_images.append(enemy_img_new)
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    explosion_anim['player'].append(img)	
	
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()	

#load all the game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
shoot_sound.set_volume(.5)
expl_sounds = []
for snd in ['Explosion_1.wav', 'Explosion_2.wav']:
    i = 0
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    expl_sounds[i].set_volume(.2)
    i = i + 1
motivate_eastwood = []
for snd in ['dyin_livin.wav', 'agreeable.wav', 'dixie.wav']:
    motivate_eastwood.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
player_die_scream = pygame.mixer.Sound(path.join(snd_dir, 'WilhelmScream.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'gain_shield.wav'))
bolt_sound = pygame.mixer.Sound(path.join(snd_dir, 'doublegun_pup.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'BGM.ogg'))
pygame.mixer.music.set_volume(0.4)


#plays the music in game
pygame.mixer.music.play(loops=-1)

#-----------Game Loop----------------
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        #all the sprite groups
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        crafts = pygame.sprite.Group()
        player = Player()
        
        all_sprites.add(player)
        for i in range(8):
            newmob()
        for i in range(3):
            newenemy()
                        
        #add score
        score = 0
    #keep running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        #check window closed
        if event.type == pygame.QUIT:
            running = False
        
    # Update
    all_sprites.update()
    # check if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius  #calc score given object radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow1 = Pow(hit.rect.center)
            all_sprites.add(pow1)
            powerups.add(pow1)
            
        newmob()

     # check if a bullet hit a craft
    hits = pygame.sprite.groupcollide(crafts, bullets, True, True)
    for hit in hits:
        score += 50   #calc score given object radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow1 = Pow(hit.rect.center)
            all_sprites.add(pow1)
            powerups.add(pow1)
            
        newenemy()   
        
    #check to see if a mob or craft hits the player adjust shield
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        death_explosion = checkshield(player.shield)

    hits = pygame.sprite.spritecollide(player, crafts, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newenemy()
        death_explosion = checkshield(player.shield)
	    
    #if we hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 20
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            bolt_sound.play()
	
	#if the player has died and the explosion is finished then end game
    if player.lives == 0 and not death_explosion.alive():
        game_over = True
	
        
    # Draw / render
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10, white)
    draw_shield_bar(screen,5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    
    #always after drawing all elements
    pygame.display.flip()

pygame.quit()
