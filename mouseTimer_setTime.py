from datetime import datetime
import time
import pyautogui
import keyboard

from pystray import Icon, MenuItem, Menu
from PIL import Image
import threading
import random

ICON_PATH = "favicon_mouse.ico"
icon_img = Image.open(ICON_PATH)

ACTIVE_9to6 = [0,1,2,4] # 월,화,수,금
ACTIVE_10to7 = [3]

start_time_9 = "09:00"
end_time_6 = "19:00"

start_time_10 = "09:00"
end_time_7 = "19:00"

# 마지막 마우스 이동 시간 및 위치 추적
last_move_time = time.time()
last_x, last_y = pyautogui.position()

# 화면 해상도 가져오기 
screen_width, screen_height = pyautogui.size()

def keyboard_press(_event):
    global last_move_time
    last_move_time = time.time()

def keyboard_listener():
    keyboard.hook(keyboard_press)
    keyboard.wait()

def mouse_timer():
    global last_move_time, last_x, last_y

    while True:
        # now = datetime.now()
        # current_time = now.strftime("%H:%M")
        # current_day = now.weekday()

        current_x, current_y = pyautogui.position()

        # 최근 5초 이내 마우스 이동 또는 키보드 움직임이 있었는지 확인
        if current_x != last_x or current_y != last_y:
            last_move_time = time.time() # 사용자가 직접 움직였으면 타이머 리셋

        # 설정된 요일과 시간 내에서만 실행
        # if (current_day in ACTIVE_9to6 and start_time_9 <= current_time <= end_time_6) or \
        #     (current_day in ACTIVE_10to7 and start_time_10 <= current_time <= end_time_7):
            
        # 최근 5초 동안 마우스/키보드 입력이 없었다면 실행
        if time.time() - last_move_time >= 5: 

            for _ in range(5):
                random_x = random.randint(0, screen_width -1)
                random_y = random.randint(0, screen_height -1)

                pyautogui.moveTo(random_x, random_y, duration=0.5)
                last_move_time = time.time() # 마지막 자동 움직임 시간 업데이트
            
            # 20% 확률로 클릭 이벤트 추가
            if random.random() < 0.2:
                pyautogui.click()

        # 현재 마우스 위치 저장 (다음 루프에서 비교할 값)
        last_x, last_y = current_x, current_y

        # 랜덤 시간 대기
        time.sleep(random.randint(25, 30))


def exit_program(icon, item):
    icon.stop() # 시스템 트레이에서 아이콘 제거
    exit(0) #프로그램 종료

menu = Menu(MenuItem("종료", exit_program))
tray_icon = Icon("MouseTimer", icon_img, menu=menu)


# 백그라운드에서 키보드 감지 실행
threading.Thread(target=keyboard_listener, daemon=True).start()

# 백그라운드에서 마우스 이동 실행
threading.Thread(target=mouse_timer, daemon=True).start()

# 시스템트레이 아이콘 실행
tray_icon.run()
