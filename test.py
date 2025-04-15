import pygame
from game_loader import Game  # 假设上面代码保存在game.py中
import enemyTank

# 初始化游戏对象
game = Game()
game.bgMap.checkpoint(1, [[0]*26 for _ in range(26)])  # 使用默认空白地图进行测试

# 创建敌方坦克，方便测试
for i in range(1, 4):
    enemy = enemyTank.EnemyTank(i)
    game.allTankGroup.add(enemy)
    game.allEnemyGroup.add(enemy)

# 测试_get_game_state
state = game.get_game_state()
print("Initial state:", state)

# 模拟一个动作 (0:上, 1:下, 2:左, 3:右, 4:射击)
actions = [4, 4, 4, 4, 4]  # 上→右→右→射击→下→左

# 测试动作序列
for action in actions:
    game.update_game_with_action(action)
    # 更新游戏画面
    game.screen.blit(game.background_image, (0, 0))
    game.tank_display_section()
    pygame.display.flip()
    pygame.event.pump()  # 防止pygame无响应
    pygame.time.wait(5000)  # 等待0.5秒以便观察效果

    # 输出当前状态
    state = game.get_game_state()
    print("State after action", action, ":", state)

pygame.quit()
