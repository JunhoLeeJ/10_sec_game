import os
import sys
import keyring
import pygame
from cryptography.fernet import Fernet
import cryptography

# 키체인 설정
SERVICE_NAME = "10_sec_game"
ACCOUNT_NAME = "encryption_key"

# 키 가져오기 또는 생성
key = keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)
if not key:
    key = Fernet.generate_key().decode()
    keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, key)
fernet = Fernet(key.encode())

# 파일 경로
base_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.dirname(__file__)
txt_path = os.path.join(base_path, "encrypted_data.txt")
print("Txt path:", txt_path)  # 디버깅 출력

# 읽기
def read_data():
    try:
        with open(txt_path, "rb") as f:
            return fernet.decrypt(f.read()).decode()
    except Exception as e:
        print(f"Error reading data: {e}")
        return "Default data"

# 쓰기
def write_data():
    global stage
    global score
    global highscore
    global antialiasing
    global fps
    global hover_enabled
    # global color_scheme
    global screen_width
    global screen_height

    data = f'{stage} {score} {highscore} {antialiasing} {fps} {hover_enabled} {screen_width} {screen_height}'

    try:
        with open(txt_path, "wb") as f:
            f.write(fernet.encrypt(data.encode()))
    except Exception as e:
        print(f"Error writing data: {e}")






# inspired by: https://youtu.be/p4wy7FGczrw?t=524

# 구현해야 하는 거 우선순위

# 메인 화면 - 플레이!, 난이도, 상점(스킨), 설정
# 스테이지 기준
# 도중에 재시작 할 수 있게
# 실패했을 때 나서 메뉴 / 재시도 화면
# 성공했을 때 메뉴 / 재시도 / 다음 스테이지 화면
# 검사/궁수 움직임
# 몬스터 움직임
# 검사 캐릭터 칼 움직임 + 타격 판정
# 슈팅 몬스터 총알 + 타격 판정
# 캐릭터 피격 판정
# 플레이 클릭으로 되도록

# 궁수 화살 움직임 + 타격 판정
# 10초씩 따로 컨트롤 할 수 있게 하는 거
# 검사, 몬스터 이전 상황 기억해서 궁수 타이밍 때 똑같이 따라 하는 거
# 밸런스 조절

# 게임 진행 상황 저장
# 상점 (스킨) (그림 그리면 됨)
# 설정 (안티엘리어싱, 화면 크기 설정)
# 난이도 설정




# 메인 게임 로직
# def main():

pygame.init()
clock = pygame.time.Clock()

# 화면 설정
screen_width = int(read_data().split()[6])
screen_height = int(read_data().split()[7])
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("10 Seconds Game")

# 유저 세팅 설정
stage = int(read_data().split()[0])
score = int(read_data().split()[1])
highscore = int(read_data().split()[2])
antialiasing = bool(read_data().split()[3])
fps = int(read_data().split()[4])
hover_enabled = bool(read_data().split()[5])
# color_scheme = int(read_data().split()[6])
# to do this black and white inverse images are needed
white = (255,255,255)
black = (0,0,0)


# 그냥 변수 설정
play_button_pressed = False

# 텍스트 설정
def write_text(text, size, color, x, y):
    font = pygame.font.SysFont('arial', size=size)
    given_text = font.render(text, antialiasing, color)
    text_width, text_height = given_text.get_size()
    screen.blit(given_text, ((screen_width - text_width) * x,
                             (screen_height - text_height) * y))


class sprite:
    global mouse_pos
    global mouse_pressed
    global stage
    def __init__(self, images_list, stages, stage_dest, pressed, unlocked, x, y):
        self.normal_image = pygame.image.load(images_list[0])
        self.hover_image = pygame.image.load(images_list[1])
        self.pressed_image = pygame.image.load(images_list[2])
        self.images_list = images_list
        image_width, image_height = self.normal_image.get_size()
        self.get_rect = self.normal_image.get_rect(topleft=((screen_width - image_width) * x,
                                                            (screen_height - image_height) * y))
        self.stage_number = stages
        self.stage_dest = stage_dest
        self.pressed = pressed
        self.unlocked = unlocked

    def change_image_stat(self):
        if self.get_rect.collidepoint(mouse_pos) and self.unlocked:
            if self.pressed:
                return self.pressed_image
            else:
                return self.hover_image
        elif not self.unlocked:
            return pygame.image.load(self.images_list[3])
        else:
            return self.normal_image

    def check_image_click(self, click_pos):
        if stage in self.stage_number:
            if self.get_rect.collidepoint(click_pos):
                self.pressed = True

    def check_image_release(self, release_pos):
        global stage
        if stage in self.stage_number and self.get_rect.collidepoint(release_pos) and self.unlocked and self.pressed:
            stage = self.stage_dest
        self.pressed = False


play_images_list = ['play_normal.png', 'play_hover.png', 'play_pressed.png']
play_sprite = sprite(play_images_list, [-1], 0, False, True,
                     0.5, 0.5)

menu_images_list = ['menu_normal.png', 'menu_hover.png', 'menu_pressed.png']
menu_sprite = sprite(menu_images_list, [0, 1, 2, 3, 4], -1, False, True,
                     0.2, 0.1)

lvl1_images_list = ['level_1_normal.png', 'level_1_hover.png', 'level_1_pressed.png']
lvl1_sprite = sprite(lvl1_images_list, [0], 1, False, True,
                     0.2, 0.3)

lvl2_images_list = ['level_2_normal.png', 'level_2_hover.png', 'level_2_pressed.png', 'level_2_locked.png']
lvl2_sprite = sprite(lvl2_images_list, [0], 2, False, False,
                     0.3, 0.3)

levels = [lvl1_sprite, lvl2_sprite]

level = levels[0]   # init value, will change


# def main():
# 만약 안되면 이거랑 마지막 주석 취소하고 싹 다 탭으로 밀기



test_variable = 0
# 게임 루프
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            play_sprite.check_image_click(event.pos)
            menu_sprite.check_image_click(event.pos)
            for level in levels:
                level.check_image_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            play_sprite.check_image_release(event.pos)
            menu_sprite.check_image_release(event.pos)
            for level in levels:
                level.check_image_release(event.pos)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]   # should be True if pressed and False if not


    # things you have to do in each stage
    if stage == -1:
        screen.fill(white)
        write_text('10 Seconds Game!', 36, black, 0.5, 0.1)
        write_text(f'Stage: {stage}', 36, black, 0.5, 0.8)
        screen.blit(play_sprite.change_image_stat(), play_sprite.get_rect)
        
    elif stage == 0:
        screen.fill(white)
        write_text('10 Seconds Game!', 36, black, 0.5, 0.1)
        for lvl in levels:
            screen.blit(lvl.change_image_stat(), lvl.get_rect)

    elif stage == 1:
        screen.fill(white)
        screen.blit(menu_sprite.change_image_stat(), menu_sprite.get_rect)
        lvl2_sprite.unlocked = True
        write_text('level 1', 36, black, 0.5, 0.1)

    elif stage == 2:
        screen.fill(white)
        screen.blit(menu_sprite.change_image_stat(), menu_sprite.get_rect)
        write_text('level 2', 36, black, 0.5, 0.1)



    # 화면 업데이트
    pygame.display.flip()
    clock.tick(fps)


# Pygame 종료
pygame.quit()

# if __name__ == "__main__":
    # main()