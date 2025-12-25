
# 🏆 줘팸터 실시간 순위 분석기 (Jweo Paem Rank Scanner)

![image](readme01.png)

> **Google Gemini**와 함께 개발한 파이썬 유틸리티입니다.
> **트릭컬 리바이브**의 '승자의 줘팸터' 화면을 실시간으로 분석하여 즉시 도전 가능한 최상위 순위를 계산해 줍니다.

---

## ✨ 주요 기능

* **Gemini AI Thought Partner:** Google Gemini와의 협업을 통해 설계된 효율적인 코드 구조 및 GUI.
* **실시간 화면 인식:** `EasyOCR`을 사용하여 별도의 엔진 설치 없이 화면 속 숫자를 판독.
* **직관적인 영역 지정:** 마우스 드래그를 통해 스캔할 영역을 직접 자유롭게 설정 가능.
* **모던한 GUI:** `Tkinter` 기반의 깔끔한 카드형 디자인으로 시인성 확보.

## 📊 계산 로직 및 출처

본 프로그램의 계산 공식은 [트릭컬 리바이브 채널의 정보글](https://arca.live/b/trickcal/100398712)을 참고하여 제작되었습니다.

| 현재 순위 구간 | 적용 비율 | 비고 |
| --- | --- | --- |
| **100위 ~ 3001위** | **92%** | 현재 순위 × 0.92 (소수점 버림) |
| **1위 ~ 99위** | **35%** | 현재 순위 × 0.35 (최소 1위 보정) |

## 🚀 시작하기

### 1. 필수 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 2. 실행 방법

```bash
python rank_scanner.py
```

### option. 실행 파일(.exe) 생성하기
PyInstaller를 사용하여 단일 실행 파일을 빌드합니다.

```bash
pyinstaller --noconsole --onefile --name "Trickcal_Jweo_Paem_Calculator" rank_scanner.py
```
빌드가 완료되면 dist 폴더 안에 Trickcal_Rank_Scanner.exe 파일이 생성됩니다.

## 📦 기술 스택

* **AI Thought Partner:** Google Gemini
* **Language:** Python 3.8+
* **Library:** EasyOCR, PyAutoGUI, NumPy, Pillow, Tkinter, PyInstaller

## 🤝 기여 및 출처

* **계산식 참고:** [아카라이브 트릭컬 채널 (ID: 교주님)](https://arca.live/b/trickcal/100398712)
* **개발 파트너:** Google Gemini

---

**Designed with 💖 by Gemini & Coding Partner**