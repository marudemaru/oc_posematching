import pygame

def initialize_bgm():
    pygame.mixer.init()

def play_bgm(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def stop_bgm():
    pygame.mixer.music.stop()

def play_sound_effect(file):
    effect = pygame.mixer.Sound(file)
    effect.play()
