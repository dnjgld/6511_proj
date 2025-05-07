import pygame
import sys
import wall
import myTank
import enemyTank
import food
import maps
import map_loader
import special_effects
#################################
import random
import time
import pickle
import numpy as np
# Please jump to line 1215 to see the function for the AI agent
#################################


"""
修改时间：2021.12.15
修改人：2019051604048 詹孝东
模块描述：
该模块是游戏类 是本游戏的主要模块
该类基本组合或者聚合了基本所有的类 就相当于一个棋盘（其它类相当于棋子 这样游戏就可以开始了）
游戏类有game_running和game_running_singled_out是两个相似的游戏方法，
只需要首先申明类然后调用其中一个方法就可以开始游戏，两个方法的区别就是游戏模式的不同
其它的方法就是服务于这两个方法的 比如暂停方法，结束方法，检测键盘方法等
推荐：如果想要了解大体框架，将所有的方法缩小（就是将函数内容隐藏） 这样更有条理
"""
class Game:
    def __init__(self):
        # 通用加载
        # ----------------------------------------------------------------------------
        pygame.init()
        # 用于加载和播放声音的 pygame 模块
        pygame.mixer.init()
        # 加载屏幕
        resolution = 750, 630
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Tank War ")
        # 加载图片,音乐,音效.
        self.background_image = pygame.image.load(r"image/background.png")
        # 右边提示图片加载
        self.background_image_level_mode = pygame.image.load(r"image/background_level_model_tishi.png")
        self.background_image_endless_mode = pygame.image.load(r"image/background_endless_mode_tishi.png")
        self.background_image_heads_up_mode = pygame.image.load(r"image/background_heads_up_mode_tishi.png")

        self.enemy_icon = pygame.image.load(r"image/enemy.png")
        self.heart_icon = pygame.image.load(r"image/heart.png")

        # 游戏结束图片
        self.game_over_player1_win = pygame.image.load(r"image/game_over_player1_win.png")
        self.game_over_player2_win = pygame.image.load(r"image/game_over_player2_win.png")
        self.game_over_win = pygame.image.load(r"image/game_over_win.png")
        self.game_over_fail = pygame.image.load(r"image/game_over_fail.png")
        # 暂停图片加载
        self.game_pause_image = pygame.image.load(r"image/game_pause.png")

        # 音效加载-------------------------------------------------------
        self.bang_sound = pygame.mixer.Sound(r"music/bang.wav")
        self.bang_sound.set_volume(1)
        self.start_sound = pygame.mixer.Sound(r"music/start.wav")
        # 队友加载和吃道具音效
        self.add_sound = pygame.mixer.Sound(r"music/add.wav")
        # 子弹打出音效（正式）
        self.attack_sound = pygame.mixer.Sound(r"music/attack.mp3")
        # 获取道具音效（正式）
        self.get_props_sound = pygame.mixer.Sound(r"music/get_props.mp3")
        # 道具出现音效（正式）
        self.prop_sound = pygame.mixer.Sound(r"music/prop.mp3")
        # 炸弹爆炸特效（正式）
        self.prop_boom_sound = pygame.mixer.Sound(r"music/prop_boom.wav")
        # 打到墙上的音效（正式）
        self.wall_sound = pygame.mixer.Sound(r"music/wall.mp3")
        # 定义精灵组:坦克，我方坦克，敌方坦克，敌方子弹
        # 用于保存和管理多个 Sprite 对象的容器类。pygame.sprite.Group()
        self.allTankGroup = pygame.sprite.Group()
        self.mytankGroup = pygame.sprite.Group()
        self.allEnemyGroup = pygame.sprite.Group()
        self.redEnemyGroup = pygame.sprite.Group()
        self.greenEnemyGroup = pygame.sprite.Group()
        self.otherEnemyGroup = pygame.sprite.Group()
        self.enemyBulletGroup = pygame.sprite.Group()

        # 自定义事件
        # 创建敌方坦克延迟200
        self.DELAYEVENT = pygame.constants.USEREVENT
        pygame.time.set_timer(self.DELAYEVENT, 200)
        # 创建 敌方 子弹延迟1000
        self.ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1
        pygame.time.set_timer(self.ENEMYBULLETNOTCOOLINGEVENT, 1000)
        # 创建 我方 子弹延迟200
        self.MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2
        pygame.time.set_timer(self.MYBULLETNOTCOOLINGEVENT, 200)
        # 敌方坦克 静止8000
        self.NOTMOVEEVENT = pygame.constants.USEREVENT + 3
        pygame.time.set_timer(self.NOTMOVEEVENT, 8000)

        # ...............参数..................................
        self.isEndless = False
        self.delay = 100
        # 敌军剩余数量
        self.remaining_enemy = 20
        # 移动参数
        self.moving = 0
        self.movdir = 0
        self.moving2 = 0
        self.movdir2 = 0
        self.running_T1 = True
        self.running_T2 = True

        self.enemyNumber = 3
        self.enemyCouldMove = True
        self.switch_R1_R2_image = True

        self.overGameLoss = False
        self.overGameWin = False
        # 关于保护罩的参数
        self.invincible_T1 = 200  # 是否无敌
        self.invincible_T2 = 200

        self.clock = pygame.time.Clock()

        # 特效和地图的初始化
        self.special_effect = special_effects.SE()
        self.bgMap = maps.Map()

        # 创建我方坦克
        self.myTank_T1 = myTank.MyTank(1)
        self.allTankGroup.add(self.myTank_T1)
        self.mytankGroup.add(self.myTank_T1)
        self.myTank_T2 = myTank.MyTank(2)
        self.allTankGroup.add(self.myTank_T2)
        self.mytankGroup.add(self.myTank_T2)

        # 创建食物/道具 但不显示
        self.prop = food.Food()
        self.bulletBoomGroup = []
        # 是否打开音效
        self.isSoundEffect = True

        # 基地是否是砖块
        self.iron_time = 0

    # 暂停函数----------------------------------------------------------------
    # 功能：点击鼠标进行暂停 并显示图片在桌面
    def game_pause(self):
        self.start_sound.stop()
        while True:
            # 显示图片
            self.screen.blit(self.game_pause_image, (250, 250))
            pygame.display.flip()
            # 如果点击鼠标就暂停结束
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # 游戏结束函数------------------------------------------------------------
    # 功能：弹出游戏结束界面，并根据结果的不同显示不同结果，并提供退出游戏
    def game_over(self,option):
        while True:
            # 根据游戏结局不同 选择不同图片显示
            if option == 1:
                self.screen.blit(self.game_over_win, (250 , 250))
            elif option == 2:
                self.screen.blit(self.game_over_fail, (250, 250))
            elif option == 3:
                self.screen.blit(self.game_over_player1_win, (250, 250))
            elif option == 4:
                self.screen.blit(self.game_over_player2_win, (250, 250))

            pygame.display.flip()
            key_pressed = pygame.key.get_pressed()
            # 按esc退出游戏
            if key_pressed[pygame.K_ESCAPE]:
                self.start_sound.stop()
                return 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # 处理事件函数-----------------------------------------------------------
    # 功能：主要就是对冷却事件的处理
    def event_section(self):
        for event in pygame.event.get():
            # 如果鼠标单击
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_pause()
            # 如果退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 我方子弹冷却事件
            if event.type == self.MYBULLETNOTCOOLINGEVENT:
                self.myTank_T1.bulletNotCooling = True

            # 敌方子弹冷却事件
            if event.type == self.ENEMYBULLETNOTCOOLINGEVENT:
                for each in self.allEnemyGroup:
                    each.bulletNotCooling = True

            # 敌方坦克静止事件
            if event.type == self.NOTMOVEEVENT:
                self.enemyCouldMove = True

            # 创建敌方坦克延迟
            if event.type == self.DELAYEVENT:
                # 敌方坦克最大数量
                if self.enemyNumber < 4 and self.remaining_enemy-self.enemyNumber >=1:
                    enemy = enemyTank.EnemyTank()
                    if pygame.sprite.spritecollide(enemy, self.allTankGroup, False, None):
                        break
                    self.allEnemyGroup.add(enemy)
                    self.allTankGroup.add(enemy)
                    self.enemyNumber += 1
                    if enemy.isred == True:
                        self.redEnemyGroup.add(enemy)
                    elif enemy.kind == 3:
                        self.greenEnemyGroup.add(enemy)
                    else:
                        self.otherEnemyGroup.add(enemy)

            # 作弊按钮
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.isSoundEffect = not self.isSoundEffect
                    self.start_sound.stop()
                # if event.key == pygame.K_c and pygame.KMOD_CTRL:
                #     pygame.quit()
                #     sys.exit()
                # if event.key == pygame.K_e:
                #     self.myTank_T1.levelUp()
                # if event.key == pygame.K_q:
                #     self.myTank_T1.levelDown()
                # if event.key == pygame.K_3:
                #     self.myTank_T1.levelUp()
                #     self.myTank_T1.levelUp()
                #     self.myTank_T1.level = 3
                # if event.key == pygame.K_2:
                #     if self.myTank_T1.speed == 3:
                #         self.myTank_T1.speed = 24
                #     else:
                #         self.myTank_T1.speed = 3
                # if event.key == pygame.K_1:
                #     for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                #         self.bgMap.brick = wall.Brick()
                #         self.bgMap.brick.rect.left, self.bgMap.brick.rect.top = 3 + x * 24, 3 + y * 24
                #         self.bgMap.brickGroup.add(self.bgMap.brick)
                # if event.key == pygame.K_4:
                #     for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                #         self.bgMap.iron = wall.Iron()
                #         self.bgMap.iron.rect.left, self.bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                #         self.bgMap.ironGroup.add(self.bgMap.iron)

    # 处理事件函数（单挑版）---------------------------------------------------------
    # 功能：主要就是对冷却事件的处理
    def event_section_singled_out(self):
        for event in pygame.event.get():
            # 如果鼠标单击
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_pause()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 我方子弹冷却事件
            if event.type == self.MYBULLETNOTCOOLINGEVENT:
                self.myTank_T1.bulletNotCooling = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.isSoundEffect = not self.isSoundEffect
                    self.start_sound.stop()
    # 玩家操作检测函数--------------------------------------------------------
    # 功能：对键盘进行检测 并对玩家一和玩家二的操作进行移动
    def operation_detection_section(self):
        key_pressed = pygame.key.get_pressed()
        # 玩家一的移动、射击操作
        # 参数 moving movdir alltankGroup self.bgMap.brickGroup, self.bgMap.ironGroup,self.bgMap.riverGroup
        if self.myTank_T1.life > 0:  # 如果有生命
            if self.moving:
                self.moving -= 1
                if self.movdir == 0:
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveUp(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                             self.bgMap.riverGroup):
                        self.moving += 1
                    self.allTankGroup.add(self.myTank_T1)
                    self.running_T1 = True
                if self.movdir == 1:
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveDown(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                               self.bgMap.riverGroup):
                        self.moving += 1
                    self.allTankGroup.add(self.myTank_T1)
                    self.running_T1 = True
                if self.movdir == 2:
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveLeft(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                               self.bgMap.riverGroup):
                        self.moving += 1
                    self.allTankGroup.add(self.myTank_T1)
                    self.running_T1 = True
                if self.movdir == 3:
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveRight(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                                self.bgMap.riverGroup):
                        self.moving += 1
                    self.allTankGroup.add(self.myTank_T1)
                    self.running_T1 = True

            if not self.moving:
                if key_pressed[pygame.K_w]:
                    self.moving = 7
                    self.movdir = 0
                    self.running_T1 = True
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveUp(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                             self.bgMap.riverGroup):
                        self.moving = 0
                    self.allTankGroup.add(self.myTank_T1)
                elif key_pressed[pygame.K_s]:
                    self.moving = 7
                    self.movdir = 1
                    self.running_T1 = True
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveDown(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                               self.bgMap.riverGroup):
                        self.moving = 0
                    self.allTankGroup.add(self.myTank_T1)
                elif key_pressed[pygame.K_a]:
                    self.moving = 7
                    self.movdir = 2
                    self.running_T1 = True
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveLeft(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                               self.bgMap.riverGroup):
                        self.moving = 0
                    self.allTankGroup.add(self.myTank_T1)
                elif key_pressed[pygame.K_d]:
                    self.moving = 7
                    self.movdir = 3
                    self.running_T1 = True
                    self.allTankGroup.remove(self.myTank_T1)
                    if self.myTank_T1.moveRight(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                                self.bgMap.riverGroup):
                        self.moving = 0
                    self.allTankGroup.add(self.myTank_T1)
            # 如果按j 则是坦克1发射子弹
            if key_pressed[pygame.K_j]:
                if not self.myTank_T1.bullet.life and self.myTank_T1.bulletNotCooling:
                    if self.isSoundEffect:
                        self.attack_sound.play()
                    self.myTank_T1.shoot()
                    self.myTank_T1.bulletNotCooling = False

        # 玩家二的移动操作
        if self.myTank_T2.life > 0:
            if self.moving2:
                self.moving2 -= 1
                if self.movdir2 == 0:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveUp(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                          self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.running_T2 = True
                if self.movdir2 == 1:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveDown(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                            self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.running_T2 = True
                if self.movdir2 == 2:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveLeft(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                            self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.running_T2 = True
                if self.movdir2 == 3:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveRight(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                             self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.running_T2 = True

            if not self.moving2:
                if key_pressed[pygame.K_UP]:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveUp(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                          self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.moving2 = 7
                    self.movdir2 = 0
                    self.running_T2 = True
                elif key_pressed[pygame.K_DOWN]:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveDown(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                            self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.moving2 = 7
                    self.movdir2 = 1
                    self.running_T2 = True
                elif key_pressed[pygame.K_LEFT]:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveLeft(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                            self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.moving2 = 7
                    self.movdir2 = 2
                    self.running_T2 = True
                elif key_pressed[pygame.K_RIGHT]:
                    self.allTankGroup.remove(self.myTank_T2)
                    self.myTank_T2.moveRight(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup,
                                             self.bgMap.riverGroup)
                    self.allTankGroup.add(self.myTank_T2)
                    self.moving2 = 7
                    self.movdir2 = 3
                    self.running_T2 = True
            # 如果点击0 则是发射子弹
            if key_pressed[pygame.K_KP0]:
                if not self.myTank_T2.bullet.life:
                    if self.isSoundEffect:
                        self.attack_sound.play()
                    self.myTank_T2.shoot()
                    self.myTank_T2.bulletNotCooling = False

    # 坦克显示函数---------------------------------------------------------
    # 功能：对我方坦克和敌方坦克进行显示
    def tank_display_section(self):
        # 画我方坦克1
        if self.myTank_T1.life > 0:
            if not (self.delay % 5):
                self.switch_R1_R2_image = not self.switch_R1_R2_image
            if self.switch_R1_R2_image and self.running_T1:
                self.screen.blit(self.myTank_T1.tank_R0, (self.myTank_T1.rect.left, self.myTank_T1.rect.top))
                self.running_T1 = False
            else:
                self.screen.blit(self.myTank_T1.tank_R1, (self.myTank_T1.rect.left, self.myTank_T1.rect.top))

            # 画保护罩 坦克1
            if self.invincible_T1 > 0:
                self.invincible_T1 -= 1
                if self.invincible_T1 % 3 == 0:
                    self.special_effect.SE_protect(self.screen, self.myTank_T1.rect.left, self.myTank_T1.rect.top,
                                                   self.invincible_T1)

        # 画我方坦克2
        if self.myTank_T2.life > 0:
            if self.switch_R1_R2_image and self.running_T2:
                self.screen.blit(self.myTank_T2.tank_R0, (self.myTank_T2.rect.left, self.myTank_T2.rect.top))
                self.running_T2 = False
            else:
                self.screen.blit(self.myTank_T2.tank_R1, (self.myTank_T2.rect.left, self.myTank_T2.rect.top))
            # 画保护罩 坦克2
            if self.invincible_T2 > 0:
                self.invincible_T2 -= 1
                if self.invincible_T2 % 3 == 0:
                    self.special_effect.SE_protect(self.screen, self.myTank_T2.rect.left, self.myTank_T2.rect.top,
                                                   self.invincible_T2)

        # 画敌方坦克
        for each in self.allEnemyGroup:
            # 判断5毛钱特效是否播放
            if each.flash:
                # 　判断画左动作还是右动作
                if self.switch_R1_R2_image:
                    self.screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                    # 如果坦克可以移动
                    if self.enemyCouldMove:
                        self.allTankGroup.remove(each)
                        each.move(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup, self.bgMap.riverGroup)
                        self.allTankGroup.add(each)
                else:
                    self.screen.blit(each.tank_R1, (each.rect.left, each.rect.top))
                    if self.enemyCouldMove:
                        self.allTankGroup.remove(each)
                        each.move(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup, self.bgMap.riverGroup)
                        self.allTankGroup.add(each)
            else:
                # 播放5毛钱特效
                if each.times > 0:
                    each.times -= 1
                    self.special_effect.SE_appearance(self.screen, 3 + each.x * 12 * 24, 3, each.times)
                if each.times == 0:
                    each.flash = True

    # 子弹显示函数-------------------------------------------------------------
    # 功能：对子弹进行显示 并检测子弹与子弹 子弹与坦克 子弹和地图碰撞等的操作
    def bullet_section(self):
        # 绘制我方子弹1
        if self.myTank_T1.bullet.life:
            self.myTank_T1.bullet.move()
            self.screen.blit(self.myTank_T1.bullet.bullet, self.myTank_T1.bullet.rect)
            # 子弹 碰撞 子弹
            for each in self.enemyBulletGroup:
                if each.life:
                    if pygame.sprite.collide_rect(self.myTank_T1.bullet, each):
                        self.myTank_T1.bullet.life = False
                        each.life = False
                        pygame.sprite.spritecollide(self.myTank_T1.bullet, self.enemyBulletGroup, True, None)
            # 子弹 碰撞 敌方坦克
            if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.redEnemyGroup, True, None):
                self.prop.change()
                if self.isSoundEffect:
                    self.prop_sound.play()
                self.enemyNumber -= 1
                if not self.isEndless:
                    self.remaining_enemy -= 1
                self.myTank_T1.bullet.life = False
                mid = special_effects.bulletBoom(self.myTank_T1.bullet.rect.left - 12,
                                                 self.myTank_T1.bullet.rect.top - 12)
                self.bulletBoomGroup.append(mid)
            elif pygame.sprite.spritecollide(self.myTank_T1.bullet, self.greenEnemyGroup, False, None):
                for each in self.greenEnemyGroup:
                    if pygame.sprite.collide_rect(self.myTank_T1.bullet, each):
                        if each.life == 1:
                            pygame.sprite.spritecollide(self.myTank_T1.bullet, self.greenEnemyGroup, True, None)
                            if self.isSoundEffect:
                                self.bang_sound.play()
                            self.enemyNumber -= 1
                            if not self.isEndless:
                                self.remaining_enemy -= 1
                        elif each.life == 2:
                            if self.isSoundEffect:
                                self.wall_sound.play()
                            each.life -= 1
                            each.tank = each.enemy_3_0
                        elif each.life == 3:
                            if self.isSoundEffect:
                                self.wall_sound.play()
                            each.life -= 1
                            each.tank = each.enemy_3_2
                self.myTank_T1.bullet.life = False
                mid = special_effects.bulletBoom(self.myTank_T1.bullet.rect.left - 12,
                                                 self.myTank_T1.bullet.rect.top - 12)
                self.bulletBoomGroup.append(mid)
            elif pygame.sprite.spritecollide(self.myTank_T1.bullet, self.otherEnemyGroup, True, None):
                if self.isSoundEffect:
                    self.bang_sound.play()
                self.enemyNumber -= 1
                if not self.isEndless:
                    self.remaining_enemy -= 1
                self.myTank_T1.bullet.life = False
                mid = special_effects.bulletBoom(self.myTank_T1.bullet.rect.left - 12,
                                                 self.myTank_T1.bullet.rect.top - 12)
                self.bulletBoomGroup.append(mid)

            # 子弹 碰撞 brickGroup
            if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.bgMap.brickGroup, True, None):
                if self.isSoundEffect:
                    self.wall_sound.play()
                self.myTank_T1.bullet.life = False
                self.myTank_T1.bullet.rect.left, self.myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            # 子弹 碰撞 ironGroup
            if self.myTank_T1.bullet.strong:
                if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.bgMap.ironGroup, True, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T1.bullet.life = False
                    self.myTank_T1.bullet.rect.left, self.myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.bgMap.ironGroup, False, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T1.bullet.life = False
                    self.myTank_T1.bullet.rect.left, self.myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            # 子弹 碰撞 家
            if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.bgMap.homeGroup, True, None):
                self.overGameLoss = True

        # 绘制我方子弹2 （模仿坦克1写）
        if self.myTank_T2.bullet.life:
            self.myTank_T2.bullet.move()
            self.screen.blit(self.myTank_T2.bullet.bullet, self.myTank_T2.bullet.rect)
            # 子弹 碰撞 敌方坦克
            if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.redEnemyGroup, True, None):
                self.prop.change()
                if self.isSoundEffect:
                    self.prop_sound.play()
                self.enemyNumber -= 1
                if not self.isEndless:
                    self.remaining_enemy -= 1
                self.myTank_T2.bullet.life = False
                mid = special_effects.bulletBoom(self.myTank_T2.bullet.rect.left - 12,
                                                 self.myTank_T2.bullet.rect.top - 12)
                self.bulletBoomGroup.append(mid)
            elif pygame.sprite.spritecollide(self.myTank_T2.bullet, self.greenEnemyGroup, False, None):
                for each in self.greenEnemyGroup:
                    if pygame.sprite.collide_rect(self.myTank_T2.bullet, each):
                        if each.life == 1:
                            pygame.sprite.spritecollide(self.myTank_T2.bullet, self.greenEnemyGroup, True, None)
                            if self.isSoundEffect:
                                self.bang_sound.play()
                            self.enemyNumber -= 1
                            if not self.isEndless:
                                self.remaining_enemy -= 1
                        elif each.life == 2:
                            if self.isSoundEffect:
                                self.wall_sound.play()
                            each.life -= 1
                            each.tank = each.enemy_3_0
                        elif each.life == 3:
                            if self.isSoundEffect:
                                self.wall_sound.play()
                            each.life -= 1
                            each.tank = each.enemy_3_2
                self.myTank_T2.bullet.life = False
                mid = special_effects.bulletBoom(self.myTank_T2.bullet.rect.left - 12,
                                                 self.myTank_T2.bullet.rect.top - 12)
                self.bulletBoomGroup.append(mid)
            elif pygame.sprite.spritecollide(self.myTank_T2.bullet, self.otherEnemyGroup, True, None):
                if self.isSoundEffect:
                    self.bang_sound.play()
                self.enemyNumber -= 1
                if not self.isEndless:
                    self.remaining_enemy -= 1
                self.myTank_T2.bullet.life = False
                mid = special_effects.bulletBoom(self.myTank_T2.bullet.rect.left - 12,
                                                 self.myTank_T2.bullet.rect.top - 12)
                self.bulletBoomGroup.append(mid)

            # 子弹 碰撞 brickGroup
            if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.bgMap.brickGroup, True, None):
                if self.isSoundEffect:
                    self.wall_sound.play()
                self.myTank_T2.bullet.life = False
                self.myTank_T2.bullet.rect.left, self.myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            # 子弹 碰撞 brickGroup
            if self.myTank_T2.bullet.strong:
                if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.bgMap.ironGroup, True, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T2.bullet.life = False
                    self.myTank_T2.bullet.rect.left, self.myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.bgMap.ironGroup, False, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T2.bullet.life = False
                    self.myTank_T2.bullet.rect.left, self.myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                # 子弹 碰撞 家
            if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.bgMap.homeGroup, True, None):
                self.overGameLoss = True
        # 绘制敌人子弹
        for each in self.allEnemyGroup:
            # 如果子弹没有生命，则赋予子弹生命
            if not each.bullet.life and each.bulletNotCooling and self.enemyCouldMove:
                self.enemyBulletGroup.remove(each.bullet)
                each.shoot()
                self.enemyBulletGroup.add(each.bullet)
                each.bulletNotCooling = False
            # 如果5毛钱特效播放完毕 并且 子弹存活 则绘制敌方子弹
            if each.flash:
                if each.bullet.life:
                    # 如果敌人可以移动
                    if self.enemyCouldMove:
                        each.bullet.move()
                    self.screen.blit(each.bullet.bullet, each.bullet.rect)

                    # 子弹 碰撞 我方坦克
                    # 敌方子弹碰撞到我方坦克1
                    if pygame.sprite.collide_rect(each.bullet, self.myTank_T1):
                        if self.invincible_T1 > 0:
                            if self.isSoundEffect:
                                self.bang_sound.play()
                            each.bullet.life = False
                        else:
                            if self.isSoundEffect:
                                self.bang_sound.play()
                            self.myTank_T1.rect.left, self.myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24
                            if not self.isEndless:
                                self.myTank_T1.life -= 1
                            each.bullet.life = False

                            self.moving = 0  # 重置移动控制参数
                            for i in range(self.myTank_T1.level + 1):
                                self.myTank_T1.levelDown()
                            self.invincible_T1 = 200

                    # 敌方子弹碰撞到我方坦克2
                    if pygame.sprite.collide_rect(each.bullet, self.myTank_T2):
                        if self.invincible_T2 > 0:
                            if self.isSoundEffect:
                                self.bang_sound.play()
                            each.bullet.life = False
                        else:
                            if self.isSoundEffect:
                                self.bang_sound.play()
                            self.myTank_T2.rect.left, self.myTank_T2.rect.top = 3 + 16 * 24, 3 + 24 * 24
                            each.bullet.life = False
                            if not self.isEndless:
                                self.myTank_T2.life -= 1
                            self.moving2 = 0  # 重置移动控制参数
                            for i in range(self.myTank_T2.level + 1):
                                self.myTank_T2.levelDown()
                            self.invincible_T2 = 200

                    # 子弹 碰撞 brickGroup
                    if pygame.sprite.spritecollide(each.bullet, self.bgMap.brickGroup, True, None):
                        each.bullet.life = False
                    # 子弹 碰撞 ironGroup
                    if each.bullet.strong:
                        if pygame.sprite.spritecollide(each.bullet, self.bgMap.ironGroup, True, None):
                            each.bullet.life = False
                    else:
                        if pygame.sprite.spritecollide(each.bullet, self.bgMap.ironGroup, False, None):
                            each.bullet.life = False
                            # 子弹 碰撞 家
                    if pygame.sprite.spritecollide(each.bullet, self.bgMap.homeGroup, True, None):
                        self.overGameLoss = True

    # 子弹显示函数(单挑版）--------------------------------------------------------
    # 功能：单挑模式的子弹显示
    def bullet_plate(self):
        # 绘制我方子弹1
        if self.myTank_T1.bullet.life:
            self.myTank_T1.bullet.move()
            self.screen.blit(self.myTank_T1.bullet.bullet, self.myTank_T1.bullet.rect)
            # 子弹 碰撞 子弹
            if self.myTank_T2.bullet.life:
                if pygame.sprite.collide_rect(self.myTank_T1.bullet, self.myTank_T2.bullet):
                    self.myTank_T1.bullet.life = False
                    self.myTank_T2.bullet.life = False

            # 子弹碰撞到我方坦克2
            if pygame.sprite.collide_rect(self.myTank_T1.bullet, self.myTank_T2):
                if self.invincible_T2 > 0:
                    if self.isSoundEffect:
                        self.bang_sound.play()
                    self.myTank_T1.bullet.life = False
                else:
                    if self.isSoundEffect:
                        self.bang_sound.play()
                    self.myTank_T2.rect.left, self.myTank_T2.rect.top = 3 + 12 * 24, 3 + 0 * 24
                    self.myTank_T1.bullet.life = False
                    self.myTank_T2.life -= 1
                    self.moving2 = 0  # 重置移动控制参数
                    for i in range(self.myTank_T2.level + 1):
                        self.myTank_T2.levelDown()
                    self.invincible_T2 = 200

            # 子弹 碰撞 brickGroup
            if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.bgMap.brickGroup, True, None):
                if self.isSoundEffect:
                    self.wall_sound.play()
                self.myTank_T1.bullet.life = False
                self.myTank_T1.bullet.rect.left, self.myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            # 子弹 碰撞 ironGroup
            if self.myTank_T1.bullet.strong:
                if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.bgMap.ironGroup, True, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T1.bullet.life = False
                    self.myTank_T1.bullet.rect.left, self.myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(self.myTank_T1.bullet, self.bgMap.ironGroup, False, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T1.bullet.life = False
                    self.myTank_T1.bullet.rect.left, self.myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24

        # 绘制我方子弹2 （模仿坦克1写）
        if self.myTank_T2.bullet.life:
            self.myTank_T2.bullet.move()
            self.screen.blit(self.myTank_T2.bullet.bullet, self.myTank_T2.bullet.rect)
            # 子弹碰撞到我方坦克1
            if pygame.sprite.collide_rect(self.myTank_T2.bullet, self.myTank_T1):
                if self.invincible_T1 > 0:
                    if self.isSoundEffect:
                        self.bang_sound.play()
                    self.myTank_T2.bullet.life = False
                else:
                    if self.isSoundEffect:
                        self.bang_sound.play()
                    self.myTank_T1.rect.left, self.myTank_T1.rect.top = 3 + 12 * 24, 3 + 24 * 24
                    self.myTank_T1.life -= 1
                    self.myTank_T2.bullet.life = False

                    self.moving = 0  # 重置移动控制参数
                    for i in range(self.myTank_T1.level + 1):
                        self.myTank_T1.levelDown()
                    self.invincible_T1 = 200

            # 子弹 碰撞 brickGroup
            if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.bgMap.brickGroup, True, None):
                if self.isSoundEffect:
                    self.wall_sound.play()
                self.myTank_T2.bullet.life = False
                self.myTank_T2.bullet.rect.left, self.myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            # 子弹 碰撞 brickGroup
            if self.myTank_T2.bullet.strong:
                if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.bgMap.ironGroup, True, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T2.bullet.life = False
                    self.myTank_T2.bullet.rect.left, self.myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(self.myTank_T2.bullet, self.bgMap.ironGroup, False, None):
                    if self.isSoundEffect:
                        self.wall_sound.play()
                    self.myTank_T2.bullet.life = False
                    self.myTank_T2.bullet.rect.left, self.myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24

    # 道具部分函数------------------------------------------------------------
    # 功能：对道具进行更新显示 并当我方碰到道具时会触发不同效果
    def props_section(self):
        # 最后画食物/道具
        if self.prop.life:
            self.screen.blit(self.prop.image, self.prop.rect)
            # 我方坦克碰撞 食物/道具

            # 如果是坦克1碰到道具
            if pygame.sprite.collide_rect(self.myTank_T1, self.prop):
                if self.isSoundEffect:
                    self.get_props_sound.play()
                if self.prop.kind == 1:  # 敌人全毁
                    if self.isSoundEffect:
                        self.prop_boom_sound.play()
                    for each in self.allEnemyGroup:
                        if pygame.sprite.spritecollide(each, self.allEnemyGroup, True, None):
                            self.enemyNumber -= 1
                            if not self.isEndless:
                                self.remaining_enemy -=1
                    self.prop.life = False
                if self.prop.kind == 2:  # 敌人静止
                    self.enemyCouldMove = False
                    self.prop.life = False
                if self.prop.kind == 3:  # 子弹增强
                    self.myTank_T1.bullet.strong = True
                    self.prop.life = False
                if self.prop.kind == 4:  # 家得到保护
                    for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                        self.bgMap.iron = wall.Iron()
                        self.bgMap.iron.rect.left, self.bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                        self.bgMap.ironGroup.add(self.bgMap.iron)
                    self.prop.life = False
                    self.iron_time = 200
                if self.prop.kind == 5:  # 坦克无敌
                    self.prop.life = False
                    self.invincible_T1 = 200
                if self.prop.kind == 6:  # 坦克升级
                    self.myTank_T1.levelUp()
                    self.prop.life = False
                if self.prop.kind == 7:  # 坦克生命+1
                    if self.myTank_T1.life < 3:
                        self.myTank_T1.life += 1
                    self.prop.life = False

            # 如果是坦克二碰到道具
            elif pygame.sprite.collide_rect(self.myTank_T2, self.prop):
                if self.isSoundEffect:
                    self.get_props_sound.play()
                if self.prop.kind == 1:  # 敌人全毁
                    self.prop_boom_sound.play()
                    for each in self.allEnemyGroup:
                        if pygame.sprite.spritecollide(each, self.allEnemyGroup, True, None):
                            self.enemyNumber -= 1
                            if not self.isEndless:
                                self.remaining_enemy -=1
                    self.prop.life = False
                if self.prop.kind == 2:  # 敌人静止
                    self.enemyCouldMove = False
                    self.prop.life = False
                if self.prop.kind == 3:  # 子弹增强
                    self.myTank_T2.bullet.strong = True
                    self.prop.life = False
                if self.prop.kind == 4:  # 家得到保护
                    for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                        self.bgMap.iron = wall.Iron()
                        self.bgMap.iron.rect.left, self.bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                        self.bgMap.ironGroup.add(self.bgMap.iron)
                    self.prop.life = False
                    self.iron_time = 200
                if self.prop.kind == 5:  # 坦克无敌
                    self.prop.life = False
                    self.invincible_T2 = 200
                if self.prop.kind == 6:  # 坦克升级
                    self.myTank_T2.levelUp()
                    self.prop.life = False
                if self.prop.kind == 7:  # 坦克生命+1
                    if self.myTank_T2.life < 3:
                        self.myTank_T2.life += 1
                    self.prop.life = False

    # 游戏运行函数（普通和无尽模式）----------------------------------------------------
    # 功能：运行此函数就将运行游戏
    # 接口：checkpoint就是选择关卡 1-35分别是对应关卡  99则是自建地图
    def game_running(self,checkpoint,isEndless):
        self.isEndless = isEndless
        # 创建地图 但是不用只是当作一个中间变量
        map_num = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # 如果checkpoint是自建关卡
        if checkpoint == 99:
            # 如果返回0则退出 如果返回数组则进行地图创建
            map_loader_me = map_loader.Map_loader()
            mid = map_loader_me.function(True)
            if mid == 0:
                return
            self.bgMap.checkpoint(checkpoint, mid)
        else:
            self.bgMap.checkpoint(checkpoint, map_num)

        # 创建敌方 坦克（在一二三处出现）
        for i in range(1, 4):
            enemy = enemyTank.EnemyTank(i)
            self.allTankGroup.add(enemy)
            self.allEnemyGroup.add(enemy)
            if enemy.isred == True:
                self.redEnemyGroup.add(enemy)
                continue
            if enemy.kind == 3:
                self.greenEnemyGroup.add(enemy)
                continue
            self.otherEnemyGroup.add(enemy)

        # 默认是单人
        self.myTank_T2.life = 0
        self.start_sound.play()
        while True:
            #游戏结束
            if self.remaining_enemy == 0:
                self.overGameWin = True

            if self.overGameLoss:
                mid = self.game_over(2)
                if mid == 0:
                    self.start_sound.stop()
                    return

            if self.overGameWin:
                mid = self.game_over(1)
                if mid == 0:
                    self.start_sound.stop()
                    return
            # 按键操作
            key_pressed = pygame.key.get_pressed()

            # 按esc退出游戏
            if key_pressed[pygame.K_ESCAPE]:
                self.start_sound.stop()
                return

            # 按F1复活玩家1
            if key_pressed[pygame.K_F1] and self.myTank_T1.life == 0:
                self.myTank_T1.life = 3
                self.myTank_T1.rect.left, self.myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24
                if self.isSoundEffect:
                    self.add_sound.play()
            # 按F2复活玩家2
            if key_pressed[pygame.K_F2] and self.myTank_T2.life == 0:
                self.myTank_T2.life = 3
                self.myTank_T2.rect.left, self.myTank_T2.rect.top = 3 + 16 * 24, 3 + 24 * 24
                if self.isSoundEffect:
                    self.add_sound.play()
            # 如果玩家死亡
            if self.myTank_T1.life == 0:
                self.myTank_T1.rect.left, self.myTank_T1.rect.top = 630, 0
            if self.myTank_T2.life == 0:
                self.myTank_T2.rect.left, self.myTank_T2.rect.top = 680, 0
            # --------------------------------------------------------------------------
            # 处理事件部分 主要就是各个事件的时间
            # ---------------------------------------------------------------------------
            self.event_section()

            # 检查用户的键盘操作
            # ----------------------------------------------------------------------------
            # 移动操作 -------------------------------------------------------------------
            self.operation_detection_section()
            # --------------------------------------------------------------------------
            # 画图像操作 ----------------------------------------------------------------
            # -------------------------------------------------------------------------
            while self.iron_time > 0:
                self.iron_time -= 1
                if self.iron_time == 1:
                    for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                        self.bgMap.brick = wall.Brick()
                        self.bgMap.brick.rect.left, self.bgMap.brick.rect.top = 3 + x * 24, 3 + y * 24
                        self.bgMap.brickGroup.add(self.bgMap.brick)

            # 画背景
            self.screen.blit(self.background_image, (0, 0))
            if self.isEndless:
                self.screen.blit(self.background_image_endless_mode, (630, 0))
            else:
                self.screen.blit(self.background_image_level_mode, (630, 0))
            # 画砖块
            for each in self.bgMap.brickGroup:
                self.screen.blit(each.image, each.rect)
            # 画石头
            for each in self.bgMap.ironGroup:
                self.screen.blit(each.image, each.rect)
            # 画河流
            for each in self.bgMap.riverGroup:
                self.screen.blit(each.image, each.rect)
            # 画冰川
            for each in self.bgMap.iceGroup:
                self.screen.blit(each.image, each.rect)
            # 画home
            for each in self.bgMap.homeGroup:
                self.screen.blit(each.image, each.rect)

            if not self.isEndless:
                # 画敌军图标
                for i in range(0,self.remaining_enemy):
                    if i in range(0,10):
                        x = 630 + 25
                        y = 80 + i*30
                        self.screen.blit(self.enemy_icon,(x,y))
                    else:
                        x = 630 + 65
                        y = 80 + (i-10)*30
                        self.screen.blit(self.enemy_icon, (x, y))

                # 画1P生命
                for i in range(0,self.myTank_T1.life):
                    x = 680 + i*20
                    self.screen.blit(self.heart_icon, (x, 378+5))

                # 画2P生命
                for i in range(0, self.myTank_T2.life):
                    x = 680 + i * 20
                    self.screen.blit(self.heart_icon, (x, 378+55))
            # --------------------------------------------------------------
            # 画坦克---------------------------------------------------------
            # --------------------------------------------------------------
            self.tank_display_section()
            # ................................................................................
            # 子弹区域..........................................................................
            # .................................................................................
            self.bullet_section()
            # 画树 因为树在表层所有在后面画
            for each in self.bgMap.treeGroup:
                self.screen.blit(each.image, each.rect)

            # 画爆炸特效
            for each in self.bulletBoomGroup:
                if each.times > 0:
                    each.times -= 1
                    if each.times % 10 == 0:
                        self.special_effect.SE_boom(self.screen,each.x,each.y,each.times)
                else:
                    self.bulletBoomGroup.remove(each)
            # ----------------------------------------------------------------
            # 画道具-----------------------------------------------------------
            # ----------------------------------------------------------------
            self.props_section()

            # 延迟
            self.delay -= 1
            if not self.delay:
                self.delay = 100
            pygame.display.flip()
            self.clock.tick(60)

    # 游戏运行函数 （单挑模式）----------------------------------------------------------
    # 功能：运行测函数就是运行单挑模式的功能
    # 接口：checkpoint就是选择关卡
    def game_running_singled_out(self,checkpoint):
        # 创建地图
        map_num = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # 如果checkpoint是自建关卡
        if checkpoint == 88:
            map_loader_me = map_loader.Map_loader()
            mid = map_loader_me.function(False)
            if mid == 0:
                return
            self.bgMap.checkpoint(checkpoint, mid)
        else:
            self.bgMap.checkpoint(checkpoint, map_num)

        self.myTank_T1.rect.left , self.myTank_T1.rect.top = 3 + 12 * 24, 3 + 24 * 24
        self.myTank_T2.rect.left , self.myTank_T2.rect.top = 3 + 12 * 24, 3 + 0 * 24
        self.start_sound.play()
        while True:

            if self.myTank_T1.life == 0:
                mid = self.game_over(4)
                if mid == 0:
                    return

            if self.myTank_T2.life == 0:
                mid = self.game_over(3)
                if mid == 0:
                    return
            # 按键操作
            key_pressed = pygame.key.get_pressed()
            # 按esc退出游戏
            if key_pressed[pygame.K_ESCAPE]:
                self.start_sound.stop()
                return

            self.event_section_singled_out()

            # 检查用户的键盘操作
            # ----------------------------------------------------------------------------
            # 移动操作 -------------------------------------------------------------------
            self.operation_detection_section()
            # --------------------------------------------------------------------------
            # 画图像操作 ----------------------------------------------------------------
            # -------------------------------------------------------------------------

            # 画背景
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.background_image_heads_up_mode, (630, 0))

            # 画砖块
            for each in self.bgMap.brickGroup:
                self.screen.blit(each.image, each.rect)
            # 画石头
            for each in self.bgMap.ironGroup:
                self.screen.blit(each.image, each.rect)
            # 画河流
            for each in self.bgMap.riverGroup:
                self.screen.blit(each.image, each.rect)

            # 画冰川
            for each in self.bgMap.iceGroup:
                self.screen.blit(each.image, each.rect)
            for i in range(0, self.myTank_T1.life):
                x = 680 + i * 20
                self.screen.blit(self.heart_icon, (x, 290 + 5))

            # 画2P生命
            for i in range(0, self.myTank_T2.life):
                x = 680 + i * 20
                self.screen.blit(self.heart_icon, (x, 290 + 55))
            # --------------------------------------------------------------
            # 画坦克---------------------------------------------------------
            # --------------------------------------------------------------
            self.tank_display_section()
            # ................................................................................
            # 子弹区域..........................................................................
            # .................................................................................
            self.bullet_plate()

            # 画树
            for each in self.bgMap.treeGroup:
                self.screen.blit(each.image, each.rect)
            # 画爆炸特效
            for each in self.bulletBoomGroup:
                if each.times > 0:
                    each.times -= 1
                    if each.times % 10 == 0:
                        self.special_effect.SE_boom(self.screen, each.x, each.y, each.times)
                else:
                    self.bulletBoomGroup.remove(each)

            # 延迟
            self.delay -= 1
            if not self.delay:
                self.delay = 100
            pygame.display.flip()

            self.clock.tick(60)

