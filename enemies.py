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

def update_enemies(enemies, speed):
    for enemy in enemies:
        enemy["y"] += speed