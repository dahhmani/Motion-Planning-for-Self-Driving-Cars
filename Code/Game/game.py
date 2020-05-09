import pygame

class car_game():
    def __init__(self,gameMode):
        pygame.init()
        self.gameMode=gameMode

        self.pixpermeter=30 #pixels/meter

        # Set up canvas
        self.clock = pygame.time.Clock()
        self.run = True

        self.all_sprites = pygame.sprite.Group()
        self.obst_list = pygame.sprite.Group()
        self.active_list=pygame.sprite.Group()
