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

# 이미지 설정
def image_get_rect(image, x, y):
    image_width, image_height = image.get_size()
    return image.get_rect(topleft=((screen_width - image_width) * x,
                                   (screen_height - image_height) * y))

def click_check_image(button_pressed, images_list):
    global mouse_pos
    global mouse_pressed
    if mouse_pressed and button_pressed and images_list[3].collidepoint(mouse_pos):
        return images_list[2]
    elif images_list[3].collidepoint(mouse_pos):
        return images_list[1]
    else:
        return images_list[0]

knight_image = pygame.image.load("sword.png")
sword_image = pygame.image.load("sword.png")
archer_image = pygame.image.load("sword.png")
bow_image = pygame.image.load("sword.png")
arrow_image = pygame.image.load("sword.png")
enemy_image = pygame.image.load("sword.png")
bullet_image = pygame.image.load("sword.png")

play_normal_image = pygame.image.load('play_normal.png')
play_hover_image = pygame.image.load('play_hover.png')
play_pressed_image = pygame.image.load('play_pressed.png')
play_get_rect = image_get_rect(play_normal_image, 0.5, 0.5)
play_images_list = [play_normal_image, play_hover_image, play_pressed_image, 
                    play_get_rect, 0, False, False]
# 0: normal, 1: hover, 2: pressed, 3: rect, 4: stage number. 4~6: ignore

lvl0_normal_image = pygame.image.load('level_0_image.png')
lvl0_hover_image = pygame.image.load('level_0_image.png')
lvl0_pressed_image = pygame.image.load('level_0_image.png')
lvl0_get_rect = image_get_rect(lvl0_normal_image, 0.1, 0.3)
lvl0_images_list = [lvl0_normal_image, lvl0_hover_image, lvl0_pressed_image, lvl0_get_rect, 0, False, False]
# 0: normal, 1: hover, 2: pressed, 3: rect, 4: level number, 5: button pressed, 6: locked

levels = [lvl0_images_list]
level = levels[0]   # init value, will change


# def main():
# 만약 안되면 이거랑 마지막 주석 취소하고 싹 다 탭으로 밀기



test_variable = 0
playing = False
# 게임 루프
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if stage == -2:
                if play_images_list[3].collidepoint(event.pos):
                    play_button_pressed = True
            elif stage == -1:
                for level in levels:
                    if level[3].collidepoint(event.pos):
                        level[5] = True     # button pressed
                        break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if stage == -2:
                if play_button_pressed and play_images_list[3].collidepoint(event.pos):
                    stage = -1
                    write_data()
            elif stage == -1:
                if level[5] and level[3].collidepoint(event.pos):
                    stage = level[4]
            play_button_pressed = False  # button press init
            level[5] = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]   # should be True if pressed and False if not


    # things you have to do in each stage
    if stage == -2:
        current_play_image = click_check_image(play_button_pressed, play_images_list)
        screen.fill(white)
        write_text('10 Seconds Game!', 36, black, 0.5, 0.1)
        write_text(f'Stage: {stage}', 36, black, 0.5, 0.8)
        screen.blit(current_play_image, play_images_list[3])
        
    elif stage == -1:
        screen.fill(white)
        write_text('10 Seconds Game!', 36, black, 0.5, 0.1)
        for lvl in levels:
            screen.blit(lvl[0], lvl[3])

    elif stage == 0:
        screen.fill(black)


    # 화면 업데이트
    pygame.display.flip()
    clock.tick(fps)


# Pygame 종료
pygame.quit()

# if __name__ == "__main__":
    # main()