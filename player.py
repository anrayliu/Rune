import pygame
import cv2 #VidCapture, resize()
import just_playback #Playback
import subprocess #run()
import os #path.exists(), remove(), path.join(), getcwd(), strerror
import time #time()
import natsort #natsorted()
import errno #ENOENT
import config


class Player:
    def __init__(self, win):
        self.win = win
        
        self.videos = natsort.natsorted(os.listdir(config.config["path"]))
        self.audio_file = "data\\extracted_audio.wav"
        if config.config["file"] in self.videos:
            self.file_index = self.videos.index(config.config["file"])
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config.config["file"])
        
        self.get_surrounding_vids()
        self.extract_info()
        self.adjust()
        
        self.audio.play()
        
    def extract_info(self):
        file = os.path.join(config.config["path"], self.videos[self.file_index])
        pygame.display.set_caption("Rune - " + self.videos[self.file_index])
        
        self.vid = cv2.VideoCapture(file)
        self.audio = just_playback.Playback()
        if config.config["mute"]:
            self.audio.set_volume(0)
        
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)
        start_extract = time.time()
        subprocess.run("ffmpeg -i \"{}\" -ab 160k -ac 2 -ar 44100 -loglevel quiet -vn {}".format(file, self.audio_file))
        end_extract = time.time()
        self.audio.load_file(self.audio_file)
        
        self.frame_count = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = self.audio.duration
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.frame_delay = 1 / self.fps * 1000
        
        print("file: " + self.videos[self.file_index])
        print("path: " + config.config["path"])
        print("duration : " + str(self.duration))
        print("frames: " + str(self.frame_count))
        print("fps: " + str(self.fps))
        print("next: " + self.next)
        print("previous: " + self.previous)
        print("rune_path: " + os.getcwd())
        print("extraction_time: " + str(end_extract - start_extract))
            
    def get_surrounding_vids(self):
        self.next = ""
        self.previous = ""
        if self.file_index < len(self.videos) - 1:
            self.next = self.videos[self.file_index + 1]
        if self.file_index > 0:
            self.previous = self.videos[self.file_index - 1]
        
    def update(self):
        while self.audio.curr_pos * 1000 > self.vid.get(cv2.CAP_PROP_POS_FRAMES) * self.frame_delay:
            self.has_frame, data = self.vid.read()
            
            if self.has_frame:
                data = cv2.resize(data, dsize=self.rect.size, interpolation=cv2.INTER_CUBIC)
                self.image = pygame.image.frombuffer(data.tobytes(), self.rect.size, "BGR")

    def draw(self):
        self.win.blit(self.image, self.rect.topleft)
        
    def pause(self):
        if self.audio.paused:
            self.audio.resume()
        else:
            self.audio.pause()
        
    def fast_forward(self, time=15):
        frame = self.vid.get(cv2.CAP_PROP_POS_FRAMES) + self.fps * time - 1
        if frame < self.frame_count:
            self.audio.seek(self.audio.curr_pos + time)
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame)
    
    def rewind(self, time=15):
        self.audio.seek(self.audio.curr_pos - time)
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.vid.get(cv2.CAP_PROP_POS_FRAMES) - self.fps * time - 1)
    
    def adjust(self):
        size = self.win.get_size()
        ratio = config.config["aspect_ratio"]
        
        w = size[0]
        h = int(w / (ratio[0] / ratio[1]))
        y = int(size[1] /2 - h / 2)
        x = 0
        if h > size[1]:
            h = size[1]
            w = int(h * (ratio[0] / ratio[1]))
            x = int(size[0] / 2 - w / 2)
            y = 0
            
        self.rect = pygame.Rect(x, y, w, h)
        
    def restart(self):
        self.audio.play()
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)