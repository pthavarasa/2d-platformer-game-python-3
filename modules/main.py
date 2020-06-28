import pygame, random, sys, math, time
from pygame.locals import *
from modules.button import Button
from modules.plateform import Plateform
from modules.thorns import Thorns
from modules.trap import Trap
from modules.player import Player

class Ninja:
    def __init__(self):
        # initialise display
        pygame.init()

        # initialise display
        self.W, self.H = 768, 512
        self.HW, self.HH = self.W / 2, self.H / 2
        self.DS = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Ultimate Ninja")
        self.fps_clock = pygame.time.Clock()
        self.FPS = 300

        # define some colors
        self.White = (255,255,255)
        self.Black = (0,0,0)
        self.Red = (255,59,48)

        # define game status
        self.start = False
        self.pause = False
        self.lost = False

    def menu(self):
        # initialise menu
        self.menu_bg = pygame.image.load('./sources/images/menu_bg.png').convert_alpha()
        self.button_width, self.button_height = 150, 50
        self.button_x = (self.W / 2) - (self.button_width / 2)
        self.button_y = (self.H / 2) - (self.button_height / 2)
        self.button_text_color = self.White
        self.button_bg_color = self.Red
        self.button_font_size = 50
        self.font = pygame.font.SysFont("comicsansms", self.button_font_size)
        self.button_text_0 = 'Play'
        self.button_text_1 = 'Quit'
        self.button_text_2 = 'Continue'
        self.button_text_3 = 'Game Over'
        self.button_play = Button(self.button_x, self.button_y, self.button_width, self.button_height,
                                  self.button_text_color, self.button_bg_color, self.button_text_0, self.font, self.DS)
        self.game_over = Button(self.button_x, self.button_y, self.button_width, self.button_height,
                                  self.button_text_color, self.button_bg_color, self.button_text_3, self.font, self.DS)
        self.button_quit = Button(self.button_x, self.button_y + 75, self.button_width, self.button_height,
                                  self.button_text_color, self.button_bg_color, self.button_text_1, self.font, self.DS)
        self.button_continue = Button(self.button_x, self.button_y, self.button_width, self.button_height,
                                      self.button_text_color, self.button_bg_color, self.button_text_2, self.font,
                                      self.DS)

    def play(self):
        # initialise plateform and player
        self.bg = pygame.image.load('./sources/images/bg.png').convert_alpha()

        self.obstacle = pygame.image.load('./sources/images/plateforme.png').convert_alpha()

        self.plateform = Plateform(self.bg, self.obstacle, self.HW, self.DS)
        self.plateform.set()
        self.green_blob = pygame.image.load('./sources/images/player.png').convert_alpha()
        self.green_blob = pygame.transform.scale(self.green_blob, (25, 50))

        self.jumpCounter = 0
        self.maxJumpRange = 90
        self.velocity = 1

        self.player = Player(self.green_blob, self.velocity, self.maxJumpRange, self.DS)
        self.player.set(0, 0, False, False, 0)

    def thorns(self):
        self.image = pygame.image.load('./sources/images/thorns.png').convert_alpha()
        self.thorns = Thorns(self.image, self.DS)
        self.thorns.set()

    def traps(self):
        self.trap_img_0 = pygame.image.load('./sources/images/trap_0.png').convert_alpha()
        self.trap_img_1 = pygame.image.load('./sources/images/trap_1.png').convert_alpha()
        self.trap_0 = Trap(self.trap_img_0, 700, self.DS)
        self.trap_01 = Trap(self.trap_img_0, 1800, self.DS)
        self.trap_1 = Trap(self.trap_img_1, 2900, self.DS)
        self.trap_0.set(330, -175)
        self.trap_01.set(1550, -175)
        self.trap_1.set(2900, -400)

    def level_1(self):
        self.plateform.keys(self.player)
        self.plateform.jump(self.player)
        self.plateform.move(self.player)
        self.plateform.collision(self.player)
        if self.thorns.collision(self.player, self.plateform):
            self.lost = True
        if self.trap_0.collision(self.player, self.plateform) or self.trap_01.collision(self.player,
                                                                                        self.plateform) or self.trap_1.collision(
                self.player, self.plateform):
            self.lost = True
        self.plateform.draw()
        self.player.draw()
        self.thorns.draw(self.plateform)
        self.trap_0.draw(self.plateform)
        self.trap_01.draw(self.plateform)
        self.trap_1.draw(self.plateform)

    def sound(self):
        pygame.mixer.music.load('./sources/music/music.wav')
        self.button_sound = pygame.mixer.Sound('./sources/sounds/button.wav')
        self.lost_sound = pygame.mixer.Sound('./sources/sounds/pipe.wav')

    def main(self):
        self.menu()
        self.thorns()
        self.traps()
        self.play()
        self.sound()
        pygame.mixer.music.play(1)
        while True:
            # exit the program
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_play.check() == True or self.button_continue.check() == True:
                        pygame.mixer.Sound.play(self.button_sound)
                        pygame.time.delay(500)
                        self.start = True
                        self.pause = False
                    elif self.button_quit.check() == True:
                        pygame.mixer.Sound.play(self.button_sound)
                        pygame.time.delay(500)
                        pygame.quit()
                        sys.exit()
                if self.button_play.check() == True or self.button_continue.check() == True:
                    self.button_play.collide_color()
                    self.button_continue.collide_color()
                elif self.button_quit.check() == True:
                    self.button_quit.collide_color()
                else:
                    self.button_play.default_color()
                    self.button_quit.default_color()
                    self.button_continue.default_color()

            k = pygame.key.get_pressed()
            if k[pygame.K_p]:
                self.start = False
                self.pause = True

            if self.start == True and self.pause == False:
                self.level_1()
            elif self.start == False and self.pause == False:
                self.DS.blit(self.menu_bg, [0, 0])
                self.button_play.draw()
                self.button_quit.draw()
            elif self.start == False and self.pause == True:
                self.DS.blit(self.menu_bg, [0, 0])
                self.button_continue.draw()
                self.button_quit.draw()
            if self.lost:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(self.lost_sound)
                self.DS.blit(self.menu_bg, [0, 0])
                self.game_over.default_color()
                self.game_over.drawTextcenter()
                self.button_quit.draw()

            pygame.display.update()
            self.fps_clock.tick(self.FPS)