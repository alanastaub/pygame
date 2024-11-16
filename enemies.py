import pygame
import random

def initialize_enemies(num_enemies, enemy_image, width, height):
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(0, width - enemy_image.get_width())
        y = random.randint(-1500, -100)
        enemies.append({"x": x, "y": y, "lives": 3, "image": enemy_image})
    return enemies

def draw_enemies(enemies, screen):
    for enemy in enemies:
        screen.blit(enemy["image"], (enemy["x"], enemy["y"]))

def update_enemies(enemies, enemy_bullets, speed):
    for enemy in enemies:
        enemy['y'] += speed
        if enemy['lives'] <= 0:
            enemies.remove(enemy)
        if random.randint(0, 900) < 1:  # 1% chance to shoot each frame
            bullet_x = enemy['x'] + enemy['image'].get_width() // 2
            bullet_y = enemy['y'] + enemy['image'].get_height()
            enemy_bullets.append([bullet_x, bullet_y])

def check_bullet_collision(bullets, enemies):
    for bullet in bullets:
        for enemy in enemies:
            if enemy['x'] < bullet[0] < enemy['x'] + enemy['image'].get_width() and \
               enemy['y'] < bullet[1] < enemy['y'] + enemy['image'].get_height():
                enemy['lives'] -= 1
                bullets.remove(bullet)
                if enemy['lives'] <= 0:
                    enemies.remove(enemy)
                break