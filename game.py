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

# Função para tratar a entrada do usuário
def handle_input(rocket_x, rocket_y, bullets, last_shot, laser_sound):
    rocket_speed = 5 # Velocidade da nave
    shoot_delay = 200 # Delay entre os tiros

    keys = pygame.key.get_pressed() # Pega as teclas pressionadas

    if keys[pygame.K_LEFT] and rocket_x - rocket_speed >= -20: # Verifica se a seta esquerda foi pressionada
        rocket_x -= rocket_speed # Move a nave para a esquerda
    if keys[pygame.K_RIGHT] and rocket_x + rocket_speed + 50 <= WIDTH: # Verifica se a seta direita foi pressionada
        rocket_x += rocket_speed # Move a nave para a direita
    if keys[pygame.K_UP] and rocket_y - rocket_speed >= -10: # Verifica se a seta para cima foi pressionada
        rocket_y -= rocket_speed # Move a nave para cima
    if keys[pygame.K_DOWN] and rocket_y + rocket_speed + 50 <= HEIGHT: # Verifica se a seta para baixo foi pressionada
        rocket_y += rocket_speed # Move a nave para baixo

    current_time = pygame.time.get_ticks() # Pega o tempo atual

    # Verifica se a barra de espaço foi pressionada e se o tempo do último tiro é maior que o delay entre os tiros
    if keys[pygame.K_SPACE] and current_time - last_shot > shoot_delay:
        bullet_x = rocket_x + 28 # Posição x do tiro
        bullet_y = rocket_y # Posição y do tiro
        bullets.append([bullet_x, bullet_y]) # Adiciona o tiro à lista de tiros
        last_shot = current_time # Atualiza o tempo do último tiro
        laser_sound.set_volume(0.3) # Define o volume do som do tiro
        laser_sound.play() # Toca o som do tiro

    return rocket_x, rocket_y, bullets, last_shot # Retorna a posição da nave, a lista de tiros e o tempo do último tiro

# Função para atualizar a posição dos tiros da nave
def update_rocker_bullets(bullets):
    for bullet in bullets:
            bullet[1] -= 10 # Atualiza a posição y do tiro

    bullets = [bullet for bullet in bullets if bullet[1] > 0] # Remove os tiros que saíram da tela
    return bullets

# Função para atualizar a posição dos tiros dos inimigos
def update_enemies_bullets(enemy_bullets, rocket_x, rocket_y, rocket_hits, max_lives, score):
    enemy_laser_sound = pygame.mixer.Sound(settings.Sounds.enemy_laser)

    for bullet in enemy_bullets:
            bullet[1] += 5 # Atualiza a posição y do tiro
            if rocket_x < bullet[0] < rocket_x + rocket.get_width() and \
               rocket_y < bullet[1] < rocket_y + rocket.get_height(): # Verifica se o tiro atingiu a nave
                rocket_hits += 1 # Incrementa o número de vidas perdidas
                score -= 10 # Decrementa a pontuação
                enemy_laser_sound.set_volume(0.1) # Define o volume do som do tiro do inimigo
                enemy_laser_sound.play() # Toca o som do tiro do inimigo
                enemy_bullets.remove(bullet) # Remove o tiro da lista

    enemy_bullets = [bullet for bullet in enemy_bullets if bullet[1] < HEIGHT] # Remove os tiros que saíram da tela
    return enemy_bullets, score, rocket_hits

def check_game_over(enemies, rocket_hits, rocket_y, max_lives, enemy_reached_base, score, again, is_winner):
    # se todos os inimigos foram eliminados ou a nave ultrapassou a tela superior a nave vence
    if len(enemies) == 0 or rocket_y + 5 < 0:
        is_winner = True
        again = False

    # se a nave foi atingida 3 vezes ou um inimigo ultrapassou a tela inferior a nave perde
    if rocket_hits >= max_lives or enemy_reached_base:
        is_winner = False
        again = False

    return again, is_winner

def start_game():
    rocket_x, rocket_y = WIDTH // 2, HEIGHT - 100

    global score, show_home, is_winner
    show_home = False
    pygame.mixer.music.set_volume(0.1)
    laser_sound = pygame.mixer.Sound(settings.Sounds.laser)
    
    enemies = initialize_enemies(20, enemy_image, WIDTH, HEIGHT)
    rocket_speed = 5
    bullets = []
    enemy_bullets = []
    last_shot = 0
    shoot_delay = 200
    rocket_hits = 0
    max_lives = 3
    score = 50
    again = True
    enemy_reached_base = False

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        rocket_x, rocket_y, bullets, last_shot = handle_input(rocket_x, rocket_y, bullets, last_shot, laser_sound)
        bullets = update_rocker_bullets(bullets)

        enemy_bullets, score, rocket_hits = update_enemies_bullets(enemy_bullets, rocket_x, rocket_y, rocket_hits, max_lives, score)

        score = check_bullet_collision(bullets, enemies, score)
        enemy_reached_base = update_enemies(enemies, enemy_bullets, speed=0.5, enemy_reached_base=enemy_reached_base)

        # Desenha a nave, os inimigos e o fundo
        screen.blit(new_background_image, (0, 0))
        screen.blit(rocket, (rocket_x, rocket_y))
        draw_enemies(enemies, screen)

        # Desenha os tiros
        for bullet in bullets:
            pygame.draw.rect(screen, settings.Colors.WHITE, (bullet[0], bullet[1], 5, 10))
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, settings.Colors.GREEN, (bullet[0], bullet[1], 5, 10))

        # Desenha as informações na tela
        draw_rocket_lives(screen, font, max_lives - rocket_hits, 10, 10) # Desenha as vidas da nave
        draw_enemies_counter(screen, font, len(enemies), WIDTH - 110, 10) # Desenha a quantidade de inimigos
        draw_score(screen, font, score, WIDTH // 2 - 50, 10) # Desenha a pontuação

        again, is_winner = check_game_over(enemies, rocket_hits, rocket_y, max_lives, enemy_reached_base, score, again, is_winner)
        if not again:
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
