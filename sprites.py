# coding=utf-8
'''
     Author: David Su
     
     Date: May 2, 2012
     
     Description: Metal Python sprites
'''    

import pygame,os,math,random
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((640,480)) 

class Background(pygame.sprite.Sprite):
    '''scrolling background sprite'''
    def __init__(self,player,level=0):
        '''initializer method with player and level number as parameters'''
        pygame.sprite.Sprite.__init__(self)              
        
        #loads image and rect        
        self.image=pygame.image.load('images\\'+('bkgd.png','bossbkgd2.png')[level]).convert()
        self.rect=self.image.get_rect()
        self.rect.left=0
        self.rect.bottom=480  
        #adjusts the screen centering 
        self.__adjustment=100+player.rect.width      
        
    def update(self,player):
        '''update method with the player as a parameter'''
        #handles the adjustment
        if player.get_direction():
            if self.__adjustment<=150:                
                self.__adjustment+=5  
            self.__player_side=player.rect.right
        else:
            if self.__adjustment>=-150:                
                self.__adjustment-=5 
            self.__player_side=player.rect.left
            
        #calculates position of the background    
        self.rect.left=320-self.__player_side+self.__adjustment
        #stops scrolling once it reaches either side of the screen
        if self.rect.left>0:
            self.rect.left=0
        elif self.rect.right<640:
            self.rect.right=640       
            
