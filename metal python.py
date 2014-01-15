# coding=utf-8
'''
     Author: David Su
     
     Date: May 2, 2012
     
     Description: Metal Python main program
'''    

# I - IMPORT AND INITIALIZE 
import pygame, sprites
pygame.init()
pygame.mixer.init()

# DISPLAY 
screen=pygame.display.set_mode((640, 480)) 
pygame.display.set_caption("Metal Python")

def main():
    '''main function'''
    keepGoing=True
    while keepGoing:
        status1=title_screen()
        if status1==0:
            status2=level1()
            if status2[0]==0:
                status3=boss(*status2[1:])                
                if status3==1:
                    if gameover():                        
                        keepGoing=False
                elif status3==2:
                    keepGoing=False
            elif status2[0]==1:                
                if gameover():
                    keepGoing=False
            elif status2[0]==2:
                keepGoing=False
        elif status1==1:            
            if instructions():
                keepGoing=False
        elif status1==2:
            keepGoing=False        
            
    pygame.mouse.set_visible(True)
    pygame.quit()

def instructions():
    '''instructions screen'''
    #Entities
    bkgd=pygame.image.load('images\\instructions.png').convert()   
    button=sprites.Button(3)    
    allSprites=pygame.sprite.Group(button)
    
    #ASSIGN
    clock=pygame.time.Clock() 
    keepGoing=True
    
    #LOOP
    while keepGoing:
        # TIME
        clock.tick(30)     
        
        # EVENT HANDLING        
        for event in pygame.event.get():              
            if event.type==pygame.QUIT:                
                keepGoing=False  
                exitstatus=1
                
        if button.get_pressed():
            keepGoing=False
            exitstatus=0                
        
        # REFRESH SCREEN          
        screen.blit(bkgd,(0,0))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    
    return exitstatus
        
def title_screen():
    '''title screen'''
    #Entities
    bkgd=pygame.image.load('images\\title screen.jpg').convert()    
    animations=[sprites.Animation(i) for i in range(2)]
    buttons=[sprites.Button(i) for i in range(3)]    
    allSprites=pygame.sprite.Group(animations[0])
    
    #sound
    sfx=pygame.mixer.Sound('sounds\\menu.wav')
    sfx.play()

    #ASSIGN
    clock=pygame.time.Clock() 
    keepGoing=True
    pygame.mouse.set_visible(True)
    
    #LOOP
    while keepGoing:
        # TIME
        clock.tick(30)     
        
        # EVENT HANDLING        
        for event in pygame.event.get():              
            if event.type==pygame.QUIT:                
                keepGoing=False 
                exitstatus=2
                
        #handles text animation
        if animations[0].get_done():
            allSprites.add(animations[1])
            
        if animations[1].get_done():
            allSprites.add(buttons)
            
        #checks if the user pressed any buttons    
        if buttons[0].get_pressed():            
            keepGoing=False
            exitstatus=0
        elif buttons[1].get_pressed():
            keepGoing=False
            exitstatus=1
        elif buttons[2].get_pressed():
            keepGoing=False
            exitstatus=2   
        
        # REFRESH SCREEN          
        screen.blit(bkgd,(0,0))
        allSprites.update()
        allSprites.draw(screen)      
        pygame.display.flip()
        
    return exitstatus

