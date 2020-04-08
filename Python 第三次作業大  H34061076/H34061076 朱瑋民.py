#zombie kill
#this is a python game which you control a turret, and shoot the zombie to get more points
#the turret is in the middle of the screen and is stable, use this turret avoid to collide with zombie and shoot more zombie
# Add Game object for complete program
#import math, random
#from livewires import games, color
#games.init(screen_width = 640, screen_height = 480, fps = 50)
#construct a class Wrapper
    #define update
        #use if to keep the object in the screen
    #define die
        #self.destroy() to destroy itself
#construct a class Collider
    #define update
        # super(Collider, self).update()
        #if collide
            #destroy the turret or the zombie
    #define die
        #destroy the thing
        #add new explosion
#construct a class zombie
    #generate three kinds of zombie small medium big
    #load zombie images
    #initialize SPEED = 2 SPAWN = 3 POINTS = 30 total=0
    #define initial
        #add one more to total zombie
        # super(zombie, self).__init__(image = zombie.images[size], x = x, y = y,dx = random.choice([1, -1]) * zombie.SPEED * random.random()/size,
        #and dy = random.choice([1, -1]) * zombie.SPEED * random.random()/size) to define zombie speed and its direction
    #define die
        #zombie total-1
        #add game score with  self.game.score.value += int(zombie.POINTS / self.size)
        #if zombie is not small
            #add new zombie with smaller size of zombie
        #if all of the zombie are destroy
            #advance to next level
#construct a class turret
        #load turret image and sound
        #define ROTATION_STEP = 3 VELOCITY_STEP = .03 VELOCITY_MAX = 3 MISSILE_DELAY = 25
        #define initial super(turret, self).__init__(image = turret.image, x = x, y = y)
        #define update
            #if press left
                #rotate left
            #if press right
                #rotate right
            # if self.missile_wait > 0
                # if waiting until the turret can fire next, decrease wait
            # if press space
                #shoot the missile
                #add missile image
        #define die
            #game end
            #super(turret, self).die()
#construct a class Missile
    #load image and sound of missile
    #define BUFFER = 40 VELOCITY_FACTOR = 7  LIFETIME = 40
    #define initial
        #play the sound of missile
        #define angle = turret_angle * math.pi / 180  
        # calculate missile's starting position with
        #buffer_x = Missile.BUFFER * math.sin(angle)
        #buffer_y = Missile.BUFFER * -math.cos(angle)
        #x = turret_x + buffer_x
        #y = turret_y + buffer_y
        # calculate missile's velocity components with
        #dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        #dy = Missile.VELOCITY_FACTOR * -math.cos(angle)
        # create the missile
        #super(Missile, self).__init__(image = Missile.image,
                                      #x = x, y = y,
                                      #dx = dx, dy = dy)
        # define update
            #super(Missile, self).update()
        # if lifetime is up, destroy the missile
            #self.lifetime -= 1
            #if self.lifetime == 0:
                #self.destroy()
#construct a class explosion
        #load explosion sound and explosion image
        #define initial
            #add image and play sound if collide
