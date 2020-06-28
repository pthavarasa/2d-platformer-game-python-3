import pygame

class Trap:
    def __init__(self, image, start, DS):
        self.trap = image
        self.trap_mask = pygame.mask.from_surface(self.trap)
        self.trap_rect = self.trap.get_rect()
        self.DS = DS
        self.start = start

    def set(self, x, y):
        self.x = x
        self.y = y

    def collision(self, player, plateform):
        self.offset = (int(player.x - (plateform.x + self.x)), int(player.y - (plateform.y + self.y)))
        self.result = self.trap_mask.overlap(player.player_mask, self.offset)
        self.offset_hit = int(plateform.x - self.y), int(plateform.y - self.y)
        self.result_hit = self.trap_mask.overlap(plateform.plateform_mask, self.offset_hit)
        if self.result_hit:
            return None
        else:
            if (player.x + abs(plateform.x)) > self.start:
                self.y += player.velocity
        if self.result:
            self.trap_v = True
        else:
            self.trap_v = False
        return self.trap_v

    def draw(self, plateform):
        self.DS.blit(self.trap, ((plateform.x + self.x), (plateform.y + self.y)))