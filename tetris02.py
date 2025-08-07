import pygame
import random

# 1. 초기 설정
pygame.init()

# 색상 정의 (RGB 값)
# 게임 배경 및 블록 색상을 깔끔하게 표현합니다.
COLORS = {
    0: (0, 0, 0),    # 배경 (검은색)
    1: (0, 255, 255), # I 블록 (하늘색)
    2: (0, 0, 255),   # J 블록 (파란색)
    3: (255, 165, 0), # L 블록 (주황색)
    4: (255, 255, 0), # O 블록 (노란색)
    5: (0, 255, 0),   # S 블록 (초록색)
    6: (128, 0, 128), # T 블록 (보라색)
    7: (255, 0, 0)    # Z 블록 (빨간색)
}

# 테트리스 블록 모양 (각 블록 타입과 회전 형태 정의)
# 각 블록은 (x, y) 좌표 쌍으로 구성됩니다.
SHAPES = {
    'I': [[(0,0), (1,0), (2,0), (3,0)],  # 가로
          [(0,0), (0,1), (0,2), (0,3)]], # 세로
    'J': [[(0,1), (1,1), (2,1), (2,0)],
          [(1,0), (1,1), (1,2), (2,2)],
          [(0,1), (0,2), (1,2), (2,2)],
          [(0,0), (1,0), (1,1), (1,2)]],
    'L': [[(0,1), (1,1), (2,1), (0,0)],
          [(1,0), (1,1), (1,2), (2,0)],
          [(0,2), (1,2), (2,2), (2,1)],
          [(0,2), (1,0), (1,1), (1,2)]],
    'O': [[(0,0), (1,0), (0,1), (1,1)]], # 정사각형은 회전해도 동일
    'S': [[(1,0), (2,0), (0,1), (1,1)],
          [(0,0), (0,1), (1,1), (1,2)]],
    'T': [[(0,1), (1,1), (2,1), (1,0)],
          [(1,0), (1,1), (1,2), (0,1)],
          [(0,1), (1,1), (2,1), (1,2)],
          [(1,0), (1,1), (1,2), (2,1)]],
    'Z': [[(0,0), (1,0), (1,1), (2,1)],
          [(1,0), (0,1), (1,1), (0,2)]]
}

# 게임 화면 설정
CELL_SIZE = 30           # 각 칸의 크기 (픽셀)
GRID_WIDTH = 10          # 테트리스 필드 가로 칸 수
GRID_HEIGHT = 20         # 테트리스 필드 세로 칸 수
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + 200 # 게임 필드 + 추가 정보(다음 블록, 점수) 표시 영역
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
GAME_FIELD_X = (SCREEN_WIDTH - 200 - GRID_WIDTH * CELL_SIZE) // 2 # 게임 필드 시작 x 좌표
GAME_FIELD_Y = 0 # 게임 필드 시작 y 좌표

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Buddy's Tetris 🎮")

# 폰트 설정 (깔끔한 GUI를 위해 기본 시스템 폰트 사용)
FONT = pygame.font.SysFont('gothic', 24) # 한글 지원을 위해 'malgungothic' 사용

# 2. Tetromino 클래스 정의
class Tetromino:
    def __init__(self, shape_type, color_id, x, y):
        self.shape_type = shape_type
        self.shapes = SHAPES[shape_type]
        self.rotation_index = 0 # 현재 블록의 회전 상태
        self.color = COLORS[color_id] # 블록의 색상
        self.color_id = color_id # <-- 이 부분을 추가했습니다!
        self.x = x # 블록의 현재 x 좌표 (칸 단위)
        self.y = y # 블록의 현재 y 좌표 (칸 단위)

    def get_current_shape(self):
        # 현재 회전 상태에 맞는 블록 모양을 반환
        return self.shapes[self.rotation_index]

    def rotate(self):
        # 블록을 회전
        self.rotation_index = (self.rotation_index + 1) % len(self.shapes)

    def move(self, dx, dy):
        # 블록을 이동
        self.x += dx
        self.y += dy