class Player(pygame.sprite.Sprite):
    '''player sprite'''
    def __init__(self,prev_player=None):
        '''initializer method with the player from the previous level as a parameter, if applicable, so that attributes can be inherited'''
        pygame.sprite.Sprite.__init__(self)       
        
        #loads all animations into nested lists
        self.__sprites=[[[[pygame.image.load('images\\player\\'+str(orientation)+'\\'+str(weapon)+'\\'+str(animation)+'\\'+str(frame)+'.png').convert_alpha() for frame in range(len(os.listdir('images\\player\\'+str(orientation)+'\\'+str(weapon)+'\\'+str(animation))))] for animation in range(7)] for weapon in range(2)] for orientation in range(2)]  
            
        #initializes animation           
        self.__orientation=0        
        self.__animation=0
        self.__frame=0
        self.__speed=15
        
        if prev_player:            
            self.__weapon=prev_player.get_weapon()
        else:
            self.__weapon=1
            
        #creates image and rect attributes
        self.image=self.__sprites[self.__orientation][self.__weapon][self.__animation][self.__frame]
        self.rect=self.image.get_rect()
        
        if prev_player:
            self.rect.bottomleft=(50,432)
        else:
            self.rect.midtop=(320,0)
        
        #previous height, used when landing on platforms
        self.__prev_bottom=self.rect.bottom        
        
        #initializes movement
        self.__vx=0
        self.__vy=0        
        self.__falling=not bool(prev_player)           
        self.__shooting=False
        
        #delay for shooting pistol
        self.__shotdelay=0
        
        #used for scoreboard
        if prev_player:
            self.__health=prev_player.get_health()
            self.__ammo=prev_player.get_ammo()
            self.__grenades=prev_player.get_grenades()
        else:
            self.__health=200
            self.__ammo=100
            self.__grenades=10
        
        self.__dead=False        
        self.__hurt=0
        
        #sound
        self.__mg_sound=pygame.mixer.Sound('sounds\\mg.wav')
        self.__pistol_sound=pygame.mixer.Sound('sounds\\pistol.wav')
        self.__death=pygame.mixer.Sound('sounds\\marco.wav')       
        
    def update(self,*args):
        '''update method'''
        #changes weapon to pistol once the mg is out of ammo
        if self.__ammo<=0:
            self.__weapon=0
        #kills player once health is 0
        if self.__health<=0 and self.__animation!=6:
            self.__death.play()
            self.__animation=6
            self.__weapon=0
            self.__frame=0
            
        #previous position for landing on platforms                
        self.__prev_bottom=self.rect.bottom 
            
        #falling
        if self.__falling:            
            self.__vy+=1.1
            self.rect.bottom+=self.__vy        
            
        #death animation
        if self.__animation==6:   
            #changes picture every 3 frames    
            if self.__frame<len(self.__sprites[self.__orientation][self.__weapon][self.__animation])*3:
                self.image=self.__sprites[self.__orientation][self.__weapon][self.__animation][self.__frame/3]
            
            #recenters image
            if self.__orientation:
                self.__prev=self.rect.bottomright
                self.rect=self.image.get_rect()
                self.rect.bottomright=self.__prev
            else:
                self.__prev=self.rect.bottomleft
                self.rect=self.image.get_rect()
                self.rect.bottomleft=self.__prev
                
            self.__frame+=1
            if self.__frame>=100:
                self.__dead=True
                
        #when alive
        else:
            #horizontal movement
            self.rect.left+=self.__vx*8
            
            #changes orientation 
            if self.__vx>0:
                self.__orientation=0
            elif self.__vx<0:
                self.__orientation=1
                
            
            
            #prevents the player from moving off the sides of the level
            if self.rect.left<=0:
                self.rect.left=0                       
                
            #animation
            #shooting
            if self.__shooting:
                if self.__animation not in [3,4,5]:
                    self.__frame=0
                if not self.__weapon:
                    self.__speed=3
                else:
                    self.__speed=1
                #while jumping
                if self.__vy:
                    self.__animation=5
                #while running
                elif self.__vx:
                    self.__animation=4
                #while standing still
                else:
                    self.__animation=3                 
            #still
            elif self.__animation and not self.__vx and not self.__vy:            
                self.__frame=0
                self.__speed=15
                self.__animation=0            
            #running
            elif self.__animation!=1 and self.__vx and not self.__vy:
                self.__frame=0
                self.__speed=2
                self.__animation=1
            #jumping
            elif self.__animation!=2 and self.__vy:
                self.__frame=0
                self.__speed=1
                self.__animation=2
            
            #updates animation
            self.image=self.__sprites[self.__orientation][self.__weapon][self.__animation][self.__frame/self.__speed].copy()
            
            #flashes red when hurt every 5 frames
            if self.__hurt>0:
                if self.__hurt%5==0:
                    self.image.fill((200,0,0), special_flags=pygame.BLEND_RGB_MULT)
                self.__hurt-=1
            
            #recenters image
            if self.__orientation:
                self.__prev=self.rect.bottomright
                self.rect=self.image.get_rect()
                self.rect.bottomright=self.__prev
            else:
                self.__prev=self.rect.bottomleft
                self.rect=self.image.get_rect()
                self.rect.bottomleft=self.__prev     
            
            self.__frame+=1
            #cycles frame count 
            if self.__frame>=len(self.__sprites[self.__orientation][self.__weapon][self.__animation])*self.__speed:
                self.__frame=0
            #resets horizontal velocity          
            self.__vx=0
            #stops shooting animation from looping
            if self.__shooting and self.__frame==0:
                self.__shooting=False               
                
    def pickup(self):
        '''called when the user picks up ammo'''
        self.__weapon=1
        self.__ammo+=100
            
    def jump(self):
        '''makes player jump'''
        if not self.__falling and self.__animation!=6:
            self.rect.top-=1
            self.__vy=-17  
            self.__falling=True
            
    def move(self,vx):
        '''moves player vx pixels'''
        self.__vx=vx                
        
    def collide_wall(self,wall,level=0):
        '''stops player when hitting a wall'''
        if level:
            self.rect.right=wall.rect.left
        else:
            self.rect.left=wall.rect.right
        self.__vx=0
        
    def fall(self):
        '''called when the player is not colliding with the ground'''
        self.__falling=True
    
    def land(self,platform):
        '''called when landing on a platform'''
        #checks if the player walked off the edge and touches another higher platform
        if not self.__falling and self.rect.bottom>platform+1:             
            self.fall()         
        #checks if player lands on top of the platform
        elif self.__prev_bottom<=platform:               
            self.rect.bottom=platform+1
            self.__vy=0
            self.__falling=False            
        
    def shoot(self):
        '''starts shooting, returns either true or the bullet number, depending on the current weapon'''
        self.__shooting=True  
        #if using a pistol, returns True when the pistol is shooting    
        if not self.__weapon and self.__frame==1:
            self.__pistol_sound.play()
            return True
        #if using a mg, returns the bullet number used in animating the bullet, and decrements ammo count
        elif self.__weapon==1:
            self.__ammo-=1            
            self.__mg_sound.play()
            return self.__frame/self.__speed            
            
    def throw_grenade(self):
        '''reduces grenade count'''
        self.__grenades-=1
        
    def get_health(self):
        '''returns the amount of health'''
        return self.__health
    
    def hurt(self,damage):
        '''lowers health and starts flashing'''
        if not self.__hurt:
            self.__health-=damage
            self.__hurt=30
        
    def get_ammo(self):
        '''returns the ammount of ammo left'''
        if not self.__weapon:
            return u'∞'
        else:
            return self.__ammo
    
    def get_grenades(self):
        '''returns the amount of grenades left'''
        return self.__grenades        
        
    def get_direction(self):
        '''returns the direction the player is facing'''
        return self.__orientation
    
    def get_weapon(self):
        '''returns the current weapon'''
        return self.__weapon
    
    def get_dying(self):
        '''returns whether the player is in the death animation'''
        if self.__dead:
            return 2
        return self.__animation==6
    
    def respawn(self,tank):
        '''respawns player once the tank is destoryed'''
        if not self.alive():
            #repositions player
            self.rect.midbottom=tank.rect.midtop
            #resets attributes
            self.__orientation=0       
            self.__prev_bottom=self.rect.bottom     
            self.__vx=0
            self.__vy=-10
            self.__falling=True
            self.__shooting=False
            self.__shotdelay=0 
        
