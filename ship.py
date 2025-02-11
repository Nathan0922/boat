import pygame
import sys
from pygame.locals import *

# 初始化 pygame
pygame.init()

# 設定視窗與顏色
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 創建視窗
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("船隻模擬")

# 定義按鈕區域
button_rects = {
    "kite": pygame.Rect(50, 500, 100, 50),
    "circle": pygame.Rect(200, 500, 100, 50),
    "arrow": pygame.Rect(350, 500, 100, 50),
}

# 初始化船隻數據
leader_pos = [400, 300]  # 領導船位置
follower_positions = [[leader_pos[0] + offset[0], leader_pos[1] + offset[1]] for offset in [[-60, -30], [-60, 30], [-120, -60], [-120, 60]]]

follower_targets = follower_positions.copy()  # 跟隨船目標位置
speed = [0, 0]  # 領導船初始速度
formation = "line"  # 預設隊形

# 繪製按鈕
def draw_buttons():
    pygame.draw.rect(screen, BLUE, button_rects["kite"])
    pygame.draw.rect(screen, BLUE, button_rects["circle"])
    pygame.draw.rect(screen, BLUE, button_rects["arrow"])

    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render("Kite", True, WHITE), (button_rects["kite"].x + 15, button_rects["kite"].y + 10))
    screen.blit(font.render("Circle", True, WHITE), (button_rects["circle"].x + 10, button_rects["circle"].y + 10))
    screen.blit(font.render("Arrow", True, WHITE), (button_rects["arrow"].x + 10, button_rects["arrow"].y + 10))

# 更新跟隨船目標位置
def update_targets(leader_pos, formation):
    if formation == "kite":
        return [[leader_pos[0] - 60, leader_pos[1] - 30],
                [leader_pos[0] - 60, leader_pos[1] + 30],
                [leader_pos[0] - 120, leader_pos[1] - 60],
                [leader_pos[0] - 120, leader_pos[1] + 60]]
    elif formation == "circle":
        return [[leader_pos[0] - 60, leader_pos[1]],
                [leader_pos[0] + 60, leader_pos[1]],
                [leader_pos[0], leader_pos[1] - 60],
                [leader_pos[0], leader_pos[1] + 60]]
    elif formation == "arrow":
        return [[leader_pos[0] - 60, leader_pos[1] - 30],
                [leader_pos[0] - 60, leader_pos[1] + 30],
                [leader_pos[0] - 120, leader_pos[1] - 15],
                [leader_pos[0] - 120, leader_pos[1] + 15]]
    else:  # 默認直線排列
        return [[leader_pos[0] - 60 * (i + 1), leader_pos[1]] for i in range(4)]

# 平滑移動（線性插值）
def lerp(start, end, t):
    return start + (end - start) * t

# 遊戲主迴圈
while True:
    screen.fill(WHITE)

    # 處理事件
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if button_rects["kite"].collidepoint(event.pos):
                formation = "kite"
            elif button_rects["circle"].collidepoint(event.pos):
                formation = "circle"
            elif button_rects["arrow"].collidepoint(event.pos):
                formation = "arrow"

    # 處理鍵盤輸入
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        speed[0] -= 0.5  # 向左
    if keys[K_d]:
        speed[0] += 0.5  # 向右
    if keys[K_w]:
        speed[1] -= 0.5  # 向左
    if keys[K_s]:
        speed[1] += 0.5  # 向右

    # 更新領導船位置
    leader_pos[0] += speed[0]
    leader_pos[1] += speed[1]

    # 確保領導船不會超出邊界
    leader_pos[0] = max(0, min(WINDOW_WIDTH, leader_pos[0]))
    leader_pos[1] = max(0, min(WINDOW_HEIGHT, leader_pos[1]))

    # 更新跟隨船目標位置
    follower_targets = update_targets(leader_pos, formation)

    # 平滑移動跟隨船
    for i in range(len(follower_positions)):
        follower_positions[i][0] = lerp(follower_positions[i][0], follower_targets[i][0], 0.05)
        follower_positions[i][1] = lerp(follower_positions[i][1], follower_targets[i][1], 0.05)

    # 繪製船隻
    pygame.draw.circle(screen, BLACK, leader_pos, 10)  # 領導船
    for pos in follower_positions:
        pygame.draw.circle(screen, BLUE, (int(pos[0]), int(pos[1])), 10)  # 跟隨船

    # 繪製按鈕
    draw_buttons()

    # 更新畫面
    pygame.display.update()

    # 控制幀率
    pygame.time.Clock().tick(60)