def level1():
    '''main game'''    
    # ENTITIES   
    #     players
    player=sprites.Player()
    tank=sprites.Tank()
    playerGrp=pygame.sprite.Group(tank,player)
    current_player=player
    
    #     background
    clean_bkgd=pygame.image.load('images\\bkgd.png').convert()
    bkgd=sprites.Background(player)     
       
    #     map objects    
    wall=sprites.Platform(((1438,380),(1,100)))
    platforms=pygame.sprite.Group([sprites.Platform(dimension) for dimension in (((0,366),(1400,1)),((1438,450),(2507,1)),((1845,342),(110,1)),((2032,260),(348,1)),((2380,342),(130,1)),((2510,260),(290,1)),((2915,260),(345,1)),((3260,342),(150,1)))])
    
    #     projectiles
    pBulletsGrp=pygame.sprite.Group()   
    eBulletsGrp=pygame.sprite.Group()   
    grenadeGrp=pygame.sprite.Group()
    
    #     scoreboard
    scoreboard=sprites.ScoreBoard(player,tank)
    
    #     enemies
    enemiesGrp=pygame.sprite.Group([sprites.Enemy(midbottom) for midbottom in ((500,366),(800,366),(1000,366),(1100,366),(1200,366),(1300,366),(1700,450),(1800,450),(1900,450),(2300,450),(2400,450),(2500,450),(2600,450),(2700,450),(2800,450),(2900,450),(3000,450),(3100,450),(3200,450),(3400,450),(3500,450),(3600,450),(3800,450),(1880,342),(2040,260),(2200,260),(2400,342),(2550,260),(2700,260),(2950,260),(3100,260),(3280,342))])    
    
    #     sound
    pygame.mixer.music.load('sounds\\music.mp3')
    pygame.mixer.music.play(-1)
    
    allSprites=pygame.sprite.OrderedUpdates(enemiesGrp,playerGrp,eBulletsGrp,pBulletsGrp,grenadeGrp)   
    
    #ASSIGN
    clock=pygame.time.Clock() 
    keepGoing=True
    pygame.mouse.set_visible(False)
    
    
    #LOOP
    while keepGoing:
        # TIME
        clock.tick(30)     
        
        # EVENT HANDLING        
        for event in pygame.event.get():              
            if event.type==pygame.QUIT:                
                keepGoing=False
                exitstatus=2
            if not current_player.get_dying():
                if event.type==pygame.KEYDOWN:                    
                    if event.key==pygame.K_e:
                        #enter tank
                        if pygame.sprite.collide_rect(player,tank) and current_player==player and not tank.get_dying():
                            current_player=tank
                            player.kill()
                        #exit tank
                        elif current_player==tank:                        
                            player.respawn(tank)
                            playerGrp.add(player)
                            allSprites.add(playerGrp)
                            current_player=player
                            tank.die()
                    elif event.key==pygame.K_l:
                        #fire cannon
                        if current_player==tank:
                            if tank.shoot_cannon():
                                grenadeGrp.add(sprites.TankShell(tank))                        
                                allSprites.add(grenadeGrp)
                        #throw grenade
                        elif player.get_grenades():                      
                            player.throw_grenade()
                            grenadeGrp.add(sprites.Grenade(player))                        
                            allSprites.add(grenadeGrp)                                          
                        
        if not current_player.get_dying():                
            keys_pressed=pygame.key.get_pressed()      
            #left and right movement        
            if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_a]:
                pass
            elif keys_pressed[pygame.K_a]:
                current_player.move(-1)
            elif keys_pressed[pygame.K_d]:
                current_player.move(1)
            #jump       
            if keys_pressed[pygame.K_j]:
                    current_player.jump()
                    
            #tank controls       
            if current_player==tank:          
                #shoot mg
                if keys_pressed[pygame.K_k]:
                    tank.shoot_mg()
                    pBulletsGrp.add(sprites.TankBullet(bkgd,tank))
                    allSprites.add(pBulletsGrp)              
                #rotate mg    
                if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]:
                    pass
                elif keys_pressed[pygame.K_w]:
                    tank.rotate(5)
                elif keys_pressed[pygame.K_s]:
                    tank.rotate(-5)
            #player control        
            else:             
                if keys_pressed[pygame.K_k]:
                    #shoot mg
                    if player.get_weapon():                     
                        pBulletsGrp.add(sprites.MGBullet(bkgd,player,player.shoot()))                        
                        allSprites.add(pBulletsGrp)
                    #shoot pistol    
                    elif player.shoot():
                        pBulletsGrp.add(sprites.PistolBullet(bkgd,player))
                        allSprites.add(pBulletsGrp)
        #collision detection                
        for item in (player,tank):  
            #collision with wall
            if pygame.sprite.collide_rect(item,wall):
                item.collide_wall(wall)    
                
            #collision with platforms    
            collision=pygame.sprite.spritecollide(item,platforms,False)           
            if collision:                              
                #finds lowest platform to land on
                item.land(max(platform.rect.top for platform in collision))               
            else:
                item.fall() 
            
        #bullet collision with current player
        for bullet in pygame.sprite.spritecollide(current_player,eBulletsGrp,False):            
            if not current_player.get_dying():
                bullet.kill()
                current_player.hurt(50)
            
        #tank collision with enemies
        for enemy in pygame.sprite.spritecollide(tank,enemiesGrp,False):            
            enemy.die()
            
        #bullet collision with enemies
        for bullet,enemy in pygame.sprite.groupcollide(pBulletsGrp,enemiesGrp,False,False).iteritems():            
            if enemy and not enemy[0].get_dying():
                bullet.kill()
                enemy[0].die()               
                
        #grenade collision with enemies
        for grenade,enemy in pygame.sprite.groupcollide(grenadeGrp,enemiesGrp,False,True).iteritems():            
            if enemy:
                grenade.explode()
                for i in enemy:
                    i.die()                        
                    
        #grenade collision with platforms
        for grenade,platform in pygame.sprite.groupcollide(grenadeGrp,platforms,False,False).iteritems():            
            if platform:
                grenade.explode()                
                
        #enemy shooting
        for enemy in enemiesGrp:
            if enemy.get_shooting():
                eBulletsGrp.add(sprites.EnemyBullet(enemy,current_player))
                allSprites.add(eBulletsGrp) 
        
        #kills tank, respawns player
        if tank.get_dying():
            player.respawn(tank)
            playerGrp.add(player)
            allSprites.add(playerGrp)
            current_player=player
            
        #exits game loop once player death animation is over                
        if player.get_dying()==2:            
            keepGoing=False
            exitstatus=1
        
        #checks if player completed level    
        if current_player.rect.right>=bkgd.image.get_width():
            keepGoing=False
            exitstatus=0
            
        # REFRESH SCREEN 
        #draws allSprites on background 
        bkgd.image.blit(clean_bkgd,(0,0))
        allSprites.update(current_player)
        allSprites.draw(bkgd.image)
        
        #updates background position
        bkgd.update(current_player)
        screen.blit(bkgd.image,bkgd.rect)
        
        #updates scoreboard onto screen
        scoreboard.update(current_player)
        screen.blit(scoreboard.image,scoreboard.rect)
        
        pygame.display.flip()
        
    pygame.mixer.music.stop()
    if tank.get_dying():
        return exitstatus,player
    return exitstatus,player,tank     