#construct a class Game
    #define initial
        # set level
        #self.level = 0
        # load sound for level advance
        #self.sound = games.load_sound("level.wav")
        # create score
        #add score with games.screen.add(self.score)
        # create player's turret in the middle of the screen
        #games.screen.add(self.turret)
    #define play(self):
        # begin theme music and load sound
        # load and set background
        # advance to level 1 with self.advance()
        # start play with games.screen.mainloop()
    #define advance
        #Advance to the next game level
        #self.level += 1
        # amount of space around turret to preserve when creating zombie
        #define BUFFER = 150
        # create new zombie
        #use for loop for i in range(self.level):
            # calculate an x and y at least BUFFER distance from the turret
            # choose minimum distance along x-axis and y-axis
            #x_min = random.randrange(BUFFER)
            #y_min = BUFFER - x_min
            # choose distance along x-axis and y-axis based on minimum distance
            #x_distance = random.randrange(x_min, games.screen.width - x_min)
            #y_distance = random.randrange(y_min, games.screen.height - y_min)
            # calculate location based on distance
            #x = self.turret.x + x_distance
            #y = self.turret.y + y_distance
            # wrap around screen, if necessary
            #x %= games.screen.width
            #y %= games.screen.height
            # create the zombie with the big size
            #add new zombie
        # display level number
        #define level message with level_message = games.Message(value = "Level " + str(self.level),size = 40,color = color.yellow,
        # x = games.screen.width/2,y = games.screen.width/10,lifetime = 3 * games.screen.fps, is_collideable = False)
        #add level message
        # play new level sound (except at first level)
        #if self.level > 1:
            #self.sound.play()    
    #define end
        # show 'Game Over' for 5 seconds
        #define end_message = games.Message(value = "Game Over",size = 90, color = color.red,x = games.screen.width/2,y = games.screen.height/2,lifetime = 5 * games.screen.fps,
        #after_death = games.screen.quit,is_collideable = False)
        #add end message
    #define main
        # zombiekill = Game()
        #zombiekill.play()
#run main()
import math, random
from livewires import games, color

games.init(screen_width = 640, screen_height = 480, fps = 50)


class Wrapper(games.Sprite):
    """ A sprite that wraps around the screen. """
    def update(self):
        """ Wrap sprite around screen. """    
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        """ Destroy self. """
        self.destroy()


class Collider(Wrapper):
    """ A Wrapper that can collide with another object. """
    def update(self):
        """ Check for overlapping sprites. """
        super(Collider, self).update()
        
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()               

    def die(self):
        """ Destroy self and leave explosion behind. """
        new_explosion = Explosion(x = self.x, y = self.y)
        games.screen.add(new_explosion)
        self.destroy()


class zombie(Wrapper):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL  : games.load_image("zombie.bmp"),
              MEDIUM : games.load_image("zombie.bmp"),
              LARGE  : games.load_image("zombiebig.bmp") }

    SPEED = 2
    SPAWN = 2
    POINTS = 30
    
    total =  0
      
    def __init__(self, game, x, y, size):
        zombie.total += 1
        
        super(zombie, self).__init__(
            image = zombie.images[size],
            x = x, y = y,
            dx = random.choice([1, -1]) * zombie.SPEED * random.random()/size, 
            dy = random.choice([1, -1]) * zombie.SPEED * random.random()/size)

        self.game = game
        self.size = size

    def die(self):
        """ Destroy zombie. """
        zombie.total -= 1

        self.game.score.value += int(zombie.POINTS / self.size)
        self.game.score.right = games.screen.width - 10
        
        if self.size != zombie.SMALL:
            for i in range(zombie.SPAWN):
                new_zombie = zombie(game = self.game,
                                        x = self.x,
                                        y = self.y,
                                        size = self.size - 1)
                games.screen.add(new_zombie)

        # if all zombie are gone, advance to next level    
        if zombie.total == 0:
            self.game.advance()

        super(zombie, self).die()


class turret(Collider):
    """ The player's turret. """
    image = games.load_image("ship.bmp")
    sound = games.load_sound("thrust.wav")
    ROTATION_STEP = 3
    VELOCITY_STEP = .03
    VELOCITY_MAX = 3
    MISSILE_DELAY = 25

    def __init__(self, game, x, y):
        """ Initialize ship sprite. """
        super(turret, self).__init__(image = turret.image, x = x, y = y)
        self.game = game
        self.missile_wait = 0

    def update(self):
        """ Rotate, thrust and fire missiles based on keys pressed. """
        super(turret, self).update()
    
        # rotate based on left and right arrow keys
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= turret.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += turret.ROTATION_STEP

     # if waiting until the turret can fire next, decrease wait
        if self.missile_wait > 0:
            self.missile_wait -= 1
            
        # fire missile if spacebar pressed and missile wait is over   
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)        
            self.missile_wait = turret.MISSILE_DELAY

    def die(self):
        """ Destroy turret and end the game. """
        self.game.end()
        super(turret, self).die()


