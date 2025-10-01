import sys
import threading
import time
import cv2
import numpy as np
from mss import mss
import os # Import the 'os' module to handle file paths
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QProgressBar, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QFont

# --- Configuration ---
HEALER_ULTIMATES = {
    "luna_ult.png": {"name": "Luna Snow", "duration": 9},
    "cloak_ult.png": {"name": "Cloak & Dagger", "duration": 12},
    "invisible_ult.png": {"name": "Invisible Woman", "duration": 7.5},
    "mantis_ult.png": {"name": "Mantis", "duration": 7},
}
MATCH_THRESHOLD = 0.65
SUBTITLE_MONITOR_AREA = {"top": 800, "left": 600, "width": 800, "height": 150}


class UltimateWidget(QWidget):
    finished = pyqtSignal(int)

    def __init__(self, ultimate_name, duration, slot_index, parent=None):
        super().__init__(parent)
        self.duration, self.remaining_time = duration, duration
        self.slot_index = slot_index
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QVBoxLayout()
        self.name_label = QLabel(f"{ultimate_name} Ultimate")
        self.name_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: white;")
        self.timer_label = QLabel(f"{self.remaining_time:.1f}s")
        self.timer_label.setFont(QFont("Arial", 14))
        self.timer_label.setStyleSheet("color: white;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, int(duration * 10))
        self.progress_bar.setValue(int(duration * 10))
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar {border: 2px solid grey; border-radius: 5px; background-color: #222222;} QProgressBar::chunk {background-color: #00A3FF; width: 10px;}")
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(100)
    
    def update_timer(self):
        self.remaining_time -= 0.1
        if self.remaining_time <= 0:
            self.timer.stop()
            self.finished.emit(self.slot_index)
            self.close()
            return
        self.timer_label.setText(f"{self.remaining_time:.1f}s")
        self.progress_bar.setValue(int(self.remaining_time * 10))

class Overlay(QWidget):
    show_timer_signal = pyqtSignal(str, float)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.showFullScreen()
        self.active_timers = {}
        self.slots = []
        self.slot_occupied = []
        num_slots = 5
        screen_center_x = QApplication.primaryScreen().geometry().center().x()
        widget_width_estimate = 250
        for i in range(num_slots):
            x_pos = screen_center_x - (widget_width_estimate // 2)
            y_pos = 50 + (i * 110)
            self.slots.append(QPoint(x_pos, y_pos))
            self.slot_occupied.append(False)
        self.templates = {}
        # --- MODIFIED CODE ---
        # Look for templates inside the 'ults' folder
        for filename, data in HEALER_ULTIMATES.items():
            try:
                # Build the full path to the image (e.g., "ults/luna_ult.png")
                image_path = os.path.join("ults", filename)
                template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if template is None: raise FileNotFoundError
                self.templates[filename] = template
                print(f"Successfully loaded template: {image_path}")
            except FileNotFoundError:
                print(f"!!! ERROR: Could not find '{image_path}'. Make sure it exists in the 'ults' folder.")
                sys.exit()
        self.show_timer_signal.connect(self.show_ultimate_timer)
        print("--- Marvel Rivals Ultimate Tracker ---")
        print("Overlay started. Looking for image matches...")
        self.tracker_thread = threading.Thread(target=self.track_templates, daemon=True)
        self.tracker_thread.start()

    def free_up_slot(self, slot_index):
        print(f"Slot {slot_index} is now free.")
        if 0 <= slot_index < len(self.slot_occupied):
            self.slot_occupied[slot_index] = False

    def track_templates(self):
        with mss() as sct:
            while True:
                sct_img = sct.grab(SUBTITLE_MONITOR_AREA)
                screen_img = np.array(sct_img)
                screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
                for filename, template in self.templates.items():
                    data = HEALER_ULTIMATES[filename]
                    if data["name"] in self.active_timers: continue
                    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(res)
                    if max_val > MATCH_THRESHOLD:
                        print(f"!!! MATCH FOUND for {data['name']} !!! (Confidence: {max_val:.2f})")
                        self.show_timer_signal.emit(data["name"], data["duration"])
                        self.active_timers[data['name']] = time.time() + data['duration']
                current_time = time.time()
                self.active_timers = {name: expiry for name, expiry in self.active_timers.items() if current_time < expiry}
                time.sleep(0.3)

    def show_ultimate_timer(self, ultimate_name, duration):
        for i, occupied in enumerate(self.slot_occupied):
            if not occupied:
                print(f"Found a free slot: {i}. Placing timer for {ultimate_name}.")
                self.slot_occupied[i] = True
                widget = UltimateWidget(ultimate_name=ultimate_name, duration=duration, slot_index=i, parent=self)
                widget.finished.connect(self.free_up_slot)
                widget.move(self.slots[i])
                widget.show()
                break
        else:
            print(f"No free slots available for {ultimate_name} timer.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec())