class MGBullet(pygame.sprite.Sprite):
    '''machine gun bullet class'''
    def __init__(self,bkgd,player,shotnum):
        '''initializer method with the background, player, and shot number as parameters'''
        pygame.sprite.Sprite.__init__(self)  
        
        #loads all required sprites, shot number determines the muzzle flash image
        self.__sprites=(pygame.image.load('images\\bullet\\'+str(player.get_direction())+'\\1\\'+str(shotnum)+'.png').convert_alpha(),pygame.image.load('images\\bullet\\bullet0.png').convert_alpha())
        
        #loads image and rect
        self.image=self.__sprites[0]
        self.rect=self.image.get_rect()        
        self.rect.centery=player.rect.centery
        #decides the direction of the bullet, makes speed random
        if player.get_direction():
            self.rect.right=player.rect.left+20
            self.__vx=-20+random.randint(-1,1)
        else:
            self.rect.left=player.rect.right-20
            self.__vx=20+random.randint(-1,1)
        #initializes attributes
        self.__player=player
        self.__frame=0
        self.__bkgd=bkgd
        self.__vy=random.randint(-1,1)
    
    def update(self,*args):
        #first frame is muzzle flash, all subsequent frames change to the bullet
        if self.__frame==1:   
            self.__prev=self.rect.center
            self.image=self.__sprites[1]
            self.rect=self.image.get_rect()
            self.rect.center=self.__prev            
        
        #moves bullet
        self.rect.left+=self.__vx
        self.rect.top+=self.__vy        
        
        #check if the bullet is outside the screen        
        if self.rect.right<-self.__bkgd.rect.left or self.rect.left>-self.__bkgd.rect.left+640 or self.rect.top<0 or self.rect.bottom>480:
            self.kill()
            
        self.__frame+=1
            
class PistolBullet(pygame.sprite.Sprite):
    '''class for pistol bullet'''
    def __init__(self,bkgd,player):
        '''initializer method with the background and player as parameters'''
        pygame.sprite.Sprite.__init__(self)  
        #loads all required sprites
        self.__sprites=[pygame.image.load('images\\bullet\\'+str(player.get_direction())+'\\0\\'+str(frame)+'.png').convert_alpha() for frame in range(2)]+[pygame.image.load('images\\bullet\\bullet0.png').convert_alpha()]        
        #loads image and rect
        self.image=self.__sprites[0]
        self.rect=self.image.get_rect()
        #sets x and y velocity
        self.rect.centery=player.rect.top+24
        if player.get_direction():
            self.rect.right=player.rect.left
            self.__vx=-20
        else:
            self.rect.left=player.rect.right
            self.__vx=20
        self.__player=player
        self.__frame=0
        self.__bkgd=bkgd
        
    def update(self,*args):
        '''update method'''
        #first 2 frames are muzzle flash, third frame becomes the bullet
        if self.__frame in (1,2):
            self.__prev=self.rect.center
            self.image=self.__sprites[self.__frame]
            self.rect=self.image.get_rect()
            self.rect.center=self.__prev        
        
        #bullet starts moving in third frame
        if self.__frame>1:
            self.rect.left+=self.__vx
        
        #checks if bullet is out of the screen
        if self.rect.right<-self.__bkgd.rect.left or self.rect.left>-self.__bkgd.rect.left+640 or self.rect.top<0 or self.rect.bottom>480:
            self.kill()
            
        self.__frame+=1
        
class Platform(pygame.sprite.Sprite):
    '''platform sprite'''
    def __init__(self,dimension):
        '''platform sprite kept for collision detection only'''
        pygame.sprite.Sprite.__init__(self)      
        self.rect=pygame.Rect(*dimension)       
    
