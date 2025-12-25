import tkinter as tk
from tkinter import font
import pyautogui
import easyocr
import numpy as np
import re
import threading
import time

class ModernRankScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("줘팸터 순위 분석기 Pro")
        self.root.geometry("400x520")
        self.root.configure(bg="#F8F9FA")  # 전체 배경색
        self.root.attributes("-topmost", True)

        # 폰트 설정
        self.title_font = font.Font(family="Malgun Gothic", size=16, weight="bold")
        self.label_font = font.Font(family="Malgun Gothic", size=10)
        self.result_font = font.Font(family="Malgun Gothic", size=22, weight="bold")
        
        # OCR 초기화
        self.reader = easyocr.Reader(['ko', 'en'])
        self.running = False
        self.scan_region = None
        self.last_rank = -1

        self.setup_ui()

    def setup_ui(self):
        """UI 구성 요소를 배치합니다."""
        
        # 1. 헤더 섹션
        header = tk.Frame(self.root, bg="#4A90E2", height=80)
        header.pack(fill="x")
        tk.Label(header, text="🏆 줘팸터 순위 분석기", font=self.title_font, fg="white", bg="#4A90E2").pack(pady=20)

        # 2. 메인 컨텐츠 (카드 레이아웃)
        content = tk.Frame(self.root, bg="#F8F9FA", padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # 컨트롤 버튼
        btn_frame = tk.Frame(content, bg="#F8F9FA")
        btn_frame.pack(fill="x", pady=10)

        self.btn_select = tk.Button(btn_frame, text="📍 영역 선택하기", command=self.start_region_selection, 
                                   font=self.label_font, bg="#FFFFFF", fg="#333333", relief="flat", 
                                   highlightthickness=1, highlightbackground="#DCDFE6", cursor="hand2", width=15)
        self.btn_select.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_toggle = tk.Button(btn_frame, text="▶ 스캔 시작", command=self.toggle_scan, 
                                   font=self.label_font, bg="#FFFFFF", fg="#333333", relief="flat", 
                                   highlightthickness=1, highlightbackground="#DCDFE6", cursor="hand2", width=15, state=tk.DISABLED)
        self.btn_toggle.pack(side="left", padx=5, expand=True, fill="x")

        # 상태 안내
        self.status_label = tk.Label(content, text="영역을 먼저 지정해 주세요.", font=self.label_font, fg="#909399", bg="#F8F9FA")
        self.status_label.pack(pady=5)

        # --- 인식 결과 카드 ---
        result_card = tk.Frame(content, bg="#FFFFFF", highlightthickness=1, highlightbackground="#EBEEF5", padx=15, pady=20)
        result_card.pack(fill="both", expand=True, pady=10)

        tk.Label(result_card, text="현재 내 순위", font=self.label_font, fg="#606266", bg="#FFFFFF").pack()
        self.rank_display = tk.Label(result_card, text="- 위", font=self.result_font, fg="#303133", bg="#FFFFFF")
        self.rank_display.pack(pady=5)

        tk.Canvas(result_card, height=1, bg="#EBEEF5", highlightthickness=0).pack(fill="x", pady=15)

        tk.Label(result_card, text="도전 가능 순위", font=self.label_font, fg="#606266", bg="#FFFFFF").pack()
        self.target_display = tk.Label(result_card, text="준비 완료", font=self.result_font, fg="#E74C3C", bg="#FFFFFF")
        self.target_display.pack(pady=5)

        # 3. 푸터
        footer = tk.Label(self.root, text="Designed by 코딩 파트너", font=("Arial", 8), fg="#C0C4CC", bg="#F8F9FA")
        footer.pack(side="bottom", pady=10)

    # --- 기능 로직 ---
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
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='#4A90E2', width=3)

    def on_move_press(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        x, y = min(self.start_x, event.x), min(self.start_y, event.y)
        w, h = abs(self.start_x - event.x), abs(self.start_y - event.y)
        self.scan_region = (x, y, w, h)
        self.selection_window.destroy()
        self.status_label.config(text="✅ 영역 설정이 완료되었습니다.", fg="#67C23A")
        self.btn_toggle.config(state=tk.NORMAL, bg="#67C23A", fg="white")

    def calculate_max_challenge(self, rank):
        # 표 기준 공식: 100위 이상 92%, 99위 이하 35%
        ratio = 0.92 if rank >= 100 else 0.35
        target = int(rank * ratio)
        if target < 1: target = 1
        return f"{target} 위"

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
                        rank_text = "순위 없음" if current_rank == 3001 else f"{current_rank} 위"
                        self.rank_display.config(text=rank_text)
                        self.target_display.config(text=self.calculate_max_challenge(current_rank))
                except:
                    pass
            time.sleep(1.2)

    def toggle_scan(self):
        if not self.running:
            self.running = True
            self.btn_toggle.config(text="⏹ 스캔 중지", bg="#F56C6C")
            self.status_label.config(text="🔍 실시간으로 순위를 추적 중입니다...", fg="#4A90E2")
            threading.Thread(target=self.scan_loop, daemon=True).start()
        else:
            self.running = False
            self.btn_toggle.config(text="▶ 스캔 재개", bg="#67C23A")
            self.status_label.config(text="⏸ 스캔이 일시 중지되었습니다.", fg="#E6A23C")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRankScanner(root)
    root.mainloop()