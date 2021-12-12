import pygame


class Events:
    def __init__(self):
        self.update()
        
    def update(self):
        self.quit = False
        self.resize = False
        self.click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.VIDEORESIZE:
                self.resize = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
                     
        self.mouse = pygame.mouse.get_pos()
        self.focused = pygame.mouse.get_focused()