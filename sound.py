import pygame
import settings

def start_music():
    pygame.mixer.init()
    pygame.mixer.music.load(settings.Sounds.background)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)