class Enemy(pygame.sprite.Sprite):
    '''enemy class'''
    __sprites=[[[pygame.image.load('images\\enemy\\'+str(orientation)+'\\'+str(animation)+'\\'+str(frame)+'.png').convert_alpha() for frame in range(len(os.listdir('images\\enemy\\'+str(orientation)+'\\'+str(animation))))] for animation in range(3)] for orientation in range(2)]
    #sound
    __shoot=pygame.mixer.Sound('sounds\\enemy.wav')
    __death=[pygame.mixer.Sound('sounds\\soldier'+str(i)+'.wav') for i in range(1,6)]
    
    def __init__(self,midbottom):
        '''initializer that accepts the midbottom coordinates as a parameter'''
        pygame.sprite.Sprite.__init__(self) 
        
        #initializes animation  
        self.__orientation=1
        self.__animation=0
        self.__frame=0
        
        #loads image and rect
        self.image=Enemy.__sprites[self.__orientation][self.__animation][self.__frame]
        self.rect=self.image.get_rect()
        self.rect.midbottom=midbottom
        self.__shotcounter=0
        self.__speed=15        
        
    def get_shooting(self):
        '''returns True when the enemy is shooting'''
        if self.__animation==1 and self.__frame==9:
            Enemy.__shoot.play()
            return True
    
    def get_direction(self):
        '''returns the direction'''
        return self.__orientation
    
    def die(self):
        '''starts death animation'''
        if self.__animation!=2:
            self.__animation=2
            self.__frame=0
            Enemy.__death[random.randint(0,4)].play()
            
    def get_dying(self):
        '''returns True when the enemy is in its death animation'''
        return self.__animation==2        
        
    def update(self,player):
        '''update method that receives the player as a parameter'''
        self.__player=player
        
        #death animation
        if self.__animation==2:
            self.__prev=self.rect.midbottom             
            #updates image and rect
            self.image=Enemy.__sprites[self.__orientation][self.__animation][self.__frame/3]            
            self.rect=self.image.get_rect()
            self.rect.midbottom=self.__prev
            self.__frame+=1
            
            #removes enemy from all groups once the death animation is over
            if self.__frame>=len(self.__sprites[self.__orientation][self.__animation])*3:                
                self.kill()             
                
        #while alive        
        else:        
            #changes orientation
            if self.__player.rect.centerx<self.rect.centerx:
                self.__orientation=1
            elif self.__player.rect.centerx>self.rect.centerx:
                self.__orientation=0
            #starts shooting 
            if self.__shotcounter>=75 and self.rect.left-480<=self.__player.rect.centerx<+self.rect.right+480:
                self.__shotcounter=0
                self.__animation=1
                self.__frame=0
                self.__speed=3
            #stands still
            elif self.__shotcounter==15:
                self.__animation=0
                self.__frame=0
                self.__speed=15                
            
            self.__prev=self.rect.midbottom           
            #updates image
            self.image=Enemy.__sprites[self.__orientation][self.__animation][self.__frame/self.__speed]
            self.rect=self.image.get_rect()
            self.rect.midbottom=self.__prev            
            
            self.__frame+=1
            if self.__frame>=len(Enemy.__sprites[self.__orientation][self.__animation])*self.__speed:
                self.__frame=0            
            
            self.__shotcounter+=1
        
class EnemyBullet(pygame.sprite.Sprite):
    '''enemy bullet class'''
    def __init__(self,enemy,player):
        '''initializer method with the enemy and player as parameters'''
        pygame.sprite.Sprite.__init__(self)   
        
        #loads all required sprites
        self.__sprites=[pygame.image.load('images\\bullet\\'+str(enemy.get_direction())+'\\0\\'+str(frame)+'.png').convert_alpha() for frame in range(2)]+[pygame.image.load('images\\bullet\\bullet1.png').convert_alpha()]
        
        #loads image and rect
        self.image=self.__sprites[0]
        self.rect=self.image.get_rect()        
        self.rect.centery=enemy.rect.top+24
        
        #calculates slope
        try:
            self.__slope=float(enemy.rect.centery-player.rect.centery)/(enemy.rect.centerx-player.rect.centerx)           
        except ZeroDivisionError:
            self.__slope=100000000
        
        #calculates x and y velocities
        if enemy.get_direction():
            self.rect.right=enemy.rect.left   
            self.__vx=-(20/(self.__slope**2+1))**0.5
        else:
            self.rect.left=enemy.rect.right
            self.__vx=(20/(self.__slope**2+1))**0.5      
        
        self.__vy=self.__slope*self.__vx         
        
        self.__frame=0
        
        
    def update(self,*args):
        '''update method'''
        #changes image in second and third frames
        if self.__frame in (1,2):
            self.__prev=self.rect.center
            self.image=self.__sprites[self.__frame]
            self.rect=self.image.get_rect()
            self.rect.center=self.__prev        
        #starts moving the sprite after the first 2 frames, which are muzzle flashes    
        if self.__frame>1:
            self.rect.left+=self.__vx
            self.rect.top+=self.__vy
    
        #kills the bullet once it is outside the background
        if self.rect.right<=0 or self.rect.left>=3945 or self.rect.top<0 or self.rect.bottom>480:
            self.kill()
            
        self.__frame+=1
        
class Grenade(pygame.sprite.Sprite):
    '''grenade class'''    
    __explosion=[pygame.image.load('images\\grenade\\'+str(frame)+'.png').convert_alpha() for frame in range(21)]
    __grenade=pygame.image.load('images\\grenade\\grenade.png').convert_alpha() 
    #sound
    __explode=pygame.mixer.Sound('sounds\\explosion.wav')
    def __init__(self,player):
        '''initializer method with the player as the parameter'''
        pygame.sprite.Sprite.__init__(self)         
        
        #initializes angle
        self.__angle=[-45,45][player.get_direction()]        
        #rotates the image and get the rect
        self.image=pygame.transform.rotate(Grenade.__grenade, self.__angle)
        self.rect=self.image.get_rect()
        
        #sets starting location and velocity
        if player.get_direction():
            self.rect.bottomright=player.rect.midtop
            self.__vx=-15            
        else:
            self.rect.bottomleft=player.rect.midtop
            self.__vx=15     
        
        self.__vy=-10      
        self.__explode=False
        self.__frame=0
        
    def explode(self):
        '''starts explosion animation'''
        self.__explode=True
        Grenade.__explode.play()
        
    def update(self,*args):
        '''update method'''
        #while exploding
        if self.__explode: 
            self.__prev=self.rect.midbottom
            self.image=Grenade.__explosion[self.__frame]
            self.rect=self.image.get_rect()
            self.rect.midbottom=self.__prev           
            
            self.__frame+=1
            #kills sprite once explosion is over
            if self.__frame>=21:
                self.kill()
        #in the air     
        else:
            #rotates image
            self.image=pygame.transform.rotate(Grenade.__grenade, self.__angle)            
            if self.__angle<0:
                self.__angle-=5
            else:
                self.__angle+=5
            #moves sprite horizontally
            self.rect.left+=self.__vx            
            #gravity
            self.__vy+=1.1
            self.rect.top+=self.__vy
                
                      
            
