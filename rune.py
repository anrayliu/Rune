import pygame
import sys #exit()
import os #remove()
import config, player, window, interface, events
pygame.init()

        
class Main:
    def __init__(self):
        self.events = events.Events()
        self.clock = pygame.time.Clock()
        self.win = window.Window().win
        
        self.player = player.Player(self.win)
        self.interface = interface.Interface(self.win, self.events, self.player)
        
    def run(self):
        while True:
            self.events.update()
            if self.events.quit:
                self.quit()
            self.clock.tick(60)
            
            if self.events.resize:
                self.player.adjust()
                self.interface.adjust()
            
            self.interface.update()
            self.player.update()
            if not self.player.audio.active:
                if config.config["loop"]:
                    self.player.restart()
                elif self.player.next != "":
                    self.player.file_index += 1
                    self.player.get_surrounding_vids()
                    self.player.extract_info()
                    self.player.audio.play()
                else:
                    self.quit()
            
            self.win.fill((0, 0, 0))
            self.player.draw()
            self.interface.draw()
            pygame.display.update()
            
    def quit(self):
        del self.player.audio
        os.remove(self.player.audio_file)
        pygame.quit()
        sys.exit()


if "file" in config.config:
    Main().run()