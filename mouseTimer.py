import time
import pyautogui

from pystray import Icon, MenuItem, Menu
from PIL import Image
import threading

ICON_PATH = "favicon_mouse.ico"
icon_img = Image.open(ICON_PATH)

last_move_time = time.time()
last_x, last_y = pyautogui.position()

def mouse_timer():
    global last_move_time, last_x, last_y

    while True:
        current_x, current_y = pyautogui.position()

        # 사용자가 마우스를 움직이면 시간 업데이트
        if (current_x != last_x or current_y != last_y):
            last_move_time = time.time()

        # 5초 내 움직이지 않으면 자동 이동
        if time.time() - last_move_time >= 30:
                x = current_x + 10
                pyautogui.moveTo(x, current_y)
                pyautogui.moveTo(x-10, current_y)
                last_move_time = time.time()

        last_x, last_y = current_x, current_y
        time.sleep(1)

# 프로그램 종료
def exit_program(icon, item):
    icon.stop() # 시스템 트레이에서 아이콘 제거
    exit(0) #프로그램 종료

# 트레이 아이콘 메뉴 설정
menu = Menu(MenuItem("종료", exit_program))
tray_icon = Icon("MouseTimer", icon_img, menu=menu)

# 백그라운드에서 마우스 이동 실행
threading.Thread(target=mouse_timer, daemon=True).start()

# 시스템트레이 아이콘 실행
tray_icon.run()