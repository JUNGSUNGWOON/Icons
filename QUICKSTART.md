# 🚀 빠른 시작 가이드

## 1분 안에 시작하기

### 📋 사전 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)

### ⚡ 빠른 설치 (Windows)

```cmd
# 1. 패키지 설치
pip install -r requirements.txt

# 2. ChromeDriver 설치 (두 가지 방법 중 선택)

## 방법 A: 자동 (네트워크 필요)
pip install webdriver-manager

## 방법 B: 수동 (권장 - 회사 네트워크)
# CHROMEDRIVER_GUIDE.md 파일을 참고하여 수동 설치
# 간단 요약:
# 1) https://chromedriver.chromium.org/downloads 에서 다운로드
# 2) chromedriver.exe를 프로젝트 폴더에 복사

# 3. 실행 스크립트 실행
run.bat
```

### ⚡ 빠른 설치 (Mac/Linux)

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. ChromeDriver 설치 (두 가지 방법 중 선택)

## 방법 A: 자동 (네트워크 필요)
pip install webdriver-manager

## 방법 B: 수동 (권장 - 회사 네트워크)
# CHROMEDRIVER_GUIDE.md 파일을 참고하여 수동 설치
# 간단 요약:
# 1) https://chromedriver.chromium.org/downloads 에서 다운로드
# 2) chmod +x chromedriver
# 3) sudo mv chromedriver /usr/local/bin/

# 3. 실행 스크립트에 실행 권한 부여
chmod +x run.sh

# 4. 실행
./run.sh
```

### 🌐 Streamlit 웹 앱 직접 실행

```bash
streamlit run streamlit_app.py
```

브라우저에서 자동으로 열립니다!

---

## 🎯 첫 번째 다운로드

### 방법 1: Streamlit 웹 앱 사용 (추천)

1. **앱 실행**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **아이템 입력**
   - 좌측 텍스트 영역에 아이템 인덱스 입력
   - 또는 `item_list.txt` 파일 업로드

3. **다운로드**
   - "🎯 다운로드 시작" 버튼 클릭
   - 진행 상황 실시간 확인

4. **결과 확인**
   - 이미지 미리보기
   - ZIP 파일로 일괄 다운로드

### 방법 2: 커맨드라인 사용

1. **item_list.txt 생성**
   ```
   113302
   113303
   7119
   7120
   ```

2. **실행**
   ```bash
   python main_final.py
   ```

---

## 📱 다른 컴퓨터에서 접속하기

### 로컬 네트워크에서 공유

```bash
# 모든 네트워크 인터페이스에서 접속 허용
streamlit run streamlit_app.py --server.address 0.0.0.0
```

다른 컴퓨터에서:
```
http://your-ip-address:8501
```

### 내 IP 주소 확인

**Windows:**
```cmd
ipconfig
```

**Mac/Linux:**
```bash
ifconfig
# 또는
ip addr show
```

---

## 🐳 Docker로 실행 (선택사항)

### Docker가 설치되어 있다면:

```bash
# 한 번에 빌드 및 실행
docker-compose up -d

# 접속
브라우저에서 http://localhost:8501

# 중지
docker-compose down
```

---

## 🔧 문제 해결

### "ConnectionError: Could not reach host" 오류

네트워크 제한으로 ChromeDriver 자동 다운로드 실패:

```bash
# 해결: ChromeDriver 수동 설치
# CHROMEDRIVER_GUIDE.md 참고
```

**빠른 해결:**
1. https://chromedriver.chromium.org/downloads 방문
2. Chrome 버전에 맞는 ChromeDriver 다운로드
3. 프로젝트 폴더에 배치
4. Streamlit 앱 재실행

### "chromedriver not found" 오류

ChromeDriver가 설치되지 않음:

```bash
# 자동 설치 (네트워크 필요)
pip install webdriver-manager

# 또는 수동 설치
# CHROMEDRIVER_GUIDE.md 참고
```

### "streamlit not found" 오류

```bash
pip install streamlit
```

### 브라우저가 자동으로 열리지 않음

수동으로 브라우저에서 열기:
```
http://localhost:8501
```

### 포트 8501이 이미 사용 중

다른 포트 사용:
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 📝 테스트 아이템 인덱스

처음 테스트할 때 사용할 수 있는 아이템 인덱스:

```
121320
130114
113302
113303
7119
7120
```

---

## 💡 다음 단계

- 📖 [전체 문서 읽기](README.md)
- 🌐 [Streamlit Cloud에 배포하기](README.md#배포-방법)
- 🐛 [문제 해결 가이드](README.md#문제-해결)

---

**즐거운 다운로드 되세요! 🍁**