##############################################################
##############################################################
# 
# Following code are written by us
#
##############################################################
##############################################################
 
    # function to get the current state of the game
    # state: [player_x, player_y, player_life, enemy1_x, enemy1_y, enemy1_life, ...]
    def get_current_state(self, enemy_num):
        state = [
            self.myTank_T1.rect.left / 630,
            self.myTank_T1.rect.top / 630,
            self.myTank_T1.life,
        ]
        for enemy in self.allEnemyGroup:
            state.extend([
                enemy.rect.left / 630,
                enemy.rect.top / 630,
                enemy.life
            ])
        while len(state) < 3 + 3 * enemy_num:
            state.append(0)
        return np.array(state, dtype=np.float32).reshape(1, -1)
    
    # function to get successor state after applying the action
    # Returns a new state object, reward, done flag, and observation
    # Reference: https://gist.github.com/SeanMirchi/46c88e82fdf579a5e3bbfa0eb0a2277d
    def get_successor_state(self, action, enemy_num):

        # Create a copy of the current state
        old_state = self.get_current_state(enemy_num)
        self.execute_action(action)
        self.event_section()
        self.bullet_section()
        self.props_section()
        self.tank_display_section()

        new_state = self.get_current_state(enemy_num)
        reward = self.reward_calculation(old_state, new_state)
        done = (self.remaining_enemy == 0) or self.overGameLoss or (self.myTank_T1.life <= 0)
        observation = new_state

        return new_state, reward, done, observation

    # function to calculate the reward based on the state transition
    def reward_calculation(self, old_state, new_state):
        reward = 0

        # 1. If the game is over, return a large negative reward.
        if self.overGameLoss:
            return -100
        
        # 2. If the player wins the game, return a large positive reward. 
        if self.remaining_enemy == 0 or getattr(self, "overGameWin", False):
            return 300 
        
        # 3. If the player's tank is destroyed, add a negative reward
        if self.myTank_T1.life < old_state[0][2]:
            reward -= 50

        # 4. If the enemy tank is destroyed, add a positive reward.
        old_enemy_count = sum([old_state[0][i+2] for i in range(3, len(old_state[0]), 3) if old_state[0][i+2] > 0])
        new_enemy_count = sum([new_state[0][i+2] for i in range(3, len(new_state[0]), 3) if new_state[0][i+2] > 0])
        if new_enemy_count < old_enemy_count:
            reward += 20

        # 5. If the player moves closer to the enemy, add a small positive reward
        px_new, py_new = new_state[0][0], new_state[0][1]
        min_dist_new = float('inf')
        for i in range(3, len(new_state[0]), 3):
            ex, ey, elife = new_state[0][i], new_state[0][i+1], new_state[0][i+2]
            if elife > 0:
                dist = abs(px_new - ex) + abs(py_new - ey)
                if dist < min_dist_new:
                    min_dist_new = dist

        px_old, py_old = old_state[0][0], old_state[0][1]
        min_dist_old = float('inf')
        for i in range(3, len(old_state[0]), 3):
            ex, ey, elife = old_state[0][i], old_state[0][i+1], old_state[0][i+2]
            if elife > 0:
                dist = abs(px_old - ex) + abs(py_old - ey)
                if dist < min_dist_old:
                    min_dist_old = dist

        # make sure the agent is moveing
        if min_dist_new < min_dist_old and (px_new != px_old or py_new != py_old):
            reward += 0.05

        return reward
    
    # We create a function similar to game_running and game_running_singled_out func to let AI play the game 
    def game_running_ai_play(self, agent, enemy_num=1, checkpoint=1, isEndless=False):
        print("\n=== AI Play Start ===")

        # initialize game state
        self.allTankGroup.empty()
        self.mytankGroup.empty()
        self.allEnemyGroup.empty()
        self.redEnemyGroup.empty()
        self.greenEnemyGroup.empty()
        self.otherEnemyGroup.empty()
        self.enemyBulletGroup.empty()
        self.bgMap.brickGroup.empty()
        self.bgMap.ironGroup.empty()
        self.bgMap.riverGroup.empty()
        self.bgMap.iceGroup.empty()
        self.bgMap.homeGroup.empty()
        self.bgMap.treeGroup.empty()
        self.bulletBoomGroup.clear()
        self.prop.life = 0  

        self.overGameLoss = False
        self.overGameWin = False
        self.enemyCouldMove = True
        self.invincible_T1 = 0
        self.invincible_T2 = 0
        self.iron_time = 0
        self.delay = 100

        self.isEndless = isEndless
        map_num = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        # let AI play the 1-35 levels of the game
        # checkpoint = random.randint(1, 35)

        # Here we just set the checkpoint from given parameter
        checkpoint = checkpoint
        self.bgMap.checkpoint(checkpoint, map_num)

        for i in range(1, enemy_num + 1):
            enemy = enemyTank.EnemyTank(i, kind = 1)
            self.allTankGroup.add(enemy)
            self.allEnemyGroup.add(enemy)
            if enemy.isred:
                self.redEnemyGroup.add(enemy)
            elif enemy.kind == 3:
                self.greenEnemyGroup.add(enemy)
            else:
                self.otherEnemyGroup.add(enemy)

        self.myTank_T2.life = 0
        self.myTank_T1.life = 3
        self.myTank_T1.rect.left, self.myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24
        self.overGameLoss = False
        self.overGameWin = False
        self.enemyCouldMove = True
        self.remaining_enemy = len(self.allEnemyGroup)
        self.enemyNumber = enemy_num
        self.invincible_T1 = 0
        self.invincible_T2 = 0
        self.iron_time = 0


        done = False
        while not done:
            self.event_section()

            # AI action
            state = self.get_current_state(enemy_num)
            state = np.array(state, dtype=np.float32).reshape(1, -1)
            action = agent.act(state)

            self.execute_action(action)

            self.bullet_section()
            self.props_section()

            # Check win/lose
            if self.remaining_enemy == 0:
                self.overGameWin = True
                print("AI winning!")
                done = True
            elif self.overGameLoss or self.myTank_T1.life <= 0:
                print("AI losing!")
                done = True

            # render the game screen
            self.render_game_screen()

        print("AI Play End")

    # this function is used to train the AI agent
    def game_running_ai_trainning(self, agent, episodes=500, batch_size=8, enemy_num=1, checkpoint=1, isEndless=False, show_training=True, file_name="default.keras"):

        print("\n=== AI Training Start ===")
        # we use a rule based approach to fasten the training process
        # But the probability of using the rule based approach will decrease over time till less than 0.1
        rule_prob = 0.5
        for episode in range(episodes):
            if rule_prob < 0.1:
                rule_prob = rule_prob*0.9

            # print the progress of training
            print(f"\n=== Episode {episode + 1}/{episodes} ===")
            start_time = time.time() 

            self.allTankGroup.empty()
            self.mytankGroup.empty()
            self.allEnemyGroup.empty()
            self.redEnemyGroup.empty()
            self.greenEnemyGroup.empty()
            self.otherEnemyGroup.empty()
            self.enemyBulletGroup.empty()
            self.bgMap.brickGroup.empty()
            self.bgMap.ironGroup.empty()
            self.bgMap.riverGroup.empty()
            self.bgMap.iceGroup.empty()
            self.bgMap.homeGroup.empty()
            self.bgMap.treeGroup.empty()
            self.bulletBoomGroup.clear()
            self.prop.life = 0  

            self.overGameLoss = False
            self.overGameWin = False
            self.enemyCouldMove = True
            self.invincible_T1 = 0
            self.invincible_T2 = 0
            self.iron_time = 0
            self.delay = 100

            self.isEndless = isEndless
            
            map_num = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
            
            # checkpoint = random.randint(1, 35)
            
            # Here I just set the checkpoint from given parameter
            checkpoint = checkpoint
            self.bgMap.checkpoint(checkpoint, map_num)

            for i in range(1, enemy_num + 1):
                enemy = enemyTank.EnemyTank(i, kind=1)
                self.allTankGroup.add(enemy)
                self.allEnemyGroup.add(enemy)
                if enemy.isred:
                    self.redEnemyGroup.add(enemy)
                elif enemy.kind == 3:
                    self.greenEnemyGroup.add(enemy)
                else:
                    self.otherEnemyGroup.add(enemy)
            self.myTank_T2.life = 0
            self.myTank_T1.life = 3
            self.myTank_T1.rect.left, self.myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24
            self.overGameLoss = False
            self.overGameWin = False
            self.enemyCouldMove = True
            self.remaining_enemy = len(self.allEnemyGroup)
            self.enemyNumber = enemy_num
            self.invincible_T1 = 0
            self.invincible_T2 = 0
            self.iron_time = 0

            # set the maximum number of steps so each episode won't take too much time
            max_steps = 1000

            # initialze the training variables
            total_reward = 0
            step_count = 0
            done = False

            state = self.get_current_state(enemy_num)
            # game not over
            while not done:
                action = agent.act(state)
                next_state, reward, done, _ = self.get_successor_state(action, enemy_num)

                agent.remember(state, action, reward, next_state, done)
                state = next_state

                step_count += 1

                # I changed to train the agent every 10 step to speed up the training process
                if step_count % 10 == 0:
                    agent.replay(batch_size)

                # update the target model every 100 steps
                if step_count % 100 == 0:
                    agent.update_target_model()

                # update the total reward
                total_reward += reward
                
                # choose to render the game screen or not
                if show_training:
                    self.render_game_screen()

                # I removed the delay and clock.tick(60) to speed up the training process
                # self.clock.tick(60)
                
                # if steps exceed the maximum steps, terminate the episode
                if step_count >= max_steps:
                    print("Episode terminated due to step limit.")
                    break
            
            # train the remaining steps (<10 steps)
            agent.replay(batch_size)
            # update the epsilon
            if agent.epsilon > agent.epsilon_min:
                agent.epsilon *= agent.epsilon_decay

            end_time = time.time() 
            elapsed = end_time - start_time
            print(f"Episode {episode + 1} finished. Total reward: {total_reward}. Time: {elapsed:.2f} seconds")
            agent.save(file_name)
            print("Epsilon:", agent.epsilon)
            print("Model saved.")
            
            with open("tank_dqn_replay.pkl", "wb") as f:
                pickle.dump(agent.memory, f)
            print("Replay buffer saved.")


        agent.save(file_name)
        print("Final model saved.")

    # Teach the ai agent basic actions to play the game so it don't need to learn from too many random actions;
    def rule_based_act(self):

        # 1. Try to shoot if any enemy is on same row or column
        px, py = self.myTank_T1.rect.left, self.myTank_T1.rect.top
        for enemy in self.allEnemyGroup:
            ex, ey = enemy.rect.left, enemy.rect.top
            if abs(px - ex) < 12 or abs(py - ey) < 12:
                blocked = False
                if abs(px - ex) < 12:
                    y_range = range(min(py, ey) + 24, max(py, ey), 24)
                    for y in y_range:
                        for block in list(self.bgMap.brickGroup) + list(self.bgMap.ironGroup):
                            if abs(block.rect.left - px) < 12 and abs(block.rect.top - y) < 12:
                                blocked = True
                                break
                        if blocked:
                            break
                    if not blocked:
                        if ey < py and (self.myTank_T1.dir_x, self.myTank_T1.dir_y) != (0, -1):
                            return 0
                        elif ey > py and (self.myTank_T1.dir_x, self.myTank_T1.dir_y) != (0, 1):
                            return 1
                        else:
                            return 4
                else:
                    x_range = range(min(px, ex) + 24, max(px, ex), 24)
                    for x in x_range:
                        for block in list(self.bgMap.brickGroup) + list(self.bgMap.ironGroup):
                            if abs(block.rect.left - x) < 12 and abs(block.rect.top - py) < 12:
                                blocked = True
                                break
                        if blocked:
                            break
                    if not blocked:
                        if ex < px and (self.myTank_T1.dir_x, self.myTank_T1.dir_y) != (-1, 0):
                            return 2
                        elif ex > px and (self.myTank_T1.dir_x, self.myTank_T1.dir_y) != (1, 0):
                            return 3
                        else:
                            return 4

        # 2. Move towards the nearest enemy
        min_dist = float('inf')
        target_dir = 4  # default = fire

        for enemy in self.allEnemyGroup:
            ex, ey = enemy.rect.left, enemy.rect.top
            dist = abs(px - ex) + abs(py - ey)
            if dist < min_dist:
                min_dist = dist
                if abs(px - ex) > abs(py - ey):
                    target_dir = 2 if ex < px else 3
                else:
                    target_dir = 0 if ey < py else 1 
        
        return target_dir
                                            
    # the game screen rendering function is pulled out from the game_running function
    def render_game_screen(self):
        # render the background
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.background_image_level_mode, (630, 0))

        # render the elements on the screen
        for each in self.bgMap.brickGroup:
            self.screen.blit(each.image, each.rect)
        for each in self.bgMap.ironGroup:
            self.screen.blit(each.image, each.rect)
        for each in self.bgMap.riverGroup:
            self.screen.blit(each.image, each.rect)
        for each in self.bgMap.iceGroup:
            self.screen.blit(each.image, each.rect)
        for each in self.bgMap.homeGroup:
            self.screen.blit(each.image, each.rect)
        for each in self.bgMap.treeGroup:
            self.screen.blit(each.image, each.rect)

        # render bullet explosion effects
        for each in self.bulletBoomGroup:
            if each.times > 0:
                each.times -= 1
                if each.times % 10 == 0:
                    self.special_effect.SE_boom(self.screen, each.x, each.y, each.times)
            else:
                self.bulletBoomGroup.remove(each)
        # render the props
        self.props_section()
        # render the tanks
        self.tank_display_section()

        # render the life icons for the player's tank
        for i in range(self.myTank_T1.life):
            x = 680 + i * 20
            y = 378 + 5  
            self.screen.blit(self.heart_icon, (x, y))

        # render the life icons for the enemy tanks
        for i in range(self.remaining_enemy):
            if i < 10:
                x = 630 + 25
                y = 80 + i * 30
            else:
                x = 630 + 65
                y = 80 + (i - 10) * 30
            self.screen.blit(self.enemy_icon, (x, y))
        pygame.display.flip()

    # update the game state based on the action taken
    def execute_action(self, action):
        self.allTankGroup.remove(self.myTank_T1)
        if action == 0:
            self.myTank_T1.moveUp(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup, self.bgMap.riverGroup)
        elif action == 1:
            self.myTank_T1.moveDown(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup, self.bgMap.riverGroup)
        elif action == 2:
            self.myTank_T1.moveLeft(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup, self.bgMap.riverGroup)
        elif action == 3:
            self.myTank_T1.moveRight(self.allTankGroup, self.bgMap.brickGroup, self.bgMap.ironGroup, self.bgMap.riverGroup)
        elif action == 4:
            if not self.myTank_T1.bullet.life and self.myTank_T1.bulletNotCooling:
                if self.isSoundEffect:
                    self.attack_sound.play()
                self.myTank_T1.shoot()
                self.myTank_T1.bulletNotCooling = False
        self.allTankGroup.add(self.myTank_T1)