import pygame
from pygame.locals import *
import random


#Farben
BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
RED       = (  0, 255, 0)



#Dimensionen
BOARDHEIGHT = 1000
BOARDLENGTH = 1400






class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.image = pygame.image.load("abgespacter_boy.png")
        self.image = pygame.transform.scale(self.image, (150, 75))
        self.rect = self.image.get_rect()

    def set_player_position(self): #Startposition von Spieler
        self.rect.centerx = BOARDLENGTH/2
        self.rect.y = BOARDHEIGHT-BOARDHEIGHT/7


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_cord, y_cord):
        super(Bullet, self).__init__()

        self.image = pygame.image.load("henny.png")
        self.image = pygame.transform.scale(self.image,(75, 67))
        self.rect = self.image.get_rect()
        self.rect.centerx = x_cord        #Koordinaten des Spielers werden übergeben
        self.rect.bottom = y_cord

    def update(self):       #Bewegung der Bullets
        self.rect.y -= 30
        if self.rect.y <= 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self,  width = 50, height = 50, color = RED):
        super(Alien, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()






class AlienBullet(pygame.sprite.Sprite):
    def __init__(self,x_cord_alien, y_cord_alien, width = 7, height = 7, color = WHITE):
        super(AlienBullet, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_cord_alien
        self.rect.y = y_cord_alien

    def update(self):
        self.rect.y += 18
        #if self.rect.y >= BOARDHEIGHT:
         #   self.kill()

class SpaceInvaders():
    def __init__(self):
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((BOARDLENGTH, BOARDHEIGHT))
        self.clock = pygame.time.Clock()

        self.can_shoot = True
        self.fire_wait = 600
        self.alien_can_shoot = True
        self.alien_fire_wait = 200
        self.alien_direction = 1

        #Sprite Gruppen
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.alien_group = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()

        self.player = Player()      #Spielerfigur wird erstellt und zur Sprite-liste hunzugefügt
        self.player_group.add(self.player)
        self.all_sprites.add(self.player)

        self.player.set_player_position()  #Anfangsbildschirm des Spiels
        self.alien_spawn(20, BOARDLENGTH/8+1)

    def start_menü(self):
        while True:     #Startmenü
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.main_game_loop()
                pygame.display.flip()

                if (event.type == pygame.QUIT):
                    pygame.quit()


            pygame.display.set_caption("YSL Flying Larry Fighter")
            pygame.init()

            DISPLAYSURF = pygame.display.set_mode((BOARDLENGTH, BOARDHEIGHT))

            ysl = pygame.image.load("index.jpeg")
            self.DISPLAYSURF.blit(ysl, (BOARDLENGTH/2-112.5, BOARDHEIGHT - (BOARDHEIGHT / 2)))

            fontObj = pygame.font.Font('freesansbold.ttf', 20)
            textSurfaceObj1 = fontObj.render("Der Boi Know Plug wird von Andy Luwitz angegriffen", True, BLACK, WHITE)
            textRectObj1 = textSurfaceObj1.get_rect()
            textRectObj1.center = (BOARDLENGTH / 2, BOARDHEIGHT / 20 + 50)

            textSurfaceObj2 = fontObj.render("Switch dich mit der Enter Taste in den flying Space,", True, BLACK, WHITE)
            textRectObj2 = textSurfaceObj2.get_rect()
            textRectObj2.center = (BOARDLENGTH / 2, BOARDHEIGHT / 20 + 80)

            textSurfaceObj3 = fontObj.render("und defeate Andy mit der neuen high quality AK Draco Henny Edition!!!",
                                             True, BLACK, WHITE)
            textRectObj3 = textSurfaceObj3.get_rect()
            textRectObj3.center = (BOARDLENGTH / 2, BOARDHEIGHT / 20 + 110)

            DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
            DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
            DISPLAYSURF.blit(textSurfaceObj3, textRectObj3)

            pygame.display.update()





    def player_commands(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                exit()
        key = pygame.key.get_pressed()
        if key[K_RIGHT] and (self.player.rect.right < BOARDLENGTH):
            self.player.rect.x += 13
        elif key[K_LEFT] and (self.player.rect.left > 0):
            self.player.rect.x -= 13
        if key[K_SPACE] and self.can_shoot:
            self.bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
            self.bullet_group.add(self.bullet)
            self.all_sprites.add(self.bullet)
            self.can_shoot = False

    def waffe_nachladen(self):
        if not self.can_shoot and self.fire_wait <= 0:
            self.can_shoot = True
            self.fire_wait = 600
        self.fire_wait -= self.clock.tick(30)


    def alien_spawn(self, y_cord, x_cord):
        x = 0
        for i in range(8):
            self.alien = Alien()
            self.alien.rect.x = x_cord
            self.alien.rect.y = y_cord
            self.alien_group.add(self.alien)
            self.all_sprites.add(self.alien)
            x_cord += 75

    def alien_update(self):
        for alien in self.alien_group:

            if alien.rect.right >= BOARDLENGTH-(BOARDLENGTH/8):

                #self.alien_spawn(20, BOARDLENGTH/8+1)



                self.alien_direction = -1
                for a in self.alien_group:
                    a.rect.y += 75



            elif alien.rect.left <= BOARDLENGTH/8:
                self.alien_direction = 1
                for a in self.alien_group:
                    a.rect.y += 75

            alien.rect.x += 15 * self.alien_direction




    def alien_shoot(self):
        for alien in self.alien_group:
            chance = random.randint(0, 10000)
            if chance > 9950:
                alien_bullet = AlienBullet(alien.rect.x, alien.rect.y)
                self.alien_bullet_group.add(alien_bullet)
                self.all_sprites.add(alien_bullet)





    def collision_check(self):
        score = 0
        for bullet in self.bullet_group:

            alien_hit_list = pygame.sprite.spritecollide(bullet, self.alien_group, True)

            for alien in alien_hit_list:
                self.bullet_group.remove(bullet)
                self.all_sprites.remove(bullet)
                score += 1
                print(score)

        for alien_bullet in self.alien_bullet_group:

            player_hit_list = pygame.sprite.spritecollide(alien_bullet, self.player_group, True)

            for player in player_hit_list:
                print("you lose")





        #while True:#Startmenü

    def main_game_loop(self):

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()









            self.all_sprites.update()

            self.DISPLAYSURF.fill(BLACK)
            self.player_commands()
            self.waffe_nachladen()
            self.collision_check()
            self.alien_shoot()
            self.alien_update()

            self.all_sprites.draw(self.DISPLAYSURF)
            self.clock.tick(120)
            pygame.display.flip()


if __name__ == '__main__':
    SpaceInvaders().start_menü()