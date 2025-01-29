import pygame
import sys
import settings

class Render:
    def __init__(self):
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
        pygame.display.set_caption("Adventure Game")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            pygame.display.update()
            self.clock.tick(settings.FPS)

if __name__ == '__main__':
    game = Render()
    game.run()