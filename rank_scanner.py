import tkinter as tk
import pyautogui
import easyocr
import numpy as np
import re
import threading
import time

class SimpleRankScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("줘팸터 최적화 계산기")
        self.root.geometry("400x400")
        self.root.attributes("-topmost", True)

        # OCR 로딩
        print("OCR 모델을 로딩 중입니다...")
        self.reader = easyocr.Reader(['ko', 'en'])
        
        self.running = False
        self.scan_region = None
        self.last_rank = -1

        # GUI 구성
        tk.Label(root, text="⚔️ 줘팸터 즉시 도전 순위", font=("Arial", 16, "bold")).pack(pady=15)
        
        self.btn_select = tk.Button(root, text="영역 선택 (드래그)", command=self.start_region_selection, width=20, bg="#f39c12", fg="white")
        self.btn_select.pack(pady=5)

        self.btn_toggle = tk.Button(root, text="실시간 스캔 시작", command=self.toggle_scan, width=20, bg="#3498db", fg="white", state=tk.DISABLED)
        self.btn_toggle.pack(pady=5)

        self.status_label = tk.Label(root, text="영역을 먼저 지정해 주세요.", fg="gray")
        self.status_label.pack(pady=10)

        # 결과 표시 (크고 명확하게)
        self.rank_display = tk.Label(root, text="- 위", font=("Arial", 20, "bold"), fg="#2c3e50")
        self.rank_display.pack(pady=10)

        self.result_display = tk.Label(root, text="도전 가능 순위 대기 중", font=("Arial", 14), fg="#e74c3c")
        self.result_display.pack(pady=10)

    # --- 영역 선택 로직 ---
    def start_region_selection(self):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-alpha", 0.3, "-fullscreen", True, "-topmost", True)
        self.canvas = tk.Canvas(self.selection_window, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        self.start_x = self.start_y = self.rect = None
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=3)

    def on_move_press(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        x, y = min(self.start_x, event.x), min(self.start_y, event.y)
        w, h = abs(self.start_x - event.x), abs(self.start_y - event.y)
        self.scan_region = (x, y, w, h)
        self.selection_window.destroy()
        self.status_label.config(text="영역 설정 완료! 스캔을 시작하세요.", fg="green")
        self.btn_toggle.config(state=tk.NORMAL)

    # --- 계산 로직 ---
    def calculate_max_challenge(self, rank):
        if rank >= 100:
            # 100위 이상: 92% 적용
            target = int(rank * 0.92)
            return f"최대 {target}위 까지 도전 가능"
        else:
            # 1~99위: 35% 적용
            target = int(rank * 0.35)
            if target < 1: target = 1
            return f"최대 {target}위 까지 도전 가능"

    def scan_loop(self):
        while self.running:
            if self.scan_region:
                try:
                    screenshot = pyautogui.screenshot(region=self.scan_region)
                    img_np = np.array(screenshot)
                    results = self.reader.readtext(img_np)
                    combined_text = " ".join([res[1] for res in results])
                    
                    if "없음" in combined_text:
                        current_rank = 3001
                    else:
                        numbers = re.findall(r'\d+', combined_text)
                        current_rank = int(numbers[0]) if numbers else None

                    if current_rank and current_rank != self.last_rank:
                        self.last_rank = current_rank
                        self.rank_display.config(text=f"현재: {current_rank if current_rank != 3001 else '순위 없음'}")
                        self.result_display.config(text=self.calculate_max_challenge(current_rank))
                except:
                    pass
            time.sleep(1.2)

    def toggle_scan(self):
        if not self.running:
            self.running = True
            self.btn_toggle.config(text="스캔 중지", bg="#e67e22")
            threading.Thread(target=self.scan_loop, daemon=True).start()
        else:
            self.running = False
            self.btn_toggle.config(text="실시간 스캔 시작", bg="#3498db")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleRankScanner(root)
    root.mainloop()