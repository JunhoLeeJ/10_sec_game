import os
import sys
import keyring
import pygame
from cryptography.fernet import Fernet
import cryptography
import time
import random


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
play = sprite(play_images_list, [-1], 0, False, True,
                     0.5, 0.5)

menu_images_list = ['menu_normal.png', 'menu_hover.png', 'menu_pressed.png']
menu = sprite(menu_images_list, [0, 1, 2, 3, 4], -1, False, True,
                     0.2, 0.1)

lvl1_images_list = ['level_1_normal.png', 'level_1_hover.png', 'level_1_pressed.png']
lvl1 = sprite(lvl1_images_list, [0], 1, False, True,
              0.2, 0.3)

lvl2_images_list = ['level_2_normal.png', 'level_2_hover.png', 'level_2_pressed.png', 'level_2_locked.png']
lvl2 = sprite(lvl2_images_list, [0], 2, False, False,
              0.3, 0.3)

levels = [lvl1, lvl2]


class archer_sprite:
    global stage

    def __init__(self, images_list, x, y, hp, cool_time, attack_time, speed, movable):
        self.normal_image = pygame.image.load(images_list[0])
        self.image = self.normal_image
        image_width, image_height = self.normal_image.get_size()
        self.normal_get_rect = self.image.get_rect(topleft=((screen_width - image_width) * x,
                                                            (screen_height - image_height) * y))
        self.start_attack_image = pygame.image.load(images_list[1])
        self.end_attack_image = pygame.image.load(images_list[2])
        attack_image_width, attack_image_height = self.end_attack_image.get_size()
        self.attack_get_rect = self.end_attack_image.get_rect(topleft=((screen_width - attack_image_width) * x,
                                                            (screen_height - attack_image_height) * y))
        self.get_rect = self.normal_get_rect
        self.x = x
        self.y = y
        self.hp = hp
        self.cool_time = cool_time
        self.attack_time = attack_time
        self.speed = speed
        self.movable = movable
        self.start_attack = 0
        self.attack_motion_frame = 0
    def collision_check(self, enemies, direction):      # using direction tilt attack range
        global stage
        for enemy in enemies:
            if self.get_rect.colliderect(enemy.get_rect):
                self.hp -= 1
                # add red screen effect - screen.blit(transparent red image)
                if self.hp <= 0:
                    stage = 'fail'
    def win_check(self, enemies):
        global stage
        win = True
        if self.hp <= 0:
            return False
        else:
            for enemy in enemies:
                if enemy.required and not enemy.removed:
                    return False
        if win:
            return True
    def attack(self):
        if time.time() - self.start_attack >= self.cool_time:
            self.start_attack = time.time()
            self.attack_motion_frame = 0
    def attack_motion(self):
        if self.attack_motion_frame <= self.attack_time / 4:    # first half prepare attack
            self.image = self.start_attack_image
            self.get_rect = self.normal_get_rect
            self.attack_motion_frame += 0.01
        elif self.attack_motion_frame <= self.attack_time:      # second half actual attack
            self.image = self.end_attack_image
            self.get_rect = self.attack_get_rect
            self.attack_motion_frame += 0.01
        else:
            self.image = self.normal_image
            self.get_rect = self.normal_get_rect



class sword_sprite(archer_sprite):     # 일단 sword sprite 만들고 나중에 겹치는 부분만 남기기
    global stage
    def __init__(self, images_list, x, y, hp, cool_time, attack_time, speed, movable, attacking):
        super().__init__(images_list, x, y, hp, cool_time, attack_time, speed, movable)
        self.attacking = attacking
        self.attack_time = attack_time
    def collision_check(self, enemies, direction):      # using direction tilt attack range
        global stage
        time_from_attack = time.time() - self.start_attack
        if time_from_attack > self.attack_time or time_from_attack <= self.attack_time / 2:
            # attacking or not
            self.attacking = False
        else:
            self.attacking = True
        for enemy in enemies:
            if self.get_rect.colliderect(enemy.get_rect):
                self.hp -= 1
                # add red screen effect - screen.blit(transparent red image)
                if self.hp <= 0:
                    stage = 'fail'
            elif self.attack_get_rect.colliderect(enemy.get_rect) and self.attacking:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.remove()



archer_images_list = ['archer_normal.png', 'archer_start_attack.png', 'archer_end_attack.png']
archer = archer_sprite(archer_images_list, 0.3, 0.5, 2, 3, 0.3, 10, True)
sword_images_list = ['sword_normal.png', 'sword_start_attack.png', 'sword_end_attack.png']
# 모션 보면 중간 맞추려는 거 때문에 굉장히 어색함. 수정 필요. 타격 판정을 겸하니까 어떻게 잘 해야 함
sword = sword_sprite(sword_images_list, 0.7, 0.5, 2, 1.5, 0.3, 10, True, False)



# def main():
# 만약 안되면 이거랑 마지막 주석 취소하고 싹 다 탭으로 밀기


test_variable = 0
# 게임 루프
running = True
while running:
    archer.attack_motion()
    sword.attack_motion()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            play.check_image_click(event.pos)
            menu.check_image_click(event.pos)
            for level in levels:
                level.check_image_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if stage != -1 and stage != 0:
                archer.attack()
                sword.attack()
            play.check_image_release(event.pos)
            menu.check_image_release(event.pos)
            for level in levels:
                level.check_image_release(event.pos)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]   # should be True if pressed and False if not


    # things you have to do in each stage
    if stage == -1:
        screen.fill(white)
        write_text('10 Seconds Game!', 36, black, 0.5, 0.1)
        write_text(f'Stage: {stage}', 36, black, 0.5, 0.8)
        screen.blit(play.change_image_stat(), play.get_rect)
        
    elif stage == 0:
        screen.fill(white)
        write_text('10 Seconds Game!', 36, black, 0.5, 0.1)
        for lvl in levels:
            screen.blit(lvl.change_image_stat(), lvl.get_rect)

    elif stage == 1:
        screen.fill(white)
        screen.blit(menu.change_image_stat(), menu.get_rect)
        screen.blit(sword.image, sword.get_rect)
        screen.blit(archer.image, archer.get_rect)
        lvl2.unlocked = True
        write_text('level 1', 36, black, 0.5, 0.1)

    elif stage == 2:
        screen.fill(white)
        screen.blit(menu.change_image_stat(), menu.get_rect)
        write_text('level 2', 36, black, 0.5, 0.1)



    # 화면 업데이트
    pygame.display.flip()
    clock.tick(fps)


# Pygame 종료
pygame.quit()

# if __name__ == "__main__":
    # main()