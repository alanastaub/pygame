import pygame
import random
from settings import General

# Função para inicializar os inimigos
# Parâmetros: número de inimigos, imagem do inimigo, largura e altura da tela
def initialize_enemies(num_enemies, enemy_image, width, height):
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(0, width - enemy_image.get_width()) # Posição x aleatória
        y = random.randint(-2000, -100) # Posição y aleatória
        enemies.append({"x": x, "y": y, "lives": 3, "image": enemy_image}) # Adiciona o inimigo à lista de inimigos
    return enemies

# Função para desenhar os inimigos
# Parâmetros: lista de inimigos, tela
def draw_enemies(enemies, screen):
    for enemy in enemies:
        # Desenha as vidas do inimigo
        for i in range(enemy["lives"]):
            pygame.draw.circle(screen, (255, 0, 0), (enemy["x"] + i * 12 + 12, enemy["y"] - 5), 4)
        screen.blit(enemy["image"], (enemy["x"], enemy["y"])) # Desenha o inimigo na tela

# Função para atualizar a posição dos inimigos
# Parâmetros: lista de inimigos, lista de tiros dos inimigos, velocidade, se um inimigo ultrapassou a tela
def update_enemies(enemies, enemy_bullets, speed, enemy_reached_base):
    for enemy in enemies:
        enemy['y'] += speed # Atualiza a posição y do inimigo
        if enemy['lives'] <= 0:
            enemies.remove(enemy) # Remove o inimigo da lista se suas vidas acabaram
        if random.randint(0, 900) < 1:  # Chance de atirar
            bullet_x = enemy['x'] + enemy['image'].get_width() // 2 # Posição x do tiro
            bullet_y = enemy['y'] + enemy['image'].get_height() # Posição y do tiro
            enemy_bullets.append([bullet_x, bullet_y]) # Adiciona o tiro à lista de tiros dos inimigos
        if enemy['y'] + enemy['image'].get_height() > General.HEIGHT:
            enemy_reached_base = True # Define que um inimigo ultrapassou a tela

    return enemy_reached_base

# Função para verificar colisão dos tiros com os inimigos
# Parâmetros: lista de tiros, lista de inimigos, pontuação
def check_bullet_collision(bullets, enemies, score):
    for bullet in bullets:
        for enemy in enemies:
            # Verifica se o tiro atingiu o inimigo
            if enemy['x'] < bullet[0] < enemy['x'] + enemy['image'].get_width() and \
               enemy['y'] < bullet[1] < enemy['y'] + enemy['image'].get_height():
                enemy['lives'] -= 1 # Remove uma vida do inimigo
                score += 10 # Incrementa a pontuação
                bullets.remove(bullet) # Remove o tiro da lista
                if enemy['lives'] <= 0: # Se o inimigo não tem mais vidas
                    score += 100 # Incrementa a pontuação
                    enemies.remove(enemy) # Remove o inimigo da lista
                break

    return score