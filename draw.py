import pygame
import settings

pygame.font.init() # Inicializa as fontes
button_font = pygame.font.Font(None, 30) # Define a fonte dos botões

# Função para desenhar um botão na tela
# Parâmetros: texto, posição x, posição y, largura, altura, cor, cor ao passar o mouse por cima, ação ao clicar
def draw_button(screen, text, x, y, width, height, color, hover_color, action=None):
    click_sound = pygame.mixer.Sound(settings.Sounds.click) # Carrega o som de clique
    mouse = pygame.mouse.get_pos() # Pega a posição do mouse
    click = pygame.mouse.get_pressed() # Pega o clique do mouse

    if x < mouse[0] < x + width and y < mouse[1] < y + height: # Verifica se o mouse está em cima do botão
        pygame.draw.rect(screen, hover_color, (x, y, width, height)) # Desenha o botão com a cor de hover
        if click[0] == 1 and action: # Verifica se o botão foi clicado
            click_sound.play() # Toca o som de clique
            action() # Executa a ação do botão
    else:
        pygame.draw.rect(screen, color, (x, y, width, height)) # Desenha o botão com a cor normal

    button_text = button_font.render(text, True, settings.Colors.WHITE) # Renderiza o texto do botão
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2)) # Pega o retângulo do texto
    screen.blit(button_text, text_rect) # Desenha o texto na tela


# Função para desenhar a pontuação na tela
# Parâmetros: tela, fonte, pontuação, posição x, posição y, tamanho da fonte
def draw_score(screen, font, score, x, y, font_size=36):
    font = pygame.font.Font(None, font_size) # Define a fonte
    score_text = font.render(f'Pontos: {score}', True, settings.Colors.WHITE) # Renderiza o texto da pontuação
    screen.blit(score_text, (x, y)) # Desenha o texto na tela

# Função para desenhar as vidas da nave na tela
# Parâmetros: tela, fonte, vidas, posição x, posição y
def draw_rocket_lives(screen, font, lives, x, y):
    font = pygame.font.Font(None, 25) # Define a fonte
    lives_text = font.render(f'Vidas: {lives}', True, settings.Colors.WHITE, settings.Colors.DARK_PINK) # Renderiza o texto das vidas
    screen.blit(lives_text, (x, y)) # Desenha o texto na tela

# Função para desenhar o contador de inimigos na tela
# Parâmetros: tela, fonte, inimigos, posição x, posição y
def draw_enemies_counter(screen, font, enemies, x, y):
    font = pygame.font.Font(None, 25) # Define a fonte
    enemies_text = font.render(f'Inimigos: {enemies}', True, settings.Colors.WHITE) # Renderiza o texto do contador de inimigos
    screen.blit(enemies_text, (x, y)) # Desenha o texto na tela