class Missile(Collider):
    """ A missile launched by the player's turret. """
    image = games.load_image("missile.bmp")
    sound = games.load_sound("missile.wav")
    BUFFER = 40
    VELOCITY_FACTOR = 7
    LIFETIME = 40

    def __init__(self, ship_x, ship_y, ship_angle):
        """ Initialize missile sprite. """
        Missile.sound.play()
        
        # convert to radians
        angle = ship_angle * math.pi / 180  

        # calculate missile's starting position 
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y

        # calculate missile's velocity components
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)

        # create the missile
        super(Missile, self).__init__(image = Missile.image,
                                      x = x, y = y,
                                      dx = dx, dy = dy)
        self.lifetime = Missile.LIFETIME

    def update(self):
        """ Move the missile. """
        super(Missile, self).update()

        # if lifetime is up, destroy the missile
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()


class Explosion(games.Animation):
    """ Explosion animation. """
    sound = games.load_sound("explosion.wav")
    images = ["explosion1.bmp",
              "explosion2.bmp",
              "explosion3.bmp",
              "explosion4.bmp",
              "explosion5.bmp",
              "explosion6.bmp",
              "explosion7.bmp",
              "explosion8.bmp",
              "explosion9.bmp"]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images = Explosion.images,
                                        x = x, y = y,
                                        repeat_interval = 4, n_repeats = 1,
                                        is_collideable = False)
        Explosion.sound.play()


class Game(object):
    """ The game itself. """
    def __init__(self):
        """ Initialize Game object. """
        # set level
        self.level = 0

        # load sound for level advance
        self.sound = games.load_sound("level.wav")

        # create score
        self.score = games.Text(value = 0,
                                size = 30,
                                color = color.white,
                                top = 5,
                                right = games.screen.width - 10,
                                is_collideable = False)
        games.screen.add(self.score)

        # create player's turret
        self.turret = turret(game = self, 
                         x = games.screen.width/2,
                         y = games.screen.height/2)
        games.screen.add(self.turret)

    def play(self):
        """ Play the game. """
        # begin theme music
        games.music.load("theme.mid")
        games.music.play(-1)

        # load and set background
        forest_image = games.load_image("forest.jpg")
        games.screen.background = forest_image

        # advance to level 1
        self.advance()

        # start play
        games.screen.mainloop()

    def advance(self):
        """ Advance to the next game level. """
        self.level += 1
        
        # amount of space around ship to preserve when creating zombie
        BUFFER = 150
     
        # create new zombie
        for i in range(self.level):
            # calculate an x and y at least BUFFER distance from the turret

            # choose minimum distance along x-axis and y-axis
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min

            # choose distance along x-axis and y-axis based on minimum distance
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(y_min, games.screen.height - y_min)

            # calculate location based on distance
            x = self.turret.x + x_distance
            y = self.turret.y + y_distance

            # wrap around screen, if necessary
            x %= games.screen.width
            y %= games.screen.height
       
            # create the zombie
            new_zombie = zombie(game = self,
                                    x = x, y = y,
                                    size = zombie.LARGE)
            games.screen.add(new_zombie)

        # display level number
        level_message = games.Message(value = "Level " + str(self.level),
                                      size = 40,
                                      color = color.yellow,
                                      x = games.screen.width/2,
                                      y = games.screen.width/10,
                                      lifetime = 3 * games.screen.fps,
                                      is_collideable = False)
        games.screen.add(level_message)

        # play new level sound (except at first level)
        if self.level > 1:
            self.sound.play()
            
    def end(self):
        """ End the game. """
        # show 'Game Over' for 5 seconds
        end_message = games.Message(value = "Game Over",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit,
                                    is_collideable = False)
        games.screen.add(end_message)


def main():
    zombiekill = Game()
    zombiekill.play()

# kick it off!
main()
