import pygame
import sys
import sound
import settings
import random
from enemies import initialize_enemies, draw_enemies, update_enemies, check_bullet_collision

pygame.init()

sound.start_music()

WIDTH, HEIGHT = settings.General.WIDTH, settings.General.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

pygame.font.init()
button_font = pygame.font.Font(None, 30)

background_image = pygame.image.load(settings.Images.background_home)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

enemy_image = pygame.image.load(settings.Images.enemy)
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
enemies = initialize_enemies(10, enemy_image, WIDTH, HEIGHT)

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    click_sound = pygame.mixer.Sound(settings.Sounds.click)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action:
            click_sound.play()
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    button_text = button_font.render(text, True, settings.Colors.WHITE)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)

def start_game():
    pygame.mixer.music.set_volume(0.1)
    new_background_image = pygame.image.load(settings.Images.background_game)
    new_background_image = pygame.transform.scale(new_background_image, (WIDTH, HEIGHT))
    laser_sound = pygame.mixer.Sound(settings.Sounds.laser)
    enemy_laser_sound = pygame.mixer.Sound(settings.Sounds.enemy_laser)

    rocket = pygame.image.load(settings.Images.rocket)
    rocket = pygame.transform.scale(rocket, (100, 100))
    character_x, character_y = WIDTH // 2, HEIGHT - 100
    character_speed = 5
    bullets = []
    enemy_bullets = []
    last_shot = 0
    shoot_delay = 200

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and character_x - character_speed >= -40:
            character_x -= character_speed
        if keys[pygame.K_RIGHT] and character_x + character_speed + 60 <= WIDTH:
            character_x += character_speed
        if keys[pygame.K_UP] and character_y - character_speed >= -10:
            character_y -= character_speed
        if keys[pygame.K_DOWN] and character_y + character_speed + 100 <= HEIGHT:
            character_y += character_speed

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_shot > shoot_delay:
            bullet_x = character_x + 50
            bullet_y = character_y
            bullets.append([bullet_x, bullet_y])
            last_shot = current_time
            laser_sound.play()

        for bullet in bullets:
            bullet[1] -= 10

        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        for bullet in enemy_bullets:
            bullet[1] += 5

        enemy_bullets = [bullet for bullet in enemy_bullets if bullet[1] < HEIGHT]

        check_bullet_collision(bullets, enemies)
        update_enemies(enemies, enemy_bullets, speed=0.5)

        screen.blit(new_background_image, (0, 0))
        screen.blit(rocket, (character_x, character_y))
        draw_enemies(enemies, screen)
        for bullet in bullets:
            pygame.draw.rect(screen, settings.Colors.WHITE, (bullet[0], bullet[1], 5, 10))
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, settings.Colors.GREEN, (bullet[0], bullet[1], 5, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def quit_game():
    pygame.quit()
    sys.exit()

def load_home():
    screen.blit(background_image, (0, 0))

    draw_button("Jogar", WIDTH // 2 - 100, 350, 200, 40, settings.Colors.PINK, settings.Colors.DARK_PINK, start_game)
    draw_button("Sair", WIDTH // 2 - 100, 400, 200, 40, settings.Colors.CIANO, settings.Colors.DARK_PINK, quit_game)

running = True
while running:
    load_home()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
