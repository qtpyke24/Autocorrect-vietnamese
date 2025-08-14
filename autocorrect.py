import signal
import sys
from pynput import keyboard
import phunspell
import pyperclip
import os
import time

# Đặt đường dẫn thư mục chứa vi_VN.dic và vi_VN.aff
os.environ['DICPATH'] = 'C:\\Users\\Admin\\Desktop\\tt\\abc'  # Thay bằng đường dẫn thư mục của bạn

# Load từ điển tiếng Việt
try:
    pspell = phunspell.Phunspell('vi_VN')
except Exception as e:
    print(f"Lỗi load từ điển: {e}")
    exit(1)

current_word = ""
pressed_keys = set()
listener = None

# Hàm xử lý tín hiệu Ctrl+C hoặc thoát
def signal_handler(sig, frame):
    print("\nDừng chương trình...")
    if listener is not None:
        listener.stop()
    sys.exit(0)

# Gắn signal handler cho Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def check_and_correct(word):
    if not word:
        return word
    if not pspell.lookup(word):
        suggestions = list(pspell.suggest(word))
        return suggestions[0] if suggestions else word
    return str(word)[1:]

def on_press(key):
    global current_word
    try:
        if key == keyboard.Key.esc:  # Nhấn Esc để dừng
            signal_handler(None, None)
        elif key not in pressed_keys:  # Chỉ xử lý nếu phím chưa pressed (tránh repeat)
            pressed_keys.add(key)
            if hasattr(key, 'char') and key.char:
                current_word += key.char
            elif key == keyboard.Key.space:
                if current_word.strip():  # Chỉ xử lý nếu có từ
                    corrected = check_and_correct(current_word.strip())
                    if corrected != current_word.strip():
                        time.sleep(0.15)  # Delay để đồng bộ
                        for _ in range(len(current_word)):  # Không xóa khoảng trắng
                            keyboard.Controller().press(keyboard.Key.backspace)
                            keyboard.Controller().release(keyboard.Key.backspace)
                            time.sleep(0.05)  # Delay mỗi backspace
                        pyperclip.copy(corrected + " ")
                        time.sleep(0.15)  # Delay trước paste
                        with keyboard.Controller().pressed(keyboard.Key.ctrl):
                            keyboard.Controller().press('v')
                            keyboard.Controller().release('v')
                        time.sleep(0.15)  # Delay sau paste
                        print(f"Sửa: {current_word} -> {corrected}")
                    current_word = ""
                else:
                    current_word = ""  # Reset nếu chỉ gõ space
            elif key == keyboard.Key.backspace:
                current_word = current_word[:-1] if current_word else ""
    except Exception as e:
        print(f"Lỗi: {e}")

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

# Bắt đầu theo dõi phím gõ với on_press và on_release
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
try:
    listener.join()
except KeyboardInterrupt:
    signal_handler(None, None)