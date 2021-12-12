import pygame 
import config 
import win32gui #setwindowpos(), getwindowrect()
import os #path.exists()


class Window:
    def __init__(self):
        self.win = pygame.display.set_mode(config.config["window_size"], pygame.RESIZABLE * config.config["resizable"])
        pygame.display.set_caption("Rune")
        if os.path.exists("data\\icon.png"):
            pygame.display.set_icon(pygame.image.load("data\\icon.png"))
        hwnd = pygame.display.get_wm_info()["window"]
        rect = win32gui.GetWindowRect(hwnd)
        win32gui.SetWindowPos(hwnd, -1, rect[0], rect[1], rect[2], rect[3], 1)