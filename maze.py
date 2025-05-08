import pygame
from pygame import *

# Инициализация Pygame
pygame.init()

# -------- Классы --------

# Класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Класс игрока
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed


# -------- Настройки окна --------
back = (200, 255, 255)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Пинг-Понг")

# -------- Игровые объекты --------
racket1 = Player('rocket.PNG', 30, 200, 5, 25, 100)
racket2 = Player('rocket.PNG', win_width - 55, 200, 5, 25, 100)
ball = GameSprite('ball.png', 325, 225, 4, 50, 50)

# -------- Шрифт и текст --------
font.init()
game_font = font.Font(None, 50)
lose1 = game_font.render('PLAYER 1 LOSE!', True, (255, 0, 0))
lose2 = game_font.render('PLAYER 2 LOSE!', True, (255, 0, 0))

# -------- Игровые переменные --------
clock = time.Clock()
FPS = 60
game = True
finish = False

speed_x = 4
speed_y = 4

# -------- Игровой цикл --------
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)

        # Логика движения
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Столкновения
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        # Отскок от краев
        if ball.rect.top <= 0 or ball.rect.bottom >= win_height:
            speed_y *= -1

        # Условия проигрыша
        if ball.rect.left <= 0:
            finish = True
            window.blit(lose1, (200, 200))
        if ball.rect.right >= win_width:
            finish = True
            window.blit(lose2, (200, 200))

        # Отрисовка
        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)