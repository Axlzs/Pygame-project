import pygame

class Animation:
    # Sprite sheet  has all the animations in a single line
    # All animations -> actions -> frames -> frame_index 
    def __init__(self, frames, cooldown):
        self.frames = frames  # List of frames for a speficific action 
        self.cooldown = cooldown # Time interval between animation frames
        self.last_update = 0 
        self.frame_index = 0
        self.is_playing = True
        self.loop = True # Some animations need to run only once, others more than once

    def get_current_frame(self):
        # Returns the current frame
        self.loop = True
        if not self.is_playing:
            return self.frames[self.frame_index]  # Return the current frame instead of the whole list
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.cooldown:
            if self.loop:
                # Loop through the frames
                self.frame_index = (self.frame_index+1) % len(self.frames)  # Wrap around to the start
            elif self.frame_index < len(self.frames) - 1:
                self.frame_index += 1
                
            self.last_update = current_time  # Update the last update time
        return self.frames[self.frame_index]  # Return the current frame based on frame_index
    
    def play_once(self):
        self.loop = False
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.cooldown:
            if self.frame_index < len(self.frames) - 1:
                self.frame_index += 1  # Advance frame until the last one
            else:
                self.is_playing = False  # Stop animation if it reaches the end without looping
            self.last_update = current_time
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