class TankShell(pygame.sprite.Sprite):
    '''tank shell sprite'''
    __explosion=[pygame.image.load('images\\grenade\\'+str(frame)+'.png').convert_alpha() for frame in range(21)]
    __shell=pygame.image.load('images\\grenade\\shell.png').convert_alpha() 
    #sound
    __explode=pygame.mixer.Sound('sounds\\explosion.wav')
    def __init__(self,tank=None):
        '''initializer method with the tank as an optional parameter. if not present, assumes shell is fired from the boss'''
        pygame.sprite.Sprite.__init__(self)   
        
        #sets key attributes
        if bool(tank):                        
            self.__angle=0             
            self.__vx=20
            self.__vy=0
            self.__da=-5 #change in angle
            self.__g=1.1
        else:
            self.__angle=135            
            self.__vx=random.randint(-20,-1)
            self.__vy=-5
            self.__da=2
            self.__g=0.4
            
        #rotates the image and get the rect
        self.image=pygame.transform.rotate(TankShell.__shell, self.__angle)
        self.rect=self.image.get_rect()       
        if bool(tank):
            self.rect.midleft=(tank.rect.left+162,tank.rect.top+50)
        else:
            self.rect.midright=(870,290)
            
        self.__explode=False
        self.__frame=0
        
        
    def explode(self):
        '''starts explosion animation'''
        if not self.__explode:
            self.__explode=True
            TankShell.__explode.play()
        
    def update(self,*args):
        '''update method'''
        #while exploding
        if self.__explode: 
            self.__prev=self.rect.midbottom
            self.image=TankShell.__explosion[self.__frame]
            self.rect=self.image.get_rect()
            self.rect.midbottom=self.__prev            
            
            self.__frame+=1
            #kills sprite once animation is over
            if self.__frame>=21:
                self.kill()
        #while in the air   
        else:
            #rotates image
            self.image=pygame.transform.rotate(TankShell.__shell, self.__angle)               
            self.__angle+=self.__da      
            #moves image horizontally
            self.rect.left+=self.__vx
            #gravity
            self.__vy+=self.__g
            self.rect.top+=self.__vy

