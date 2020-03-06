#inizializzazione
import pygame
from random import randint as rand
pygame.init()
#creazione schermo
screen = pygame.display.set_mode((731, 487))
pygame.display.set_caption("Save Di Leo From COVID19")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
bg = pygame.image.load("bg1.jpg")
myfont = pygame.font.SysFont('Comic Sans MS', 20)
game_over_screen = myfont.render('GAME OVER', False, (255, 0, 0))
#inizializzazione regole
score = 0
difficulty = 1




#caricamento immagini oggetti
virus_img = pygame.image.load("virus.png")
syringe_img = pygame.image.load("syringe.png")
player_img = pygame.image.load("player.png")
#classe giocatore
class player_character(object):
    def __init__(self, initial_x, initial_y, vel):
        self.x = initial_x
        self.y = initial_y
        self.vel = vel
        self.right = False
        self.left = False
    def draw(self):
        screen.blit(player_img, (self.x, self.y))
    def movement(self):
        if self.right and self.x < 731 - 64 - self.vel:
            self.x += self.vel
        if self.left and self.x > 0 + self.vel:
            self.x -= self.vel
#classe siringhe (proiettili)
class syringe(object):
    def __init__(self, vel, initial_x, initial_y):
        self.fire = False
        self.vel = vel
        self.x = initial_x
        self.y = initial_y

    def movement(self, p_x, p_y):
        if not self.fire:
            self.x = p_x
            self.y = p_y
        else:
            self.y -= self.vel
            if self.y <= 0:
                self.fire = False
    def draw(self):
        screen.blit(syringe_img, (self.x, self.y))
#classe virus
class virus(object):
    def __init__(self, vel):
        self.vel = vel
        self.army_x = []
        self.army_y = []
    def recruit(self, dif):
        while len(self.army_y) < dif*2:
            x = rand(31, 680)
            y = rand(31, 64)
            self.army_x.append(x)
            self.army_y.append(y)
    def draw(self):
        for i in range(len(self.army_y)):
            screen.blit(virus_img, (self.army_x[i], self.army_y[i]))
    def movement(self, y):
        for i in range(len(self.army_y)):
                self.army_y[i] += self.vel


def difficulty_set(s):
    if score < 10:
        return 1
    else:
        return int((score / 10) + 1)



#creazione oggetti
player_1 = player_character(365, 410, 4)
projectile = syringe(6, 365, 410)
covid_19 = virus(0.25)
covid_19.recruit(difficulty)    #il numero di virus aumenta all'aumentare della difficolta che aumenta all'aumentare dei punti (score)
#funzione di "animazione"
def draw():
    screen.blit(bg, (0, 0))
    score_text = myfont.render(f'SCORE : {score}', False, (0, 255, 0))
    screen.blit(score_text, (0, 0))
    if not game_over:
        projectile.draw()
        player_1.draw()
        covid_19.draw()
    else:
        screen.blit(game_over_screen, (340, 205))

#L00P
run = True
game_over = False
while run:
    screen.fill((0, 0, 0))
    #comandi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_1.right = True
                player_1.left = False
            if event.key == pygame.K_LEFT:
                player_1.left = True
                player_1.right = False
            if event.key == pygame.K_SPACE:
                projectile.fire = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_1.right = False
            if event.key == pygame.K_LEFT:
                player_1.left = False


    #movimenti
    player_1.movement()
    projectile.movement(player_1.x, player_1.y)
    covid_19.movement(player_1.y)
    draw()
    for i in range(len(covid_19.army_y)):
        if (projectile.y - 16 < covid_19.army_y[i] + 16 and projectile.y -16 > covid_19.army_y[i] - 16) and (projectile.x > covid_19.army_x[i] - 16 and projectile.x < covid_19.army_x[i] + 16):
            score += 1
            projectile.fire = False
            covid_19.army_x.remove(covid_19.army_x[i])
            covid_19.army_y.remove(covid_19.army_y[i])
            covid_19.recruit(difficulty)
        if covid_19.army_y[i] >= player_1.y:
            game_over = True
    difficulty = difficulty_set(score)


    pygame.display.update()
