import pygame
import sys
import sound
import settings
import random
from enemies import initialize_enemies, draw_enemies, update_enemies, check_bullet_collision
from draw import draw_button, draw_score, draw_rocket_lives, draw_enemies_counter

pygame.init() # Inicializa o pygame

sound.start_music() # Inicia a música de fundo

WIDTH, HEIGHT = settings.General.WIDTH, settings.General.HEIGHT # Largura e altura da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Cria a tela
pygame.display.set_caption("Space Invaders") # Define o título da janela

pygame.font.init() # Inicializa as fontes
button_font = pygame.font.Font(None, 30) # Define a fonte dos botões

# Carrega as imagens
background_image = pygame.image.load(settings.Images.background_home) # Carrega a imagem de fundo da tela inicial
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) # Redimensiona a imagem para o tamanho da tela

background_loss = pygame.image.load(settings.Images.background_loss) # Carrega a imagem de fundo da tela de derrota
background_loss = pygame.transform.scale(background_loss, (WIDTH, HEIGHT)) # Redimensiona a imagem para o tamanho da tela

background_win = pygame.image.load(settings.Images.background_win) # Carrega a imagem de fundo da tela de vitória
background_win = pygame.transform.scale(background_win, (WIDTH, HEIGHT)) # Redimensiona a imagem para o tamanho da tela

new_background_image = pygame.image.load(settings.Images.background_game) # Carrega a imagem de fundo do jogo em execução
new_background_image = pygame.transform.scale(new_background_image, (WIDTH, HEIGHT)) # Redimensiona a imagem para o tamanho da tela

enemy_image = pygame.image.load(settings.Images.enemy) # Carrega a imagem do inimigo
enemy_image = pygame.transform.scale(enemy_image, (50, 50)) # Redimensiona a imagem do inimigo

rocket = pygame.image.load(settings.Images.rocket) # Carrega a imagem da nave
rocket = pygame.transform.scale(rocket, (60, 60)) # Redimensiona a imagem da nave

def start_game():
    rocket_x, rocket_y = WIDTH // 2, HEIGHT - 100

    global show_home, score, is_winner
    pygame.mixer.music.set_volume(0.1)
    laser_sound = pygame.mixer.Sound(settings.Sounds.laser)
    enemy_laser_sound = pygame.mixer.Sound(settings.Sounds.enemy_laser)

    enemies = initialize_enemies(20, enemy_image, WIDTH, HEIGHT)
    rocket_speed = 5
    bullets = []
    enemy_bullets = []
    last_shot = 0
    shoot_delay = 200
    rocket_hits = 0
    max_lives = 3
    score = 0

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and rocket_x - rocket_speed >= -20:
            rocket_x -= rocket_speed
        if keys[pygame.K_RIGHT] and rocket_x + rocket_speed + 50 <= WIDTH:
            rocket_x += rocket_speed
        if keys[pygame.K_UP] and rocket_y - rocket_speed >= -10:
            rocket_y -= rocket_speed
        if keys[pygame.K_DOWN] and rocket_y + rocket_speed + 50 <= HEIGHT:
            rocket_y += rocket_speed

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_shot > shoot_delay:
            bullet_x = rocket_x + 28
            bullet_y = rocket_y
            bullets.append([bullet_x, bullet_y])
            last_shot = current_time
            laser_sound.set_volume(0.5)
            laser_sound.play()

        for bullet in bullets:
            bullet[1] -= 10

        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        if (rocket_y + 5 < 0):
            show_home = False
            is_winner = True
            return

        for bullet in enemy_bullets:
            bullet[1] += 5
            if rocket_x < bullet[0] < rocket_x + rocket.get_width() and \
               rocket_y < bullet[1] < rocket_y + rocket.get_height():
                rocket_hits += 1
                score -= 10
                enemy_laser_sound.set_volume(0.1)
                enemy_laser_sound.play()
                enemy_bullets.remove(bullet)
                if rocket_hits >= max_lives:
                    show_home = False
                    is_winner = False
                    return

        enemy_bullets = [bullet for bullet in enemy_bullets if bullet[1] < HEIGHT]

        enemies_count_before = len(enemies)
        check_bullet_collision(bullets, enemies)
        score += (enemies_count_before - len(enemies)) * 100
        if update_enemies(enemies, enemy_bullets, speed=0.5):
            show_home = False
            is_winner = False
            return

        screen.blit(new_background_image, (0, 0))
        screen.blit(rocket, (rocket_x, rocket_y))
        draw_enemies(enemies, screen)
        for bullet in bullets:
            pygame.draw.rect(screen, settings.Colors.WHITE, (bullet[0], bullet[1], 5, 10))
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, settings.Colors.GREEN, (bullet[0], bullet[1], 5, 10))

        draw_rocket_lives(screen, font, max_lives - rocket_hits, 10, 10)
        draw_enemies_counter(screen, font, len(enemies), WIDTH - 110, 10)
        draw_score(screen, font, score, WIDTH // 2 - 50, 10)

        if len(enemies) == 0:
            show_home = False
            is_winner = True
            return

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def quit_game():
    pygame.quit()
    sys.exit()

def show_game_over():
    screen.blit(background_win if is_winner else background_loss, (0, 0))
    draw_score(screen, button_font, score, WIDTH // 2 - 100, 300)

    draw_button(screen, "Jogar Novamente", WIDTH // 2 - 100, 350, 200, 40, settings.Colors.PINK, settings.Colors.DARK_PINK, start_game)
    draw_button(screen, "Sair", WIDTH // 2 - 100, 400, 200, 40, settings.Colors.CIANO, settings.Colors.DARK_PINK, quit_game)


def load_home():
    screen.blit(background_image, (0, 0))

    draw_button(screen, "Jogar", WIDTH // 2 - 100, 350, 200, 40, settings.Colors.PINK, settings.Colors.DARK_PINK, start_game)
    draw_button(screen, "Sair", WIDTH // 2 - 100, 400, 200, 40, settings.Colors.CIANO, settings.Colors.DARK_PINK, quit_game)


running = True
show_home = True
is_winner = False
score = 0
while running:
    load_home() if show_home else show_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