class Tank(pygame.sprite.Sprite):
    '''tank sprite'''
    def __init__(self,prev_tank=None):
        '''intializer method'''
        pygame.sprite.Sprite.__init__(self)
        #loads all animations
        self.__sprites=[[pygame.image.load('images\\tank\\'+str(animation)+'\\'+str(frame)+'.png').convert_alpha() for frame in range(len(os.listdir('images\\tank\\'+str(animation))))] for animation in range(5)]         
        #loads mg turret image
        self.__mg=pygame.image.load('images\\tank\\turret.png').convert_alpha() 
        
        #sets initial animation
        self.__animation=0
        self.__frame=0
        
        #loads image and rect
        self.image=self.__sprites[self.__animation][self.__frame].copy()
        self.rect=self.image.get_rect()
        if prev_tank:
            self.rect.bottomleft=(50,432)
        else:
            self.rect.bottomleft=(1450,450)
        
        #sets attributes        
        self.__prev_bottom=self.rect.bottom        
        self.__vx=0
        self.__vy=0
        self.__falling=False
        self.__shooting_cannon=False
        self.__shooting_mg=False
        self.__speed=15
        self.__angle=0  
        if prev_tank:
            self.__shells=int(prev_tank.get_grenades())
            self.__health=int(prev_tank.get_health())
        else:
            self.__shells=10
            self.__health=200
        self.__hurt=0
        
        #sound
        self.__cannon=pygame.mixer.Sound('sounds\\cannon.wav')
        self.__mg_sound=pygame.mixer.Sound('sounds\\mg.wav')
        self.__explode=pygame.mixer.Sound('sounds\\explosion.wav')
        
    def get_grenades(self):
        '''returns the number of tank shells left'''
        return self.__shells
    
    def get_ammo(self):
        '''returns the ammount of ammo left'''
        return u'∞'
    
    def get_health(self):
        '''return the amount of health left'''
        return self.__health
    
    def hurt(self,damage):
        '''decrements health and makes image flash red'''
        if not self.__hurt:
            self.__health-=damage/2
            self.__hurt=30    
        
    def jump(self):
        '''starts jumping'''
        if not self.__falling and self.__animation!=3:
            self.rect.top-=1
            self.__vy=-17  
            self.__falling=True
            
    def move(self,vx):
        '''moves the tank horizontally'''
        self.__vx=vx           
        
    def collide_wall(self,wall,level=0):
        '''handles collision with the wall'''
        if level:
            self.rect.right=wall.rect.left
        else:
            self.rect.left=wall.rect.right
        self.__vx=0
        
    def fall(self):
        '''called when the tank is not on any platform'''
        self.__falling=True
        
    def get_angle(self):
        '''returns the angle of the machine gun turret'''
        return self.__angle
    
    def land(self,platform):
        '''lands the tank on a platform'''
        #checks if the tank drove off a platform and touched a higher platform
        if not self.__falling and self.rect.bottom>platform+1:            
            self.__falling=True
        #checks if the tank was completely above the platform at some point    
        elif self.__prev_bottom<=platform:
            self.rect.bottom=platform+1
            self.__vy=0
            self.__falling=False
        
    def shoot_cannon(self):    
        '''initiates shooting animation'''
        if self.__shells>0:
            self.__shooting_cannon=True  
            self.__shells-=1
            self.__cannon.play()
            return True
            
    def shoot_mg(self):
        '''plays the shooting sound'''        
        self.__mg_sound.play()
        
    def die(self):
        '''called when the player exited the tank'''
        if self.__animation!=4:
            self.__animation=4
            self.__frame=0
            self.__explode.play()
            
    def rotate(self,angle):
        '''rotates the turret'''
        self.__angle+=angle
          
    def get_direction(self):
        '''returns the direction the tank is facing'''
        return 0    
    
    def get_dying(self):
        '''returns whether the tank is in its death animation'''
        return self.__animation==4
        
    def get_turret(self):
        '''returns the coordinates of the center of the turret'''
        return self.__temp_rect.centerx+self.rect.left,self.__temp_rect.centery+self.rect.top
    
    def update(self,*args):
        '''update method'''
        #runs the die() method once the tank is out of health
        if self.__health<=0 and self.__animation!=4:
            self.die()
            
        #updates previous bottom    
        self.__prev_bottom=self.rect.bottom
        
        #falling
        if self.__falling:
            self.__vy+=1.1
            self.rect.bottom+=self.__vy
                
        #death animation
        if self.__animation==4:               
            #updates image    
            if self.__frame<len(self.__sprites[self.__animation])*3:
                self.image=self.__sprites[self.__animation][self.__frame/3]
            else:
                #kills sprite once out of animations
                self.kill()           
            
            #updates rect while keeping the old bottomleft
            self.__prev=self.rect.bottomleft
            self.rect=self.image.get_rect()
            self.rect.bottomleft=self.__prev           
            
            self.__frame+=1            
            
        #while alive
        else:            
            #horizontal movement    
            self.rect.left+=self.__vx*8
            
            #checks if the tank is outside the map
            if self.rect.left<=0:
                self.rect.left=0               
                
            #animation
            #shooting
            if self.__shooting_cannon:
                if self.__animation!=2:
                    self.__frame=0                
                    self.__animation=2 
                    self.__speed=2
            #still
            elif self.__animation and not self.__vx and not self.__vy:            
                self.__frame=0
                self.__speed=15
                self.__animation=0  
            #jumping
            elif self.__animation!=3 and self.__vy:
                self.__frame=0
                self.__speed=1
                self.__animation=3
            #running
            elif self.__animation!=1 and self.__vx and not self.__vy:
                self.__frame=0
                self.__speed=2
                self.__animation=1           
            
            #updates image
            self.image=self.__sprites[self.__animation][self.__frame/self.__speed].copy()            
            
            self.__prev=self.rect.bottomleft
            self.rect=self.image.get_rect()
            self.rect.bottomleft=self.__prev
                
            #mg turret
            self.__temp=pygame.transform.rotate(self.__mg, self.__angle)
            self.__temp_rect=self.__temp.get_rect()
            self.__temp_rect.center=((46,self.image.get_height()-59),(48,100))[self.__animation==3]
            self.image.blit(self.__temp,self.__temp_rect)   
            
            #flashed red while hurt
            if self.__hurt>0:
                if self.__hurt%5==0:
                    self.image.fill((200,0,0), special_flags=pygame.BLEND_RGB_MULT)
                self.__hurt-=1
            
            self.__frame+=1
            
            #cycles animation frames
            if self.__frame>=len(self.__sprites[self.__animation])*self.__speed:
                self.__frame=0
            #resets horizontal velocity and __shooting_cannon after the animation is over
            self.__vx=0
            if self.__shooting_cannon and self.__frame==0:
                self.__shooting_cannon=False            
                
