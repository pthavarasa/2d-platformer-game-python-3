import pygame

class Thorns:
    def __init__(self, image, DS):
        self.thorns = image
        self.thorns_mask = pygame.mask.from_surface(self.thorns)
        self.thorns_rect = self.thorns.get_rect()
        self.DS = DS

    def set(self):
        self.x = 0
        self.y = 0

    def collision(self, player, plateform):
        self.offset = (int(player.x - (plateform.x + self.x)), int(player.y - (plateform.y + self.y)))
        self.result = self.thorns_mask.overlap(player.player_mask, self.offset)
        if self.result:
            self.thorn = True
        else:
            self.thorn = False
        return self.thorn

    def draw(self, plateform):
        self.DS.blit(self.thorns, ((plateform.x + self.x), (plateform.y + self.y)))