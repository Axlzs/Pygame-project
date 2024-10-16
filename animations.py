import pygame
import spritesheet
from static_variables import *

class Animation:
    # Sprite sheet  has all the animations in a single line
    # All animations -> actions -> frames -> frame_index 
    def __init__(self, frames, cooldown):
        self.frames = frames  # List of frames for a speficific action 
        self.cooldown = cooldown # Time interval between animation frames
        self.last_update = pygame.time.get_ticks() 
        self.frame_index = 0
        self.is_playing = True
        self.loop = True # Some animations need to run only once, others more than once

    def get_current_frame(self):
        # Returns current frame
        if not self.is_playing:
            return self.frames[self.frame_index]
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.cooldown[self.frame_index]:
            if self.loop:
                """While frame_index is less than total frames, the action will run, 
                however, if both values are the same e.g frame_index = 5 
                and total frames is 5 means that we have reached the last frame of an action, 
                and so the answer to this equasion would be 0 indicating that 
                we have gone through all the frames"""
                self.frame_index = (self.frame_index + 1) % (len(self.frames)+1) 
            elif self.frame_index < len(self.frames) -1:
                self.frame_index +=1
        self.last_update = current_time # Notes the last time the animation was updated 
        return self.frames[self.frame_index]

    def is_completed(self):
        return self.frame_index == len(self.frames) - 1 and not self.loop
     
    def reset(self):
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
    
    def play(self):
        self.is_playing = True

    def stop(self):
        self.is_playing = False
