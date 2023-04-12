from pygame import*
from time import time as count
import json

height = 650
width = 700

mixer.init()
init()

window = display.set_mode((width, height))
display.set_caption('Arcade Burst Demo: Ping Pong - 2 Players')
display.set_icon(image.load('images/ball.png'))

fps = time.Clock()

bg = transform.scale(image.load('images/bg.png'), (700, 650))
hit = mixer.Sound('sounds/hit.wav')
lose = mixer.Sound('sounds/lose.ogg')
victory = mixer.Sound('sounds/win.wav')
hit.set_volume(0.5)
lose.set_volume(0.5)
victory.set_volume(0.5)

mixer.music.load('music/ping_music.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(loops=-1)

p1_score = 0
p2_score = 0
speed_x = 5
speed_y = 5
game_over = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.cooldown = 1
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
    def LEFT(self):
        self.rect.x -= 3
        
    def RIGHT(self):
        self.rect.x += 3
            
class Player1(GameSprite):
    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if pressed_keys[K_d] and self.rect.x + self.rect.width <= 700:
            self.rect.x += self.speed

class Player2(GameSprite):
    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT] and self.rect.x + self.rect.width <= 700:
            self.rect.x += self.speed
            
class Ball(GameSprite):
    def update(self):
        self.rect.x += speed_x
        self.rect.y += speed_y
        global p1_score, p2_score
        if self.rect.y > 800:
            self.rect.x = 350
            self.rect.y = 300
            p2_score = p2_score + 1
            lose.play()
            
        if self.rect.y < -100:
            self.rect.x = 350
            self.rect.y = 300
            p1_score = p1_score + 1
            lose.play()
    
    def collide(self, obj):
        if count() - self.cooldown < 0.5:
            return False
        res = self.rect.colliderect(obj.rect)
        if res:
            self.cooldown = count()
        return res
    
        
def set_count():
    global p1_score, p2_score                   
    p1_count = font.SysFont('Consolas', 20).render('Score: ' + str(p1_score), True, (241, 114, 252))
    p2_count = font.SysFont('Consolas', 20).render('Score: ' + str(p2_score), True, (239, 255, 64))
    fps_count = font.SysFont('Consolas', 15).render('FPS: ' + str(int(fps.get_fps())), True, (250, 250, 250))
    window.blit(p1_count, (5, 25))
    window.blit(p2_count, (5, 45))
    window.blit(fps_count, (5, 5))
        
def win():
        global speed_x, speed_y, game_over
        if p1_score == 10:
            window.blit(bg, (0, 0))
            window.blit(p1_win, (280, 280))
            window.blit(pls_quit, (150, 320))
            speed_x = 0
            speed_y = 0
            victory.play()
            mixer.music.set_volume(0.1)
            win_txt = open('data/result.txt', 'w+')
            win_txt.write('Result: P1 win'+'\nP1 Score: '+str(p1_score)+'\nP2 Score: '+str(p2_score))
        if p2_score == 10:
            window.blit(bg, (0, 0))
            window.blit(p2_win, (280, 280))
            window.blit(pls_quit, (150, 320))
            speed_x = 0
            speed_y = 0
            victory.play()
            mixer.music.set_volume(0.1)
            win_txt = open('data/result.txt', 'w+')
            win_txt.write('Result: P2 win'+'\nP1 Score: '+str(p1_score)+'\nP2 Score: '+str(p2_score))

p1 = Player1('images/player1_platform.png', 280, 590, (150, 50), 6)
p2 = Player2('images/player2_platform.png', 280, 10, (150, 50), 6)
ball = Ball('images/ball.png', 350, 300, (50, 50), 1)

p1_win = font.SysFont('Times New Roman', 35).render('P1 WIN!!!', True, (241, 241, 241))
p2_win = font.SysFont('Times New Roman', 35).render('P2 WIN!!!', True, (241, 241, 241))
pls_quit = font.SysFont('Times New Roman', 25).render('Please, quit for game. After restart the game', True, (241, 241, 241))
save = font.SysFont('Times New Roman', 25).render('*data saved*', True, (241, 241, 241))

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
    if not game_over:
    
        if ball.rect.x > width-50 or ball.rect.x < 0:
            speed_x *= -1
            hit.play()
       
        if ball.collide(p1):
            speed_y *= -1   
            hit.play()
        if ball.collide(p2):
            speed_y *= -1
            hit.play()
        
        p1.update() 
        p2.update()
        ball.update()
        window.blit(bg, (0, 0))
        p1.draw()
        p2.draw()
        ball.draw()
        set_count()
    
        if p1_score == 10 or p2_score == 10:
            game_over = True
            win()

    fps.tick(60)
    display.update()

start_time = count()

while game and count() - start_time < 5:
    for e in event.get():
        if e.type == QUIT:
            game = False
game = False