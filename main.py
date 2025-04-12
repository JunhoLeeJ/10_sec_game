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


import os
import sys
import keyring
import pygame
from cryptography.fernet import Fernet

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
def write_data(data):
    try:
        with open(txt_path, "wb") as f:
            f.write(fernet.encrypt(data.encode()))
    except Exception as e:
        print(f"Error writing data: {e}")

# 게임 로직 (예시)
def main():
    print("Game started")
    print("Current data:", read_data())
    new_data = "Updated by game"
    write_data(new_data)
    print("New data:", read_data())# Pygame 초기화
    pygame.init()

    # 화면 설정
    screen_height = 750
    screen_width = 1200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("10 Seconds Game")
    white = (0,0,0)
    black = (255,255,255)

    # 변수 설정
    antialiasing = True
    center = 'center'

    # 텍스트 설정
    def write_text(text, size, color, x, y):
        font = pygame.font.SysFont('arial', size=size)
        given_text = font.render(text, antialiasing, color)
        text_width, text_height = given_text.get_size()
        if x == 'center':
            x = (screen_width - text_width) // 2
        if y == 'center':
            y = (screen_height - text_height) // 2
        screen.blit(given_text, (x, y))

    # 이미지 설정
    def draw_image(image, x, y):
        image_width, image_height = image.get_size()
        if x == 'center':
            x = (screen_width - image_width) // 2
        if y == 'center':
            y = (screen_height - image_height) // 2
        screen.blit(image, (x, y))

    knight_image = pygame.image.load("sword image.png")
    sword_image = pygame.image.load("sword image.png")
    archer_image = pygame.image.load("sword image.png")
    bow_image = pygame.image.load("sword image.png")
    arrow_image = pygame.image.load("sword image.png")
    enemy_image = pygame.image.load("sword image.png")
    bullet_image = pygame.image.load("sword image.png")

    play_nonhover_image = pygame.image.load('play nonhover.png')
    play_hover_image = pygame.image.load('play hover.png')


    def play():
        pass

    test_variable = 0
    playing = False
    # 게임 루프
    running = True
    while running:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if playing:
            play()

        write_text('10 Seconds Game!', 36, black, center, 50)
        draw_image(play_nonhover_image, center, center)


        test_variable += 0.1

        # 화면 업데이트
        pygame.display.flip()


    # Pygame 종료
    pygame.quit()

if __name__ == "__main__":
    main()