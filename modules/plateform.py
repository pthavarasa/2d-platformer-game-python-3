import pygame

class Plateform:
    def __init__(self, bg, image, screen_HW, DS):
        self.bg = bg # background image
        self.plateform = image # Plateform image
        self.width, self.height = self.plateform.get_rect().size # size of width and height
        self.plateform_mask = pygame.mask.from_surface(self.plateform) # plateform mask usefull for collision
        self.plateform_rect = self.plateform.get_rect()
        self.x = 0
        self.y = 0
        self.screen_HW = screen_HW # half width of display
        self.DS = DS # display
        self.state = {'left': False, 'right': False, 'oxS': False, 'mxS': False, 'jumping': False, 'falling': False} #

    def set(self):
        self.x = 0
        self.y = 0
        self.state['left'] = False
        self.state['right'] = False
        self.state['oxS'] = False
        self.state['mxS'] = False
        self.state['jumping'] = False
        self.state['falling'] = False

    def collision(self, player):

        self.offset = (int(player.x - self.x), int(player.y - self.y))
        self.result_0 = self.plateform_mask.overlap(player.player_mask, self.offset)
        self.result_1 = self.plateform_mask.overlap(player.player_mask, (self.offset[0], self.offset[1] + player.velocity))

        if self.result_0:
            if self.state['left'] and self.state['oxS']:
                self.x -= player.velocity
            elif self.state['left'] and self.state['mxS']:
                player.x += player.velocity
            elif self.state['right'] and self.state['oxS']:
                self.x += player.velocity
            elif self.state['right'] and self.state['mxS']:
                player.x -= player.velocity
        else:
            if self.result_1:
                self.state['falling'] = False
            else:
                if not self.state['jumping']:
                    player.y += player.velocity
                    self.state['falling'] = True

    def keys(self, player):
        self.state['mxS'] = False
        self.state['oxS'] = False
        self.state['left'] = False
        self.state['right'] = False
        k = pygame.key.get_pressed()
        if k[pygame.K_LEFT]:
            self.state['left'] = True
            self.state['right'] = False
        elif k[pygame.K_RIGHT]:
            self.state['right'] = True
            self.state['left'] = False
        if k[pygame.K_UP] and not self.state['jumping'] and not self.state['falling']:
            self.state['jumping'] = True
            player.jump_counter = 0

    def jump(self, player):
        if self.state['jumping']:
            player.y -= player.velocity
            player.jump_counter += 1
            if player.jump_counter == player.maxJumpRange:
                self.state['jumping'] = False

    def move(self, player):
        if self.state['right'] and player.x >= 0 and player.x < self.screen_HW:
            player.x += player.velocity
            self.state['mxS'] = True
        if self.state['left'] and player.x > 0 and player.x <= self.screen_HW and self.x == 0:
            player.x -= player.velocity
            self.state['mxS'] = True
        if self.state['right'] and self.x > -(self.width - self.screen_HW * 2) and player.x >= self.screen_HW:
            self.x -= player.velocity
            self.state['oxS'] = True
        if self.state['left'] and self.x >= -(self.width - self.screen_HW * 2) and player.x == self.screen_HW:
            self.x += player.velocity
            self.state['oxS'] = True
        if self.state['right'] and self.x <= -(self.width - self.screen_HW * 2) and player.x < (self.screen_HW * 2 - player.width):
            player.x += player.velocity
            self.state['mxS'] = True
        if self.state['left'] and self.x <= -(self.width - self.screen_HW * 2) and player.x <= (self.screen_HW * 2 - player.width):
            player.x -= player.velocity
            self.state['mxS'] = True

    def draw(self):
        self.DS.blit(self.bg, (self.x, self.y))
        self.DS.blit(self.plateform, (self.x, self.y))