class TankBullet(pygame.sprite.Sprite):
    '''tank bullet sprite'''
    __sprite=pygame.image.load('images\\bullet\\bullet3.png').convert_alpha()
    
    def __init__(self,bkgd,tank):   
        '''initializer method with the background and tank as parameters'''
        pygame.sprite.Sprite.__init__(self)          
        #rotates image
        self.image=pygame.transform.rotate(TankBullet.__sprite, tank.get_angle())             
        #gets rect and positions it
        self.rect=self.image.get_rect()        
        self.rect.center=tank.get_turret()       
        #calculate x and y velocities
        self.__vx=-math.sin(math.radians(tank.get_angle()))*30+random.randint(-1,1)
        self.__vy=-math.cos(math.radians(tank.get_angle()))*30+random.randint(-1,1)
        
        self.__frame=0
        self.__bkgd=bkgd
        
    def update(self,*args):
        '''update method'''
        #bullet starts moving during second frame
        if self.__frame:
            self.rect.left+=self.__vx
            self.rect.top+=self.__vy
        #kills bullet once it is outside the screen
        if self.rect.right<-self.__bkgd.rect.left or self.rect.left>-self.__bkgd.rect.left+640 or self.rect.bottom<0 or self.rect.top>480:
            self.kill()
            
        self.__frame+=1
        
class ScoreBoard(pygame.sprite.Sprite):
    '''scoreboard sprite'''
    def __init__(self,player,tank=None):
        '''initializer method with the player and the tank as parameters'''
        pygame.sprite.Sprite.__init__(self)
        
        #loads background and font
        self.__background=pygame.image.load('images\\scoreboard.png').convert_alpha()
        self.__font=pygame.font.Font('fonts\\Square.ttf',20)
        self.__player=player
        self.__tank=tank       
        self.rect=pygame.Rect(0,0,1,1)
        
    def update(self,current_player):
        '''update method'''
        self.image=self.__background.copy()  
        #blits labels
        self.image.blit(self.__font.render(('life     ','armour')[current_player==self.__tank]+' '*30+'ammo'+' '*7+('grenade','cannon')[current_player==self.__tank], True, (223,221,209)),(5,5))
        #draws health bar frame
        pygame.draw.rect(self.image,(0,0,0),(4,24,202,22),1)
        #draws health bar
        pygame.draw.rect(self.image,((75,196,81),(255,130,37))[current_player==self.__tank],(5,25,current_player.get_health(),20))
        #blits ammo and grenade count
        if type(current_player.get_ammo())!=int:
            self.__ammo=current_player.get_ammo()
        else:
            self.__ammo=str(current_player.get_ammo())
        self.image.blit(self.__font.render(self.__ammo.center(3)+' '*15+str(current_player.get_grenades()),True,(241,125,4)),(230,25))
        
class Animation(pygame.sprite.Sprite):
    '''title animations'''
    def __init__(self,num):
        '''initializer method with the image number as the parameter'''
        pygame.sprite.Sprite.__init__(self)        
        
        #loads image and rect
        self.__image=pygame.image.load('images\\'+('metal','python')[num]+'.png').convert_alpha()           
        self.rect=self.__image.get_rect()      
        self.rect.center=(160,80+50*num)
        
        self.__frame=0        
        self.__size=self.__image.get_size()
        
    def get_done(self):
        '''returns True when the animation is over'''
        return self.__frame==20        
    
    def update(self):
        '''update method'''
        if self.__frame<20:        
            self.image=pygame.transform.scale(self.__image.copy(), self.__size)
            self.__prev=self.rect.center
            self.rect=self.image.get_rect()
            self.rect.center=self.__prev         
            #makes image 98% smaller each frame
            self.__size=map(lambda x:int(0.98*x),self.__size)            
            self.__frame+=1
        
class Button(pygame.sprite.Sprite):
    '''button class'''
    #sound
    __press=pygame.mixer.Sound('sounds\\button.wav')
    
    def __init__(self,num):
        '''initializer class with the button number'''
        pygame.sprite.Sprite.__init__(self)
        #loads font and text
        self.__font=pygame.font.Font('fonts\\Square.ttf',30)        
        self.__text=('START','CONTROLS','QUIT','BACK','RESUME','RETURN TO TITLE SCREEN')[num]
        #loads image and rect
        self.image=self.__font.render(self.__text,True,(255,255,255))
        self.rect=self.image.get_rect()              
        self.rect.center=((160,200),(160,250),(160,300),(280,440),(320,200),(320,280))[num]
        
        self.__collided=False        
        
    def get_pressed(self):
        '''returns whether the button is being pressed'''
        self.__collided=self.rect.collidepoint(pygame.mouse.get_pos())
        if self.__collided and pygame.mouse.get_pressed()[0]:
            Button.__press.play()
            return True
        
    def update(self):
        '''update method'''
        #turns red when mouse if hovering over it 
        self.image=self.__font.render(self.__text,True,((255,255,255),(255,0,0))[self.__collided])      
        
class GameOver(pygame.sprite.Sprite):
    '''class for gameover screen'''
    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)
        #loads background image and rect
        self.__bkgd=pygame.image.load('images\\gameover.jpg').convert()
        self.rect=self.__bkgd.get_rect()
        self.rect.topleft=(0,0)
        #initial tint
        self.__colour=0      
        
    def get_done(self):
        '''returns True once the animation is over'''
        return self.__colour>=300
        
    def update(self):
        '''update method'''
        #colour goes from dark to bright    
        if self.__colour<=255:   
            self.image=self.__bkgd.copy()
            self.image.fill((self.__colour,)*3, special_flags=pygame.BLEND_RGB_MULT)
        else:
            self.image=self.__bkgd
        
        #lightens colour
        self.__colour+=1  
        
