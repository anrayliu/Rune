import pygame 


class Interface:
    def __init__(self, win, events, player):
        self.win = win 
        self.events = events 
        self.player = player
        
        self.original_play = pygame.image.load("data\\play.png").convert_alpha()
        self.original_pause = pygame.image.load("data\\pause.png").convert_alpha()
        self.original_rewind = pygame.image.load("data\\rewind.png").convert_alpha()
        self.original_fast_forward = pygame.transform.flip(self.original_rewind, True, False)
        
        self.adjust()
        
    def update(self):
        if self.events.focused and self.player.rect.collidepoint(self.events.mouse):
            if self.events.click:
                if self.play_rect.collidepoint(self.events.mouse):
                    self.player.pause()
                elif self.rewind_rect.collidepoint(self.events.mouse):
                    self.player.rewind()
                elif self.fast_forward_rect.collidepoint(self.events.mouse):
                    self.player.fast_forward()
            self.show_interface = True 
        else:
            self.show_interface = False
            
    def draw(self):
        if self.show_interface:
            pygame.draw.line(self.win, (128, 128, 128), (self.w * 0.1, self.h * 0.9), (self.w * 0.9, self.h * 0.9), 8)
            pygame.draw.line(self.win, (255, 0, 0), (self.w * 0.1, self.h * 0.9), (self.w * 0.1 + self.player.audio.curr_pos * self.ratio, self.h * 0.9), 6)
            
            if self.player.audio.paused:
                self.win.blit(self.play, self.play_rect.topleft)
            else:
                self.win.blit(self.pause, self.play_rect.topleft)
                
            self.win.blit(self.rewind, self.rewind_rect.topleft)
            self.win.blit(self.fast_forward, self.fast_forward_rect.topleft)
            
    def adjust(self):
        self.w, self.h = self.win.get_size()
        self.ratio = self.w * 0.8 / self.player.duration
        
        size = int(self.player.rect.w * 0.2)
        half_size = int(self.player.rect.w * 0.1)
        quarter_size = int(self.player.rect.w * 0.05)
        
        self.play = pygame.transform.scale(self.original_play, (size, size))
        self.pause = pygame.transform.scale(self.original_pause, (size, size))
        self.rewind = pygame.transform.scale(self.original_rewind, (half_size, half_size))
        self.fast_forward = pygame.transform.scale(self.original_fast_forward, (half_size, half_size))
        
        self.play_rect = pygame.Rect(self.w / 2 - half_size, self.h / 2 - half_size, size, size)
        self.rewind_rect = pygame.Rect(self.play_rect.x - size, self.play_rect.y + quarter_size, half_size, half_size)
        self.fast_forward_rect = pygame.Rect(self.play_rect.right + half_size, self.play_rect.y + quarter_size, half_size, half_size)