def gameover():
    #Entities
    bkgd=sprites.GameOver()       
    allSprites=pygame.sprite.Group(bkgd)
    #sound
    pygame.mixer.music.load('sounds\\gameover.wav')
    pygame.mixer.music.play()
    
    #ASSIGN
    clock=pygame.time.Clock() 
    keepGoing=True
    
    #LOOP
    while keepGoing:
        # TIME
        clock.tick(30)     
        
        # EVENT HANDLING        
        for event in pygame.event.get():              
            if event.type==pygame.QUIT:                
                keepGoing=False       
                exitstatus=1                
        
        if bkgd.get_done():
            keepGoing=False
            exitstatus=0                
        
        # REFRESH SCREEN          
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()      
   
    return exitstatus    

def boss(prev_player,prev_tank=None):
    #Entities
    #player
    player=sprites.Player(prev_player)
    if prev_tank:    
        tank=sprites.Tank(prev_tank)
        current_player=tank
        playerGrp=pygame.sprite.Group(tank)
    else:
        tank=None
        current_player=player
        playerGrp=pygame.sprite.Group(player)
    
    #     background
    clean_bkgd=pygame.image.load('images\\bossbkgd2.png').convert()
    bkgd=sprites.Background(player,1)     
       
    #     map objects    
    wall=sprites.Platform(((865,0),(1,480)))
    platform=sprites.Platform(((0,432),(1280,1)))
    
    #     projectiles
    laser=sprites.Laser()
    pBulletsGrp=pygame.sprite.Group()   
    shellGrp=pygame.sprite.Group()   
    pGrenadeGrp=pygame.sprite.Group()
    
    #powerup
    mgicon=sprites.MGIcon()
    
    #     scoreboard
    scoreboard=sprites.ScoreBoard(player,tank)
    
    #     boss
    boss=sprites.Boss()    
    
    #     sound
    pygame.mixer.music.load('sounds\\boss.mp3')
    pygame.mixer.music.play(-1)  
    missioncomplete=pygame.mixer.Sound('sounds\\mission complete.wav')
    
    allSprites=pygame.sprite.OrderedUpdates(playerGrp,boss,mgicon,pBulletsGrp,shellGrp,pGrenadeGrp,laser)   
    
    #ASSIGN
    clock=pygame.time.Clock() 
    keepGoing=True
    pygame.mouse.set_visible(False)    
    cutscene=True        
    
    #LOOP
    while keepGoing:
        # TIME
        clock.tick(30)     
        
        # EVENT HANDLING        
        for event in pygame.event.get():              
            if event.type==pygame.QUIT:                
                keepGoing=False
                exitstatus=2            
            if not cutscene and not current_player.get_dying():
                if event.type==pygame.KEYDOWN:                    
                    if event.key==pygame.K_e:                        
                        #exit tank
                        if current_player==tank:                        
                            player.respawn(tank)
                            playerGrp.add(player)
                            allSprites.add(playerGrp)
                            current_player=player
                            tank.die()
                    elif event.key==pygame.K_l:
                        #fire cannon
                        if current_player==tank:
                            if tank.shoot_cannon():
                                pGrenadeGrp.add(sprites.TankShell(tank))              
                                allSprites.add(pGrenadeGrp)
                        #throw grenade
                        elif player.get_grenades():                      
                            player.throw_grenade()
                            pGrenadeGrp.add(sprites.Grenade(player))
                            allSprites.add(pGrenadeGrp)
                            
        #cutscene at beginning of level                
        if cutscene:
            current_player.move(1)
            if current_player.rect.left+700>=boss.rect.right:
                cutscene=False
                boss.start()        
                            
        elif not current_player.get_dying():                
            keys_pressed=pygame.key.get_pressed()      
            #left and right movement        
            if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_a]:
                pass
            elif keys_pressed[pygame.K_a]:
                current_player.move(-1)
            elif keys_pressed[pygame.K_d]:
                current_player.move(1)
            #jump       
            if keys_pressed[pygame.K_j]:
                    current_player.jump()
                    
            #tank controls       
            if current_player==tank:          
                #shoot mg
                if keys_pressed[pygame.K_k]:
                    tank.shoot_mg()
                    pBulletsGrp.add(sprites.TankBullet(bkgd,tank))
                    allSprites.add(pBulletsGrp)              
                #rotate mg    
                if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]:
                    pass
                elif keys_pressed[pygame.K_w]:
                    tank.rotate(5)
                elif keys_pressed[pygame.K_s]:
                    tank.rotate(-5)
            #player control        
            else:             
                if keys_pressed[pygame.K_k]:
                    #shoot mg
                    if player.get_weapon():                     
                        pBulletsGrp.add(sprites.MGBullet(bkgd,player,player.shoot()))                        
                        allSprites.add(pBulletsGrp)
                    #shoot pistol    
                    elif player.shoot():
                        pBulletsGrp.add(sprites.PistolBullet(bkgd,player))
                        allSprites.add(pBulletsGrp)
                        
        #collision detection                
        for item in filter(bool,(player,tank)):  
            #collision with wall
            if pygame.sprite.collide_rect(item,wall):
                item.collide_wall(wall,1)    
                
            #collision with platforms                         
            if pygame.sprite.collide_rect(item,platform):                              
                #finds lowest platform to land on
                item.land(platform.rect.top)               
            else:
                item.fall() 
        
        #laser collision with player
        if pygame.sprite.collide_rect(laser,current_player):
            current_player.hurt(50)    
            
        #MGIcon collision with player
        if pygame.sprite.collide_rect(mgicon,current_player):
            player.pickup()
            mgicon.hide()
        
        #shell collision with player
        for shell in pygame.sprite.spritecollide(current_player,shellGrp,False):            
            if not current_player.get_dying():
                shell.explode()
                current_player.hurt(50)
            
        #shell collision with ground
        for shell in pygame.sprite.spritecollide(platform,shellGrp,False):   
            shell.explode()           
                
        #grenade collision with boss
        for grenade in pygame.sprite.spritecollide(boss,pGrenadeGrp,False):           
            grenade.explode()
            boss.hurt(5)       
            
        #bullet collision with boss
        for bullet in pygame.sprite.spritecollide(boss,pBulletsGrp,False):           
            bullet.kill()
            boss.hurt(1) 
                    
        #grenade collision with ground
        for grenade in pygame.sprite.spritecollide(platform,pGrenadeGrp,False):
            grenade.explode()                
                
        #boss shooting shells
        if boss.get_attack()==1:
            shellGrp.add(sprites.TankShell())
            allSprites.add(shellGrp)
        #laser attack
        elif boss.get_attack()==2:
            laser.reset()
        
        #kills tank, respawns player
        if tank and tank.get_dying():
            player.respawn(tank)
            playerGrp.add(player)
            allSprites.add(playerGrp)
            current_player=player
            
        #exits game loop once player death animation is over                
        if player.get_dying()==2:            
            keepGoing=False
            exitstatus=1
        
        #checks if player successfully completed level    
        if boss.get_dead():
            pygame.mixer.music.stop()
            missioncomplete.play()
            screen.blit(pygame.image.load('images\\mission complete.png').convert_alpha(),(109,167))
            pygame.display.flip() 
            pygame.time.wait(8000)
            keepGoing=False
            exitstatus=0
            
        # REFRESH SCREEN 
        #draws allSprites on background 
        bkgd.image.blit(clean_bkgd,(0,0))
        allSprites.update(current_player)
        allSprites.draw(bkgd.image)
        
        #updates background position
        bkgd.update(current_player)
        screen.blit(bkgd.image,bkgd.rect)
        
        #updates scoreboard onto screen
        scoreboard.update(current_player)
        screen.blit(scoreboard.image,scoreboard.rect)
        
        pygame.display.flip()        
    
    return exitstatus  

main()