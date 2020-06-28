import pygame

class Player:
    def __init__(self, image, velocity, maxJumpRange, DS):
        self.velocity = velocity
        self.maxJumpRange = maxJumpRange
        self.player = image
        self.width, self.height = self.player.get_rect().size
        self.player_mask = pygame.mask.from_surface(self.player)
        self.player_rect = self.player.get_rect()
        self.DS = DS

    def set(self, x, y, jumping, falling, j_count):
        self.x = x
        self.y = y
        self.jumping = jumping
        self.falling = falling
        self.jump_counter = j_count

    def draw(self):
        self.DS.blit(self.player, (self.x, self.y))