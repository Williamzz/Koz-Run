from __future__ import division
import pygame,math
import random
pygame.mixer.init(44100, -16,2,2048)


def Game():
    myX = 0
    myY = 0
    yDelta = 0
    prevY = 0
    fps = 60
    pygame.mixer.music.load("Images/starwars.wav")
    pygame.mixer.music.play(-1)
    # def getCenter():

    #   # import the necessary packages
    from collections import deque
    import numpy as np
    import argparse
    import imutils
    import cv2

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=20,
        help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    pts = deque(maxlen=args["buffer"])

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)

    # otherwise, grab a reference to the video file
    else:
        camera = cv2.VideoCapture(args["video"])

        # keep looping
        # while True:
            
        # cv2.destroyAllWindows()

    #getCenter()

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
     
    # Call this function so the Pygame library can initialize itself
    pygame.init()
    screen = pygame.display.set_mode([640, 480])
    # This sets the name of the window
    pygame.display.set_caption('Koz Run')
    clock = pygame.time.Clock()

    # Set positions of graphics # Load and set up graphics.
    background_position = [0, -1]
    background_image = pygame.image.load("Images/bg1.jpg").convert()
     
    # The road line
    class Obstacle(object):
        def __init__(self, time):
            self.time = time

    class Roadline(Obstacle):
        def draw(self, screen):
            time = (self.time + 1) % fps # start with zero
            startingY, endingY, timeFactor, maxHeight = 248, 520, time / fps, 40
            yLower = startingY + (endingY-startingY) * timeFactor
            height = maxHeight * timeFactor
            width = height / 6
            pointlist = [(325 - width,yLower - height),(325+width,yLower - height),
                (325 + width*1.5,yLower),(325 - width*1.5,yLower)]
            pygame.draw.polygon(screen, WHITE, pointlist)

    def drawAll(time,screen):
        time = (time + 1) % fps
        for i in range(4):
            modifier = i * fps//4
            Roadline(time + modifier).draw(screen)

    class Player(pygame.sprite.Sprite): #pygame.sprite.Sprite
        def __init__(self, x=200, y=200, action = "run"):
            # Call the parent's constructor
            #super().__init__()
            self.score = 0
            self.running = True
            self.action = action
            self.image = self.getImage()
            # center = self.rect.center()
            w,h = self.image.get_size()
            self.image = pygame.transform.scale(self.image, (65, 152)) 
            self.rect = self.image.get_rect()
            # self.rect.center = center
            self.position = (x, y)
            self.imageRun1 = pygame.image.load("Images/runner1.png").convert_alpha()
            self.imageRun2 = pygame.image.load("Images/runner2.png").convert_alpha()

        def getImage(self):
            if self.action == "run":
                return pygame.image.load("Images/runner1.png").convert_alpha()
            elif self.action == "jump":
                self.image = pygame.image.load("Images/jumper.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (65, 152)) 
                return self.image
            # elif self.action == "slide":
            #     return pygame.image.load("Images/slider.png").convert_alpha()

        def flipPlayer(self, val):
            if val == True:
                self.image = self.imageRun1
            else:
                self.image = self.imageRun2
            self.image = pygame.transform.scale(self.image, (65, 152))
            return self.image


    class Obstruct(pygame.sprite.Sprite):
        def __init__(self,x,y):
            # Load and set up graphics.
            Obstacleimagelist=[]
            Rockimage=pygame.image.load("Images/Rock.png/").convert_alpha()
            treeimage=pygame.image.load("Images/tree.png/").convert_alpha()
            treetrunk=pygame.image.load("Images/treetrunk.png/").convert_alpha()
            Obstacleimagelist.append(Rockimage)
            Obstacleimagelist.append(treeimage)
            Obstacleimagelist.append(treetrunk)

            self.x=x
            self.y=y
            self.w=0
            self.h=0
            self.image=random.choice(Obstacleimagelist)
            w,h = self.image.get_size()
            self.size=( int(w), int(h))
            self.image = pygame.transform.scale(self.image, self.size)    
            self.rect = self.image.get_rect()
            self.position=(int(x),int(y))
            list1 = [0.1*x for x in range(-20,21)]
            self.direction=random.choice(list1)

            self.animate = False
            self.animation_speed = 3

        def getposition(self):
            return self.position

        def update(self):
            x=self.x
            y=self.y
            self.x+=1*self.direction
            self.y+=2
            self.position=(x,y)
            if self.animate:
                if self.animation_target_width > self.rect.width or self.animation_target_height > self.rect.height:
                    center_location = self.rect.center
                    self.image = pygame.transform.scale(self.original_image, (self.rect.width+self.animation_speed, self.rect.height+self.animation_speed))
                    # self.rect = self.image.get_rect()
                    self.rect.center = center_location


        def scale_animation(self, new_width, new_height):
            self.animate = True
            self.animation_target_width = new_width
            self.animation_target_height = new_height
            self.original_image = self.image



    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.w = 0
            self.h = 0

            self.image = pygame.image.load("Images/kozFace.png").convert_alpha()
            w,h = self.image.get_size()
            self.size=( int(w)//12, int(h)//12)

            self.image = pygame.transform.scale(self.image, self.size) 
            self.rect = self.image.get_rect()
            self.position=(x,y)
            self.direction=random.randint(-3,3)

            self.animate = False
            self.animation_speed = 3




        def getcoinposition(self):
            return self.position

        def updatecoin(self):
            x=self.x
            y=self.y
            self.x+=1*self.direction
            self.y+=4
            self.position=(x,y)
            if self.animate:
                if self.animation_target_width > self.rect.width or self.animation_target_height > self.rect.height:
                    center_location = self.rect.center
                    self.image = pygame.transform.scale(self.original_image, (self.rect.width+self.animation_speed, self.rect.height+self.animation_speed))
                    # self.rect = self.image.get_rect()
                    self.rect.center = center_location

        def scale_animation(self, new_width, new_height):
            self.animate = True
            self.animation_target_width = new_width
            self.animation_target_height = new_height
            self.original_image = self.image



    def collisiondetection(x1,y1,x2,y2):
        if abs(y1-y2)<=80 and abs(x1-x2)<=70 and y2>=350:
            return True
        else: return False



    jumpTime = 0
    time = 0
    done = False
    val = True
    player = Player(640-int(myX),320)
    Obstructlist=[]
    Coinlist = []





    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        # grab the current frame
        (grabbed, frame) = camera.read()

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        # if args.get("video") and not grabbed:
        #   break

        # resize the frame, blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, width=600)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)# construct a mask for the color "green", then perform
        mask = cv2.erode(mask, None, iterations=2)# a series of dilations and erosions to remove any small
        mask = cv2.dilate(mask, None, iterations=2)# blobs left in the mask

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            myX = x
            myY = y
            yDelta = int(prevY-myY)
            prevY = y
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 50:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the points queue
        pts.appendleft(center)
        screen.blit(background_image, background_position)

        # loop over the set of tracked points
        for i in xrange(1, len(pts)):
            # if either of the tracked points are None, ignore them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        # key = cv2.waitKey(33) & 0xFF
                # Draw image for pygame
        drawAll(time,screen)


        # Copy image to screen:
        time = (time + 1) % 60

        if time == 0:
            obstruct=Obstruct(310,248)
            Obstructlist.append(obstruct)
        if time == 10:
            num = random.randint(1,3)
            if num == 2:    
                coin1 = Coin(310,200)
                coin2 = Coin(310,248)
                coin2.direction = coin1.direction
                Coinlist.append(coin1)
                Coinlist.append(coin2)
            elif num == 1:
                coin1 = Coin(310,200)
                Coinlist.append(coin1)
            else:
                coin1 = Coin(310,200)
                coin3 = Coin(310,248)
                coin2 = Coin(310,224)
                coin2.direction = coin1.direction 
                coin3.direction = coin1.direction
                Coinlist.append(coin1)
                Coinlist.append(coin2)
                Coinlist.append(coin3)

        screen.blit(background_image, background_position)
        for i in range(4):
            modifier = i *15
            Roadline(time + modifier).draw(screen)

        

        for obstruct in Obstructlist:
            # obstruct.changeposition()
            # obstruct.changesize()
            obstruct.scale_animation(obstruct.rect.width,player.rect.height)
            screen.blit(obstruct.image, obstruct.position)
            # if pygame.sprite.spritecollide(player,obstruct):
            #     print ("Game Over")

            # (x1,y1)=player.position
            (x2,y2)=(obstruct.getposition())
         
            if y2>=450: Obstructlist.remove(obstruct)
            # print("x1,y1",(kozX,kozY))
            # print("x2,y2",(x2,y2))
            # if collisiondetection(x1,y1,x2,y2):
            #     print("gg")
            # if pygame.sprite.collide_rect(player,obstruct):
            #     # done=True
            #     print("Game Over")
            obstruct.update()


        for coin in Coinlist:
            coin.scale_animation(coin.rect.width,player.rect.height)
            coin.updatecoin()
            screen.blit(coin.image, coin.position)
            (c1,c2)=coin.getcoinposition()
            if c2>=450: Coinlist.remove(coin)

        #player 
        kozX = 640-int(myX)
        kozY = int(myY) if player.action == "jump" else 320
        for obstruct in Obstructlist:
            (x1,y1)=(kozX,kozY)
            (x2,y2)=(obstruct.getposition())

            if collisiondetection(x1,y1,x2,y2):
                effect = pygame.mixer.Sound('Images/Screaming.wav')
                effect.play()
                player.score -= 1
                Obstructlist.remove(obstruct)
        for coin in Coinlist:
            (x1,y1)=(kozX,kozY)
            (x2,y2)=(coin.getcoinposition())

            if collisiondetection(x1,y1,x2,y2):
                player.score+=1
                effect = pygame.mixer.Sound('Images/coin.wav')
                effect.play()
                Coinlist.remove(coin)


        # print(kozX,kozY)
        player.position = (kozX, kozY)
        if yDelta > 35:
            player.action = "jump"
            player.position = (640-int(myX), int(myY))
            jumpTime = 0
        # elif yDelta < -60:
        #     player.action= "slide"
        #     player.position = (640-int(myX), 320)
        #     jumpTime = 0
        elif jumpTime > 4:
            player.action = "run"

        if player.action == "run":
            if time % 3 == 0:
                val = True if val == False else False
                player.flipPlayer(val)
            screen.blit(player.image, player.position)
        elif player.action == "jump":
            jumpTime += 1
            player.image = player.getImage()
            screen.blit(player.image, player.position)
        # elif player.action == "slide":
        #     jumpTime += 1
        #     player.image = player.getImage()
        #     screen.blit(player.image, player.position)
        
        font = pygame.font.Font(None, 35)
        text = font.render("Score: %d * 112"%player.score, 1, (0,0,0))
        textpos = (50,50)
        screen.blit(text, textpos)


        pygame.display.flip()
        clock.tick(fps)
        
    pygame.quit()

Game()




