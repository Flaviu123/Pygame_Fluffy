import pygame
import os
import random


class Settings(object):                                 # Die Klasse in der klasse speicher ich Variabeln, Dateipfade
    window_width = 500
    window_height = 750
    fps = 60
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    modus = "mask"
    caption = "Pygame"
    nof_meteor = 15
    score = 0
    life = 3
    countspeed = 0


class Background(object):                               #Ich lade den Hintergrund und passe ich an das Fenster an
    def __init__(self, filename="background03.png") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):                             #Der Hintergrund wird gezeichnet
        screen.blit(self.image, (0, 0))


class Player(pygame.sprite.Sprite):                     #Ich lade das Player image, scaliere und die kolision
    def __init__(self, picturefile) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path, picturefile)).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (40, 35))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = 10
        self.rect.centery = 10
        self.speed_v = 0
        self.speed_h = 0
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height

    def update(self):                                   #sorgt dafür das man nicht raus kann und das man sich bewegen kann
        self.wall_collision()
        self.rect.move_ip((self.speed_h, self.speed_v))

    def draw(self, screen):                             #spieler wird gezeichnet
        screen.blit(self.image, self.rect)

    def wall_collision(self):                           #überprüft ob sich der spieler am rand befindet
        if self.rect.top + self.speed_v < 0:
            self.stop_v()
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.stop_v()
        if self.rect.left + self.speed_h < 0:
            self.stop_h()
        if self.rect.right + self.speed_h > Settings.window_width:
            self.stop_h()

    def stop_v(self):                                   #Ein reset für die Vertikale Geschwindigkeit
        self.speed_v = 0

    def stop_h(self):                                   #Ein reset für die Horizontale Geschiwindigkeit
        self.speed_h = 0

    def down(self):                                     #Geschwindigkeit nach unten
        self.speed_v = 4

    def up(self):                                       #Geschwindigkeit nach oben
        self.speed_v = -4

    def left(self):                                     #Geschwindigkeit nach links
        self.speed_h = -4

    def right(self):                                    #Geschwindigkeit nach rechts
        self.speed_h = 4


class Meteor(pygame.sprite.Sprite):                     #Lädt das Image für die gegenstände die fallen ein
    def __init__(self) -> None:
        super().__init__()
        self.width = random.randint(40, 60)             #scaliert diese in verschiedenen größen
        self.image_orig = pygame.image.load(os.path.join(Settings.image_path, "Asteroid_Brown.png")).convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (self.width, self.width))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(1, Settings.window_width - self.rect.width)
        self.speed_v = random.randint(1, 3) + Settings.countspeed         #Geschwindigkeit beim fallen der Meteorieten

        self.score = 0

    def update(self):                                   #Updatet das die Meteorieten scih bewegen und überprüft ob ein Meteor unten ist
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.count_hit()
        self.rect.move_ip((0, self.speed_v))

    def draw(self, screen):                             #Zeichnet die Meteorieten
        screen.blit(self.image, self.rect)

    def count_hit(self):                                #entfernt die Meteoriten die unten angelangt sind zählt das ganze mit einer variabel und lässt die geschwindigkeit wachsen
        self.kill()
        Settings.score += 1
        if Settings.countspeed <= 4:
            Settings.countspeed += 0.03


class Game(object):                                    #fügt die bitmaps zu klassen hinzu, überprüft kollision, lebensabzug und tot, Updatet das Programm, Input definition
    def __init__(self) -> None:
        super().__init__()

        pygame.init()

        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"

        pygame.display.set_caption(Settings.caption)

        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.background = Background()
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player("player.png"))
        self.meteor = pygame.sprite.Group()

        self.running = False

    def run(self):                                      #führt die wichtigsten methoden aus in einer Whileschleiche aus
        self.start()
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        pygame.quit()

    def watch_for_events(self):                         #überprüft Tastendrücke und reagiert darauf
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.player.sprite.down()
                elif event.key == pygame.K_UP:
                    self.player.sprite.up()
                elif event.key == pygame.K_LEFT:
                    self.player.sprite.left()
                elif event.key == pygame.K_RIGHT:
                    self.player.sprite.right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.sprite.stop_v()
                elif event.key == pygame.K_UP:
                    self.player.sprite.stop_v()
                elif event.key == pygame.K_LEFT:
                    self.player.sprite.stop_h()
                elif event.key == pygame.K_RIGHT:
                    self.player.sprite.stop_h()

    def start(self):                                    #Methode die am anfang die Metheorieten spawned und den background und den spieler spawned
        self.background = Background()
        self.spawn()
        for a in range(Settings.nof_meteor):
            self.meteor.add(Meteor())
    def spawn(self):                                    #fügt den spieler hinzu
        self.player.add(Player("player.png"))

    def update(self):                                   #Updatet alle methoden die Benötigt werden
        self.check_for_collision()
        self.player.update()
        self.meteor.update()
        if len(self.meteor.sprites()) < 15:
            self.meteor.add(Meteor())


    def draw(self):                                     #Zeichnet die einzelnen Bitmaps und gibt diese aus
        self.background.draw(self.screen)
        self.meteor.draw(self.screen)
        self.player.draw(self.screen)
        text_surface_score = self.font.render("Score: {0}".format(Settings.score), True, (255, 255, 255))
        self.screen.blit(text_surface_score, dest=(10, 10))

        pygame.display.flip()

    def life(self):                                     #überprüft ob man noch leben hat
        if Settings.life <= 0:
            self.death()

    def death(self):
        self.running = False

    def check_for_collision(self):                      #Überprüft ob eine kolision zwischen dem player und einem Metheor vorliegt wenn ja zieht er ein leben ab
        self.player.hit = pygame.sprite.groupcollide(self.player, self.meteor, True, False, pygame.sprite.collide_mask)
        if self.player.hit:
            Settings.life -= 1
            self.spawn()
            if Settings.life <= 0:
                self.death()

if __name__ == '__main__':

    game = Game()
    game.run()