class Boss(pygame.sprite.Sprite):
    '''class for gameover screen'''
    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)
        
        #loads image and rect
        self.__sprites=[pygame.image.load('images\\boss\\tank'+str(i)+'.png').convert_alpha() for i in range(2)]
        self.__explosion=[pygame.image.load('images\\tank\\4\\'+str(i)+'.png').convert_alpha() for i in range(17,42)]
        
        self.image=self.__sprites[0].copy()
        self.rect=self.image.get_rect()
        self.rect.topleft=(865,283)        
        
        #initializes parameters
        self.__health=3000        
        self.__active=False        
        self.__animation=0
        self.__delay=0
        self.__attack=0        
        self.__dying=False
        self.__dead=False
        self.__hurt=False
        self.__frame=0
        #sound
        self.__explode=pygame.mixer.Sound('sounds\\explosion.wav')
        
    def start(self):
        '''called when the player sees the tank and the tank starts to attack'''
        self.__active=True
        
    def get_attack(self):
        '''returns the current attack'''
        return self.__attack
    
    def hurt(self,damage): 
        '''reduces health'''
        self.__health-=damage
        self.__hurt=True
        
    def get_dead(self):
        '''returns True when the boss death animation is over'''
        return self.__dead
    
    def update(self,*args):
        '''update method'''        
        #checks if boss is dead
        if not self.__dying and self.__health<=0:
            self.__dying=True
            self.__delay=0
            self.__explode.play()
            
        #death animation
        if self.__dying:
            self.image=self.__explosion[self.__delay/3]
            self.__prev=self.rect.center
            self.rect=self.image.get_rect()
            self.rect.center=self.__prev
            self.__delay+=1
            if self.__delay>=len(self.__explosion)*3:
                self.kill()
                self.__dead=True
        #while alive    
        elif self.__active:
            #picks random attack
            if not self.__animation:
                self.__animation=random.randint(0,2)
                self.__delay=0
            #shoot cannon every half second
            if self.__animation==1:
                self.image=self.__sprites[0].copy()
                if self.__delay in (30,60,90):
                    self.__attack=1
                if self.__delay in (31,61,91):
                    self.__attack=0
                #stops shooting after 3 seconds
                elif self.__delay==150:
                    self.__animation=0
                    self.__delay==0
            #laser cannon
            elif self.__animation==2:
                #changes tank image
                if self.__delay==0:
                    self.__frame=1                    
                #starts shooting
                elif self.__delay==60:
                    self.__frame=0                    
                    self.__attack=2
                elif self.__delay==61:
                    self.__attack=0
                #stops shooting
                elif self.__delay==150:
                    self.__animation=0
                    self.__delay=0
                    
            #clears image
            self.image=self.__sprites[self.__frame].copy()
            #flashes red when hurt
            if self.__hurt:
                self.image.fill((200,0,0), special_flags=pygame.BLEND_RGB_MULT)
                self.__hurt=False
                
        self.__delay+=1
                    
class Laser(pygame.sprite.Sprite):
    '''laser attack for boss'''
    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)
        #loads image and rect
        self.__sprites=[pygame.image.load('images\\boss\\laser\\'+str(i)+'.png') for i in range(4)]
        self.image=self.__sprites[0]
        self.rect=self.image.get_rect()
        self.hide()
        self.__frame=0
        
    def reset(self):        
        '''activates laser'''
        self.rect.midright=(910,390)
        self.__active=True
        self.__frame=0
        
    def hide(self):
        '''hides laser by moving it offscreen'''
        self.__active=False
        self.rect.bottom=-1        
        
    def update(self,*args):
        '''update method'''
        #changes pictures    
        if self.__active:
            if not self.__frame:
                self.image=self.__sprites[0]
            elif self.__frame==20:
                self.image=self.__sprites[1]
            elif self.__frame==40:
                self.image=self.__sprites[2]
            elif self.__frame==45:
                self.image=self.__sprites[3]
            elif self.__frame==50:
                self.hide()
            
            #recenters image
            self.__prev=self.rect.midright
            self.rect=self.image.get_rect()
            self.rect.midright=self.__prev
            
            self.__frame+=1     
            
class MGIcon(pygame.sprite.Sprite):
    '''machine gun pickup'''    
    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('images\\mgicon.png')
        self.rect=self.image.get_rect()
        self.hide()
        
    def hide(self):
        '''hides image'''
        self.__active=False
        self.rect.bottom=-1        
        
    def update(self,*args):            
        if self.__active:
            #moves image down
            self.rect.bottom+=5
            if self.rect.bottom>=480:
                #hides image again when it is below the screen
                self.hide()
        else:
            #randomly respawns it at a random x location
            if random.randint(1,750)==1:
                self.__active=True
                self.rect.centerx=random.randint(300,800)
                
        
        