# 3. TetrisGame 클래스 정의 (게임 로직 관리)
class TetrisGame:
    def __init__(self):
        # 게임 필드를 0으로 초기화 (0은 빈 칸을 의미)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_block = self.new_block() # 현재 떨어지는 블록
        self.next_block = self.new_block()   # 다음에 나올 블록
        self.game_over = False               # 게임 종료 여부
        self.score = 0                       # 점수
        self.level = 1                       # 레벨
        self.fall_time = 0                   # 블록이 떨어진 시간
        self.fall_speed = 500                # 블록이 자동으로 떨어지는 속도 (밀리초)

    def new_block(self):
        # 새 블록 생성 (랜덤)
        shape_type = random.choice(list(SHAPES.keys()))
        # SHAPES.keys() 리스트의 인덱스를 사용하여 COLORS 딕셔너리의 키(color_id)를 가져옵니다.
        # 인덱스가 0부터 시작하고 COLORS 키가 0(배경)을 제외한 1부터 시작하므로 +1 해줍니다.
        color_id = list(SHAPES.keys()).index(shape_type) + 1
        # 블록 초기 위치: 필드 중앙 상단
        return Tetromino(shape_type, color_id, GRID_WIDTH // 2 - 2, 0)

    def check_collision(self, block, dx=0, dy=0):
        # 블록이 이동하거나 회전했을 때 다른 블록이나 벽과 충돌하는지 확인
        for x_offset, y_offset in block.get_current_shape():
            x, y = block.x + x_offset + dx, block.y + y_offset + dy
            # 필드 경계 밖이거나 이미 채워진 칸과 겹치면 충돌
            if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.grid[y][x] == 0):
                # 단, 블록이 떨어지기 전에는 grid[-1] 같은 인덱스 에러가 발생할 수 있으므로,
                # y좌표가 0보다 작은 경우는 무시하도록 조건을 추가할 수 있습니다. (시작 위치 때문)
                if y < 0: continue # 블록이 아직 필드 위에서 시작하는 경우
                return True
        return False

    def lock_block(self):
        # 현재 블록을 게임 필드에 고정
        for x_offset, y_offset in self.current_block.get_current_shape():
            x, y = self.current_block.x + x_offset, self.current_block.y + y_offset
            if y < 0: # 블록이 맨 위에서 굳어져 게임 오버 상황
                self.game_over = True
                return
            self.grid[y][x] = self.current_block.color_id # <-- 이 부분을 수정했습니다!
        self.clear_lines() # 줄 제거 확인

    def clear_lines(self):
        # 완성된 줄을 찾아서 제거하고 점수 획득
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if 0 not in row: # 0이 없으면 모든 칸이 채워진 완성된 줄
                lines_cleared += 1
            else:
                new_grid.append(row)
        # 완성된 줄 수만큼 빈 줄을 위에서 추가
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        self.grid = new_grid

        # 점수 및 레벨 계산 (테트리스 공식에 따름)
        if lines_cleared == 1: self.score += 100 * self.level
        elif lines_cleared == 2: self.score += 300 * self.level
        elif lines_cleared == 3: self.score += 500 * self.level
        elif lines_cleared == 4: self.score += 800 * self.level # 테트리스!

        self.level = 1 + self.score // 1000 # 1000점당 레벨업
        # 레벨업에 따라 낙하 속도 조절
        self.fall_speed = max(50, 500 - (self.level - 1) * 50) # 최소 속도 50ms

    def update_game_state(self, dt):
        # 게임 상태 업데이트 (블록 낙하, 충돌 등)
        if self.game_over: return

        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.check_collision(self.current_block, dy=1):
                self.current_block.move(0, 1) # 아래로 한 칸 이동
            else:
                self.lock_block() # 충돌 발생 시 블록 고정
                if not self.game_over: # 게임 오버가 아닐 때만 다음 블록 생성
                    self.current_block = self.next_block
                    self.next_block = self.new_block()
                    # 새 블록 생성 후 즉시 충돌 확인 (시작 위치에 이미 블록이 있으면 게임 오버)
                    if self.check_collision(self.current_block):
                        self.game_over = True

    # 4. 그리기 함수
    def draw_grid(self):
        # 게임 필드 배경을 그립니다.
        pygame.draw.rect(SCREEN, (50, 50, 50), (GAME_FIELD_X, GAME_FIELD_Y, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        # 그리드 선을 그립니다 (깔끔한 시각화를 위해 회색 선 사용)
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(SCREEN, (70, 70, 70), (GAME_FIELD_X + x * CELL_SIZE, GAME_FIELD_Y), (GAME_FIELD_X + x * CELL_SIZE, GAME_FIELD_Y + GRID_HEIGHT * CELL_SIZE))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(SCREEN, (70, 70, 70), (GAME_FIELD_X, GAME_FIELD_Y + y * CELL_SIZE), (GAME_FIELD_X + GRID_WIDTH * CELL_SIZE, GAME_FIELD_Y + y * CELL_SIZE))

    def draw_block(self, block, offset_x=0, offset_y=0):
        # 현재 떨어지는 블록이나 다음 블록을 그립니다.
        for x_offset, y_offset in block.get_current_shape():
            x, y = block.x + x_offset, block.y + y_offset
            # 화면에 표시되는 실제 픽셀 좌표 계산
            draw_x = GAME_FIELD_X + (x + offset_x) * CELL_SIZE
            draw_y = GAME_FIELD_Y + (y + offset_y) * CELL_SIZE
            # 블록 채우기 (Rect 함수 마지막 인자 0은 채우기를 의미)
            pygame.draw.rect(SCREEN, block.color, (draw_x, draw_y, CELL_SIZE, CELL_SIZE), 0)
            # 블록 테두리 (Rect 함수 마지막 인자 1은 테두리 두께)
            pygame.draw.rect(SCREEN, (200, 200, 200), (draw_x, draw_y, CELL_SIZE, CELL_SIZE), 1)

    def draw_locked_blocks(self):
        # 필드에 고정된 블록들을 그립니다.
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] != 0:
                    color = COLORS[self.grid[y][x]] # 저장된 색상 ID로 색상 가져오기
                    draw_x = GAME_FIELD_X + x * CELL_SIZE
                    draw_y = GAME_FIELD_Y + y * CELL_SIZE
                    pygame.draw.rect(SCREEN, color, (draw_x, draw_y, CELL_SIZE, CELL_SIZE), 0)
                    pygame.draw.rect(SCREEN, (200, 200, 200), (draw_x, draw_y, CELL_SIZE, CELL_SIZE), 1)

    def draw_text(self):
        # 점수, 레벨, 다음 블록 등의 정보를 표시합니다.
        # 다음 블록 표시 영역
        next_block_x = GAME_FIELD_X + GRID_WIDTH * CELL_SIZE + 30
        next_block_y = 50
        next_text_surface = FONT.render("NEXT BLOCK", True, (255, 255, 255))
        SCREEN.blit(next_text_surface, (next_block_x, next_block_y - 30))
        # 다음 블록을 그릴 때 x 오프셋은 FIELD_X 기준으로 조절해줍니다.
        self.draw_block(self.next_block, offset_x=(next_block_x - GAME_FIELD_X) // CELL_SIZE - self.next_block.x, offset_y=(next_block_y - GAME_FIELD_Y) // CELL_SIZE - self.next_block.y)

        # 점수 및 레벨 표시
        score_text_surface = FONT.render(f"SCORE: {self.score}", True, (255, 255, 255))
        level_text_surface = FONT.render(f"LEVEL: {self.level}", True, (255, 255, 255))
        SCREEN.blit(score_text_surface, (next_block_x, next_block_y + 150))
        SCREEN.blit(level_text_surface, (next_block_x, next_block_y + 180))

        # 게임 오버 메시지
        if self.game_over:
            game_over_surface = FONT.render("GAME OVER", True, (255, 0, 0))
            restart_surface = FONT.render("Press R to Restart", True, (255, 255, 255))
            # 화면 중앙에 오도록 위치 조정
            go_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            SCREEN.blit(game_over_surface, go_rect)
            SCREEN.blit(restart_surface, restart_rect)

# 5. 메인 게임 루프
def main():
    clock = pygame.time.Clock()
    game = TetrisGame()

    running = True
    while running:
        dt = clock.tick(60) # 프레임 속도 60 FPS (dt는 이전 프레임으로부터 경과한 시간, 밀리초 단위)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game.game_over: # 게임 오버 시 'R' 키로 재시작
                    if event.key == pygame.K_r:
                        game = TetrisGame()
                        game.game_over = False
                    continue

                if event.key == pygame.K_LEFT:
                    if not game.check_collision(game.current_block, dx=-1):
                        game.current_block.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    if not game.check_collision(game.current_block, dx=1):
                        game.current_block.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    # '아래' 키를 누르면 블록이 바로 한 칸 아래로 이동
                    if not game.check_collision(game.current_block, dy=1):
                        game.current_block.move(0, 1)
                elif event.key == pygame.K_UP:
                    # '위' 키를 누르면 블록 회전 (회전 후 충돌 검사)
                    original_rotation_index = game.current_block.rotation_index
                    game.current_block.rotate() # 일단 회전 시도

                    # 벽 차기 (Wall Kick) 로직 - 회전 후 벽이나 다른 블록에 갇히는 경우 옆으로 이동 시도
                    # 단순화를 위해 일단 회전 후 충돌이 있으면 회전 취소
                    if game.check_collision(game.current_block):
                        game.current_block.rotation_index = original_rotation_index # 충돌 시 원래대로 되돌리기
                elif event.key == pygame.K_SPACE:
                    # '스페이스바' 누르면 바로 맨 아래로 (하드 드롭)
                    while not game.check_collision(game.current_block, dy=1):
                        game.current_block.move(0, 1)
                    game.lock_block() # 고정
                    if not game.game_over:
                        game.current_block = game.next_block
                        game.next_block = game.new_block()
                        if game.check_collision(game.current_block):
                            game.game_over = True


        # 게임 상태 업데이트
        game.update_game_state(dt)

        # 화면 그리기
        SCREEN.fill(COLORS[0]) # 배경을 검은색으로 채움
        game.draw_grid()        # 그리드 그리기
        game.draw_locked_blocks() # 고정된 블록 그리기

        if not game.game_over:
            game.draw_block(game.current_block) # 현재 블록 그리기

        game.draw_text()        # 점수 및 UI 텍스트 그리기

        pygame.display.flip() # 화면 업데이트

    pygame.quit() # Pygame 종료

if __name__ == "__main__":
    main()
