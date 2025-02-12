from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame, sys, time

pygame.mixer.init()

def play_music(game) -> None:

    while game.current_location_id in range(2,10):
        pygame.mixer.music.load("gerstein_audio.mp3")
        pygame.mixer.music.play(fade_ms=2000)
        time.sleep(3)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.stop()




# Load and play background music (loops indefinitely)
pygame.mixer.music.load("background.mp3")  # Replace with your file
pygame.mixer.music.play(-1)  # -1 means loop forever




pygame.mixer.music.play(loops=-1, fade_ms= 2000)

pygame.mixer.music.rewind()

pygame.mixer.music.stop()

pygame.mixer.music.pause()

pygame.mixer.music.unpause()

pygame.mixer.music.fadeout(2000)

pygame.mixer.set_volume(0.5)

pygame.mixer.get_busy()
