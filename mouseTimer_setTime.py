from datetime import datetime
import time
import pyautogui

from pystray import Icon, MenuItem, Menu
from PIL import Image
import threading

ICON_PATH = "favicon_mouse.ico"
icon_img = Image.open(ICON_PATH)

ACTIVE_9to6 = [0,1,2,4] # 월,화,수,금
ACTIVE_10to7 = [3]

start_time_9 = "09:00"
end_time_6 = "19:00"

start_time_10 = "09:00"
end_time_7 = "19:00"

last_move_time = time.time()
last_x, last_y = pyautogui.position()

def mouse_timer():
    global last_move_time, last_x, last_y

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.weekday()

        current_x, current_y = pyautogui.position()

        if (current_x != last_x or current_y != last_y):
            last_move_time = time.time()

        if (current_day in ACTIVE_9to6 and start_time_9 <= current_time <= end_time_6) or \
            (current_day in ACTIVE_10to7 and start_time_10 <= current_time <= end_time_7):
            
            if time.time() - last_move_time >= 5:
                x = current_x + 10
                pyautogui.moveTo(x, current_y)
                pyautogui.moveTo(x-10, current_y)
                last_move_time = time.time()

        last_x, last_y = current_x, current_y

        time.sleep(30)

def exit_program(icon, item):
    icon.stop() # 시스템 트레이에서 아이콘 제거
    exit(0) #프로그램 종료

menu = Menu(MenuItem("종료", exit_program))
tray_icon = Icon("MouseTimer", icon_img, menu=menu)

# 백그라운드에서 마우스 이동 실행
threading.Thread(target=mouse_timer, daemon=True).start()

# 시스템트레이 아이콘 실행
tray_icon.run()